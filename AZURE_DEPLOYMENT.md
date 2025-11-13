# Azure Container Apps Deployment Guide

This guide provides comprehensive instructions for deploying the Danish Data Science Community (DDSC) website to Azure Container Apps with all necessary supporting services.

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Azure Resources Required](#azure-resources-required)
4. [Local Testing with Azure Configuration](#local-testing)
5. [Azure Deployment Steps](#azure-deployment-steps)
6. [Configuration](#configuration)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)

## Architecture Overview

The application will be deployed to Azure using the following services:

```
┌─────────────────────────────────────────────────────────────┐
│                    Azure Container Apps                      │
│  ┌──────────────────┐           ┌──────────────────┐        │
│  │   Web Container  │           │ Celery Container │        │
│  │   (Django App)   │           │    (Workers)     │        │
│  └────────┬─────────┘           └────────┬─────────┘        │
│           │                              │                   │
└───────────┼──────────────────────────────┼───────────────────┘
            │                              │
            ├──────────────┬───────────────┤
            │              │               │
    ┌───────▼──────┐  ┌───▼────────┐  ┌──▼─────────────┐
    │  Azure DB    │  │   Azure    │  │  Azure Blob    │
    │ for PostgreSQL│  │ Cache for  │  │    Storage     │
    │              │  │   Redis    │  │                │
    └──────────────┘  └────────────┘  └────────────────┘
```

## Prerequisites

### Required Tools
- **Azure CLI** (`az`) - [Install Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Docker Desktop** - [Install Guide](https://docs.docker.com/desktop/)
- **Python 3.11.9** - [Download](https://www.python.org/downloads/)
- **Git** - [Install Guide](https://git-scm.com/downloads)

### Azure Subscription
- Active Azure subscription with contributor access
- Sufficient quota for the following resources:
  - Container Apps
  - PostgreSQL Flexible Server
  - Cache for Redis
  - Storage Account

### Verify Prerequisites

```powershell
# Check Azure CLI
az --version

# Check Docker
docker --version

# Check Python
python --version

# Login to Azure
az login

# Set subscription (if you have multiple)
az account set --subscription "Your Subscription Name"
```

## Azure Resources Required

### 1. Resource Group
A logical container for all resources.

### 2. Azure Database for PostgreSQL Flexible Server
- **SKU**: Standard_B2s (minimum) or Standard_D2s_v3 (recommended)
- **Storage**: 32 GB minimum
- **Version**: PostgreSQL 13 or higher
- **Backup**: Enabled with 7-day retention

### 3. Azure Cache for Redis
- **SKU**: Basic C1 (minimum) or Standard C1 (recommended)
- **Version**: Redis 6.x
- **TLS**: Enabled
- **Port**: 6380 (SSL)

### 4. Azure Storage Account
- **SKU**: Standard_LRS (minimum) or Standard_GRS (recommended)
- **Kind**: StorageV2
- **Access Tier**: Hot
- **Containers**: Create a container named `ddsc` with blob public access

### 5. Azure Container Registry (Optional but Recommended)
- **SKU**: Basic (minimum) or Standard (recommended)
- For storing Docker images privately

### 6. Azure Container Apps Environment
- Container Apps hosting environment with managed infrastructure

### 7. Log Analytics Workspace
- For monitoring and diagnostics

## Local Testing with Azure Configuration

Before deploying to Azure, test the configuration locally:

### 1. Create `.env` file

```powershell
# Copy the example file
Copy-Item .env.example .env

# Edit .env with your values
notepad .env
```

### 2. Start services locally

```powershell
# Start all services using Azure-compatible configuration
docker-compose -f docker-compose.azure.yml up -d

# Check logs
docker-compose -f docker-compose.azure.yml logs -f

# Stop services
docker-compose -f docker-compose.azure.yml down
```

### 3. Run migrations and create superuser

```powershell
# Access the web container
docker exec -it ddsc-web-azure bash

# Run migrations
python manage.py migrate --settings=ddsc_web.settings.azure

# Create superuser
python manage.py createsuperuser --settings=ddsc_web.settings.azure

# Exit container
exit
```

### 4. Test the application

Open browser to: http://localhost:8000

## Azure Deployment Steps

### Option A: Deploy Using Azure Container Apps (Recommended)

#### Step 1: Create Resource Group

```powershell
# Set variables
$RESOURCE_GROUP = "rg-ddsc-prod"
$LOCATION = "northeurope"  # or "westeurope"
$ENVIRONMENT = "prod"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION
```

#### Step 2: Create Azure Database for PostgreSQL

```powershell
$DB_SERVER_NAME = "ddsc-postgres-prod"
$DB_ADMIN_USER = "django_admin"
$DB_ADMIN_PASSWORD = "YourSecurePassword123!"  # Use a strong password
$DB_NAME = "ddsc_production"

# Create PostgreSQL server
az postgres flexible-server create `
  --resource-group $RESOURCE_GROUP `
  --name $DB_SERVER_NAME `
  --location $LOCATION `
  --admin-user $DB_ADMIN_USER `
  --admin-password $DB_ADMIN_PASSWORD `
  --sku-name Standard_B2s `
  --tier Burstable `
  --storage-size 32 `
  --version 13 `
  --backup-retention 7

# Create database
az postgres flexible-server db create `
  --resource-group $RESOURCE_GROUP `
  --server-name $DB_SERVER_NAME `
  --database-name $DB_NAME

# Allow Azure services to access
az postgres flexible-server firewall-rule create `
  --resource-group $RESOURCE_GROUP `
  --name $DB_SERVER_NAME `
  --rule-name AllowAzureServices `
  --start-ip-address 0.0.0.0 `
  --end-ip-address 0.0.0.0
```

#### Step 3: Create Azure Cache for Redis

```powershell
$REDIS_NAME = "ddsc-redis-prod"

# Create Redis cache
az redis create `
  --resource-group $RESOURCE_GROUP `
  --name $REDIS_NAME `
  --location $LOCATION `
  --sku Basic `
  --vm-size c1 `
  --enable-non-ssl-port false

# Get Redis connection details
$REDIS_HOST = az redis show --resource-group $RESOURCE_GROUP --name $REDIS_NAME --query "hostName" -o tsv
$REDIS_KEY = az redis list-keys --resource-group $RESOURCE_GROUP --name $REDIS_NAME --query "primaryKey" -o tsv
```

#### Step 4: Create Azure Storage Account

```powershell
$STORAGE_ACCOUNT = "ddscstorprod"  # Must be globally unique, lowercase
$CONTAINER_NAME = "ddsc"

# Create storage account
az storage account create `
  --resource-group $RESOURCE_GROUP `
  --name $STORAGE_ACCOUNT `
  --location $LOCATION `
  --sku Standard_LRS `
  --kind StorageV2

# Get storage account key
$STORAGE_KEY = az storage account keys list `
  --resource-group $RESOURCE_GROUP `
  --account-name $STORAGE_ACCOUNT `
  --query "[0].value" -o tsv

# Create blob container
az storage container create `
  --name $CONTAINER_NAME `
  --account-name $STORAGE_ACCOUNT `
  --account-key $STORAGE_KEY `
  --public-access blob
```

#### Step 5: Create Container Registry (Optional)

```powershell
$ACR_NAME = "ddscacrprod"  # Must be globally unique

# Create ACR
az acr create `
  --resource-group $RESOURCE_GROUP `
  --name $ACR_NAME `
  --sku Basic `
  --admin-enabled true

# Get ACR credentials
$ACR_USERNAME = az acr credential show --name $ACR_NAME --query "username" -o tsv
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv
```

#### Step 6: Build and Push Docker Images

```powershell
# Login to ACR
az acr login --name $ACR_NAME

# Build and push web image
docker build -t "$ACR_NAME.azurecr.io/ddsc-web:latest" -f Dockerfile .
docker push "$ACR_NAME.azurecr.io/ddsc-web:latest"

# Build and push celery image
docker build -t "$ACR_NAME.azurecr.io/ddsc-celery:latest" -f Dockerfile.celery .
docker push "$ACR_NAME.azurecr.io/ddsc-celery:latest"
```

#### Step 7: Create Container Apps Environment

```powershell
# Install Container Apps extension
az extension add --name containerapp --upgrade

# Create Log Analytics workspace
$WORKSPACE_NAME = "ddsc-logs-prod"
az monitor log-analytics workspace create `
  --resource-group $RESOURCE_GROUP `
  --workspace-name $WORKSPACE_NAME `
  --location $LOCATION

$WORKSPACE_ID = az monitor log-analytics workspace show `
  --resource-group $RESOURCE_GROUP `
  --workspace-name $WORKSPACE_NAME `
  --query "customerId" -o tsv

$WORKSPACE_KEY = az monitor log-analytics workspace get-shared-keys `
  --resource-group $RESOURCE_GROUP `
  --workspace-name $WORKSPACE_NAME `
  --query "primarySharedKey" -o tsv

# Create Container Apps environment
$ENVIRONMENT_NAME = "ddsc-env-prod"
az containerapp env create `
  --name $ENVIRONMENT_NAME `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --logs-workspace-id $WORKSPACE_ID `
  --logs-workspace-key $WORKSPACE_KEY
```

#### Step 8: Deploy Web Container App

```powershell
$WEB_APP_NAME = "ddsc-web"

# Create secrets (store sensitive values)
az containerapp create `
  --name $WEB_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --environment $ENVIRONMENT_NAME `
  --image "$ACR_NAME.azurecr.io/ddsc-web:latest" `
  --target-port 8000 `
  --ingress external `
  --min-replicas 1 `
  --max-replicas 5 `
  --cpu 1.0 `
  --memory 2.0Gi `
  --registry-server "$ACR_NAME.azurecr.io" `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --env-vars `
    DJANGO_SETTINGS_MODULE=ddsc_web.settings.azure `
    SECRET_KEY=secretref:secret-key `
    POSTGRES_HOST="$DB_SERVER_NAME.postgres.database.azure.com" `
    POSTGRES_DB=$DB_NAME `
    POSTGRES_USER=$DB_ADMIN_USER `
    POSTGRES_PASSWORD=secretref:postgres-password `
    POSTGRES_PORT=5432 `
    REDIS_HOST=$REDIS_HOST `
    REDIS_PORT=6380 `
    REDIS_PASSWORD=secretref:redis-password `
    REDIS_SSL=true `
    AZURE_ACCOUNT_NAME=$STORAGE_ACCOUNT `
    AZURE_ACCOUNT_KEY=secretref:azure-storage-key `
    AZURE_STORAGE_CONTAINER=$CONTAINER_NAME `
    AZURE_STORAGE_LOCATION=prod `
  --secrets `
    "secret-key=YourSecretKeyHere" `
    "postgres-password=$DB_ADMIN_PASSWORD" `
    "redis-password=$REDIS_KEY" `
    "azure-storage-key=$STORAGE_KEY"

# Get the application URL
$WEB_URL = az containerapp show `
  --name $WEB_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --query "properties.configuration.ingress.fqdn" -o tsv

Write-Host "Application URL: https://$WEB_URL"
```

#### Step 9: Deploy Celery Container App

```powershell
$CELERY_APP_NAME = "ddsc-celery"

az containerapp create `
  --name $CELERY_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --environment $ENVIRONMENT_NAME `
  --image "$ACR_NAME.azurecr.io/ddsc-celery:latest" `
  --min-replicas 1 `
  --max-replicas 3 `
  --cpu 0.5 `
  --memory 1.0Gi `
  --registry-server "$ACR_NAME.azurecr.io" `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --env-vars `
    DJANGO_SETTINGS_MODULE=ddsc_web.settings.azure `
    SECRET_KEY=secretref:secret-key `
    POSTGRES_HOST="$DB_SERVER_NAME.postgres.database.azure.com" `
    POSTGRES_DB=$DB_NAME `
    POSTGRES_USER=$DB_ADMIN_USER `
    POSTGRES_PASSWORD=secretref:postgres-password `
    POSTGRES_PORT=5432 `
    REDIS_HOST=$REDIS_HOST `
    REDIS_PORT=6380 `
    REDIS_PASSWORD=secretref:redis-password `
    REDIS_SSL=true `
    AZURE_ACCOUNT_NAME=$STORAGE_ACCOUNT `
    AZURE_ACCOUNT_KEY=secretref:azure-storage-key `
  --secrets `
    "secret-key=YourSecretKeyHere" `
    "postgres-password=$DB_ADMIN_PASSWORD" `
    "redis-password=$REDIS_KEY" `
    "azure-storage-key=$STORAGE_KEY"
```

#### Step 10: Run Initial Setup

```powershell
# Execute migrations
az containerapp exec `
  --name $WEB_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --command "python manage.py migrate --noinput"

# Collect static files
az containerapp exec `
  --name $WEB_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --command "python manage.py collectstatic --noinput"

# Create superuser (interactive)
az containerapp exec `
  --name $WEB_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --command "python manage.py createsuperuser"
```

### Option B: Deploy Using Bicep Infrastructure as Code

See `infra/main.bicep` for a complete Infrastructure as Code deployment.

```powershell
# Deploy using Bicep
az deployment group create `
  --resource-group $RESOURCE_GROUP `
  --template-file infra/main.bicep `
  --parameters infra/parameters.json
```

## Configuration

### Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key | Yes | Random 50-char string |
| `DJANGO_SETTINGS_MODULE` | Settings module | Yes | `ddsc_web.settings.azure` |
| `ALLOWED_HOSTS` | Comma-separated hosts | Yes | `yourdomain.com,www.yourdomain.com` |
| `POSTGRES_HOST` | PostgreSQL server | Yes | `server.postgres.database.azure.com` |
| `POSTGRES_DB` | Database name | Yes | `ddsc_production` |
| `POSTGRES_USER` | Database user | Yes | `django_admin` |
| `POSTGRES_PASSWORD` | Database password | Yes | Secure password |
| `REDIS_HOST` | Redis server | Yes | `cache.redis.cache.windows.net` |
| `REDIS_PASSWORD` | Redis access key | Yes | From Azure Portal |
| `AZURE_ACCOUNT_NAME` | Storage account | Yes | `ddscstorprod` |
| `AZURE_ACCOUNT_KEY` | Storage key | Yes | From Azure Portal |
| `EMAIL_USER` | SMTP username | Yes | `your@email.com` |
| `EMAIL_PASSWORD` | SMTP password | Yes | App-specific password |

### Custom Domain Configuration

```powershell
# Add custom domain to Container App
az containerapp hostname add `
  --name $WEB_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --hostname "www.yourdomain.com"

# Bind certificate (requires managed certificate or uploaded cert)
az containerapp hostname bind `
  --name $WEB_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --hostname "www.yourdomain.com" `
  --environment $ENVIRONMENT_NAME `
  --validation-method CNAME
```

## Monitoring and Maintenance

### View Logs

```powershell
# View web app logs
az containerapp logs show `
  --name $WEB_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --follow

# View celery logs
az containerapp logs show `
  --name $CELERY_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --follow
```

### Scaling

```powershell
# Scale web app
az containerapp update `
  --name $WEB_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --min-replicas 2 `
  --max-replicas 10

# Scale celery workers
az containerapp update `
  --name $CELERY_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --min-replicas 2 `
  --max-replicas 5
```

### Database Backup

```powershell
# Create manual backup
az postgres flexible-server backup create `
  --resource-group $RESOURCE_GROUP `
  --name $DB_SERVER_NAME

# List backups
az postgres flexible-server backup list `
  --resource-group $RESOURCE_GROUP `
  --name $DB_SERVER_NAME
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Failed
- Verify firewall rules allow Container Apps
- Check PostgreSQL connection string
- Ensure SSL is enabled

```powershell
# Test connection from container
az containerapp exec `
  --name $WEB_APP_NAME `
  --resource-group $RESOURCE_GROUP `
  --command "psql -h $DB_SERVER_NAME.postgres.database.azure.com -U $DB_ADMIN_USER -d $DB_NAME"
```

#### 2. Redis Connection Failed
- Verify TLS/SSL is enabled
- Check Redis access key
- Ensure port 6380 is used

#### 3. Static Files Not Loading
- Verify blob storage container is public
- Check STATIC_URL configuration
- Run `collectstatic` command

#### 4. Container App Not Starting
- Check container logs
- Verify environment variables
- Check resource quotas

### Get Support

- Azure Support: https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade
- Django Documentation: https://docs.djangoproject.com/
- Azure Container Apps: https://learn.microsoft.com/azure/container-apps/

## Security Best Practices

1. **Use Azure Key Vault** for sensitive secrets
2. **Enable HTTPS** for all connections
3. **Restrict database firewall** to Container Apps only
4. **Use managed identities** where possible
5. **Regular security updates** for dependencies
6. **Enable Azure Defender** for Container Apps
7. **Implement WAF** (Web Application Firewall)
8. **Regular backup testing**

## Cost Optimization

1. Use **Consumption plan** for Container Apps
2. Enable **auto-scaling** based on load
3. Use **Basic tier** for development/staging
4. Implement **blob lifecycle policies**
5. Monitor with **Azure Cost Management**
6. Use **reserved instances** for predictable workloads

## Next Steps

1. Configure custom domain and SSL certificate
2. Set up CI/CD pipeline with GitHub Actions
3. Configure monitoring alerts
4. Implement backup and disaster recovery
5. Performance tuning and optimization
6. Security hardening and penetration testing

---

**Last Updated**: November 2025
**Version**: 1.0
