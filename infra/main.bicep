// Main Bicep template for DDSC Website Azure Infrastructure
// This template deploys all required Azure resources for the Django application
targetScope = 'resourceGroup'

// ============================================================================
// Parameters
// ============================================================================

@description('Environment name (dev, staging, prod)')
@allowed([
  'dev'
  'staging'
  'prod'
])
param environment string = 'prod'

@description('Azure region for all resources')
param location string = resourceGroup().location

@description('Application name prefix')
param appName string = 'ddsc'

@description('PostgreSQL administrator username')
@secure()
param postgresAdminUsername string

@description('PostgreSQL administrator password')
@secure()
param postgresAdminPassword string

@description('Django secret key')
@secure()
param djangoSecretKey string

@description('Email user for SMTP')
param emailUser string

@description('Email password for SMTP')
@secure()
param emailPassword string

@description('Allowed hosts (comma-separated)')
param allowedHosts string

@description('Custom domain name (optional)')
param customDomain string = ''

@description('Container image tag')
param imageTag string = 'latest'

@description('Container Registry name (leave empty to use Docker Hub)')
param containerRegistryName string = ''

// ============================================================================
// Variables
// ============================================================================

var resourceNamePrefix = '${appName}-${environment}'
var postgresServerName = '${resourceNamePrefix}-postgres'
var redisName = '${resourceNamePrefix}-redis'
var storageAccountName = replace('${appName}${environment}stor', '-', '')
var logWorkspaceName = '${resourceNamePrefix}-logs'
var containerEnvName = '${resourceNamePrefix}-env'
var webAppName = '${resourceNamePrefix}-web'
var celeryAppName = '${resourceNamePrefix}-celery'
var containerName = appName

// Container image references
var webImage = empty(containerRegistryName) ? 'ddsc/web:${imageTag}' : '${containerRegistryName}.azurecr.io/ddsc-web:${imageTag}'
var celeryImage = empty(containerRegistryName) ? 'ddsc/celery:${imageTag}' : '${containerRegistryName}.azurecr.io/ddsc-celery:${imageTag}'

// ============================================================================
// Log Analytics Workspace
// ============================================================================

resource logWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logWorkspaceName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// ============================================================================
// Azure Database for PostgreSQL Flexible Server
// ============================================================================

resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: postgresServerName
  location: location
  sku: {
    name: 'Standard_B2s'
    tier: 'Burstable'
  }
  properties: {
    version: '13'
    administratorLogin: postgresAdminUsername
    administratorLoginPassword: postgresAdminPassword
    storage: {
      storageSizeGB: 32
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
  }
}

// PostgreSQL Database
resource postgresDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  parent: postgresServer
  name: 'ddsc_production'
}

// PostgreSQL Firewall Rule - Allow Azure Services
resource postgresFirewallRule 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2022-12-01' = {
  parent: postgresServer
  name: 'AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// ============================================================================
// Azure Cache for Redis
// ============================================================================

resource redisCache 'Microsoft.Cache/redis@2023-08-01' = {
  name: redisName
  location: location
  properties: {
    sku: {
      name: 'Basic'
      family: 'C'
      capacity: 1
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
    redisConfiguration: {
      'maxmemory-policy': 'allkeys-lru'
    }
  }
}

// ============================================================================
// Azure Storage Account (Blob Storage)
// ============================================================================

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: true
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

// Blob Service
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
}

// Blob Container
resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: containerName
  properties: {
    publicAccess: 'Blob'
  }
}

// ============================================================================
// Container Apps Environment
// ============================================================================

resource containerEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: containerEnvName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logWorkspace.properties.customerId
        sharedKey: logWorkspace.listKeys().primarySharedKey
      }
    }
  }
}

// ============================================================================
// Web Container App (Django Application)
// ============================================================================

resource webApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: webAppName
  location: location
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
        transport: 'auto'
        allowInsecure: false
      }
      secrets: [
        {
          name: 'secret-key'
          value: djangoSecretKey
        }
        {
          name: 'postgres-password'
          value: postgresAdminPassword
        }
        {
          name: 'redis-password'
          value: redisCache.listKeys().primaryKey
        }
        {
          name: 'azure-storage-key'
          value: storageAccount.listKeys().keys[0].value
        }
        {
          name: 'email-password'
          value: emailPassword
        }
      ]
      registries: empty(containerRegistryName) ? [] : [
        {
          server: '${containerRegistryName}.azurecr.io'
          username: containerRegistryName
          passwordSecretRef: 'acr-password'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'web'
          image: webImage
          resources: {
            cpu: json('1.0')
            memory: '2Gi'
          }
          env: [
            {
              name: 'DJANGO_SETTINGS_MODULE'
              value: 'ddsc_web.settings.azure'
            }
            {
              name: 'SECRET_KEY'
              secretRef: 'secret-key'
            }
            {
              name: 'ALLOWED_HOSTS'
              value: allowedHosts
            }
            {
              name: 'POSTGRES_HOST'
              value: postgresServer.properties.fullyQualifiedDomainName
            }
            {
              name: 'POSTGRES_DB'
              value: 'ddsc_production'
            }
            {
              name: 'POSTGRES_USER'
              value: postgresAdminUsername
            }
            {
              name: 'POSTGRES_PASSWORD'
              secretRef: 'postgres-password'
            }
            {
              name: 'POSTGRES_PORT'
              value: '5432'
            }
            {
              name: 'REDIS_HOST'
              value: redisCache.properties.hostName
            }
            {
              name: 'REDIS_PORT'
              value: '6380'
            }
            {
              name: 'REDIS_PASSWORD'
              secretRef: 'redis-password'
            }
            {
              name: 'REDIS_SSL'
              value: 'true'
            }
            {
              name: 'AZURE_ACCOUNT_NAME'
              value: storageAccount.name
            }
            {
              name: 'AZURE_ACCOUNT_KEY'
              secretRef: 'azure-storage-key'
            }
            {
              name: 'AZURE_STORAGE_CONTAINER'
              value: containerName
            }
            {
              name: 'AZURE_STORAGE_LOCATION'
              value: environment
            }
            {
              name: 'EMAIL_USER'
              value: emailUser
            }
            {
              name: 'EMAIL_PASSWORD'
              secretRef: 'email-password'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
        rules: [
          {
            name: 'http-scaling'
            http: {
              metadata: {
                concurrentRequests: '50'
              }
            }
          }
        ]
      }
    }
  }
}

// ============================================================================
// Celery Container App (Background Workers)
// ============================================================================

resource celeryApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: celeryAppName
  location: location
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: {
      secrets: [
        {
          name: 'secret-key'
          value: djangoSecretKey
        }
        {
          name: 'postgres-password'
          value: postgresAdminPassword
        }
        {
          name: 'redis-password'
          value: redisCache.listKeys().primaryKey
        }
        {
          name: 'azure-storage-key'
          value: storageAccount.listKeys().keys[0].value
        }
        {
          name: 'email-password'
          value: emailPassword
        }
      ]
      registries: empty(containerRegistryName) ? [] : [
        {
          server: '${containerRegistryName}.azurecr.io'
          username: containerRegistryName
          passwordSecretRef: 'acr-password'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'celery'
          image: celeryImage
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: [
            {
              name: 'DJANGO_SETTINGS_MODULE'
              value: 'ddsc_web.settings.azure'
            }
            {
              name: 'SECRET_KEY'
              secretRef: 'secret-key'
            }
            {
              name: 'POSTGRES_HOST'
              value: postgresServer.properties.fullyQualifiedDomainName
            }
            {
              name: 'POSTGRES_DB'
              value: 'ddsc_production'
            }
            {
              name: 'POSTGRES_USER'
              value: postgresAdminUsername
            }
            {
              name: 'POSTGRES_PASSWORD'
              secretRef: 'postgres-password'
            }
            {
              name: 'POSTGRES_PORT'
              value: '5432'
            }
            {
              name: 'REDIS_HOST'
              value: redisCache.properties.hostName
            }
            {
              name: 'REDIS_PORT'
              value: '6380'
            }
            {
              name: 'REDIS_PASSWORD'
              secretRef: 'redis-password'
            }
            {
              name: 'REDIS_SSL'
              value: 'true'
            }
            {
              name: 'AZURE_ACCOUNT_NAME'
              value: storageAccount.name
            }
            {
              name: 'AZURE_ACCOUNT_KEY'
              secretRef: 'azure-storage-key'
            }
            {
              name: 'EMAIL_USER'
              value: emailUser
            }
            {
              name: 'EMAIL_PASSWORD'
              secretRef: 'email-password'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
      }
    }
  }
}

// ============================================================================
// Outputs
// ============================================================================

output webAppUrl string = webApp.properties.configuration.ingress.fqdn
output postgresServerName string = postgresServer.name
output postgresServerFqdn string = postgresServer.properties.fullyQualifiedDomainName
output redisHostName string = redisCache.properties.hostName
output storageAccountName string = storageAccount.name
output containerEnvName string = containerEnv.name
output resourceGroupName string = resourceGroup().name
