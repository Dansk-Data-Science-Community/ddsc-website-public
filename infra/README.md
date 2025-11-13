# Azure Infrastructure

This directory contains Infrastructure as Code (IaC) files for deploying the DDSC website to Azure Container Apps.

## Files

- **main.bicep** - Main Bicep template defining all Azure resources
- **parameters.json** - Production parameters template (use with Azure Key Vault)
- **parameters.dev.json** - Development parameters (for testing)
- **deploy.ps1** - PowerShell deployment script with validation and what-if analysis

## Quick Start

### Prerequisites

1. Install [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
2. Login to Azure: `az login`
3. Set subscription: `az account set --subscription "Your Subscription"`

### Deploy to Azure

```powershell
# Development environment
.\deploy.ps1 -Environment dev -ResourceGroup rg-ddsc-dev -Location northeurope

# Preview changes only (What-If mode)
.\deploy.ps1 -Environment prod -ResourceGroup rg-ddsc-prod -Location northeurope -WhatIf

# Production deployment
.\deploy.ps1 -Environment prod -ResourceGroup rg-ddsc-prod -Location northeurope
```

### Manual Deployment

```powershell
# Create resource group
az group create --name rg-ddsc-prod --location northeurope

# Validate deployment
az deployment group validate \
  --resource-group rg-ddsc-prod \
  --template-file main.bicep \
  --parameters parameters.json

# Preview changes
az deployment group what-if \
  --resource-group rg-ddsc-prod \
  --template-file main.bicep \
  --parameters parameters.json

# Deploy
az deployment group create \
  --name ddsc-deployment \
  --resource-group rg-ddsc-prod \
  --template-file main.bicep \
  --parameters parameters.json
```

## Resources Created

The Bicep template creates the following Azure resources:

1. **Log Analytics Workspace** - Centralized logging and monitoring
2. **PostgreSQL Flexible Server** - Database with backup and SSL
3. **Azure Cache for Redis** - Session storage and Celery broker
4. **Storage Account** - Blob storage for static and media files
5. **Container Apps Environment** - Managed environment for containers
6. **Web Container App** - Django application (auto-scaling 1-5 instances)
7. **Celery Container App** - Background task workers (auto-scaling 1-3 instances)

## Architecture

```
Container Apps Environment
├── Web App (Django)
│   ├── Min: 1 replica
│   ├── Max: 5 replicas
│   └── Auto-scale on HTTP requests
└── Celery App (Workers)
    ├── Min: 1 replica
    └── Max: 3 replicas

External Services
├── PostgreSQL Flexible Server
├── Redis Cache
└── Blob Storage
```

## Configuration

### Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| environment | Environment name (dev/staging/prod) | Yes | prod |
| location | Azure region | Yes | Resource group location |
| appName | Application name prefix | Yes | ddsc |
| postgresAdminUsername | PostgreSQL admin user | Yes | - |
| postgresAdminPassword | PostgreSQL admin password | Yes | - |
| djangoSecretKey | Django secret key | Yes | - |
| emailUser | SMTP email username | Yes | - |
| emailPassword | SMTP email password | Yes | - |
| allowedHosts | Allowed hosts (comma-separated) | Yes | - |
| customDomain | Custom domain (optional) | No | - |
| imageTag | Container image tag | No | latest |
| containerRegistryName | ACR name (optional) | No | - |

### Secrets Management

For production, store sensitive values in Azure Key Vault:

```powershell
# Create Key Vault
az keyvault create \
  --name ddsc-kv-prod \
  --resource-group rg-ddsc-prod \
  --location northeurope

# Store secrets
az keyvault secret set --vault-name ddsc-kv-prod --name postgres-admin-password --value "YourSecurePassword"
az keyvault secret set --vault-name ddsc-kv-prod --name django-secret-key --value "YourSecretKey"
az keyvault secret set --vault-name ddsc-kv-prod --name email-password --value "YourEmailPassword"

# Update parameters.json to reference Key Vault
```

## Post-Deployment

After deployment, run these commands:

```powershell
# Get outputs
az deployment group show \
  --name ddsc-deployment \
  --resource-group rg-ddsc-prod \
  --query properties.outputs

# Run migrations
az containerapp exec \
  --name ddsc-prod-web \
  --resource-group rg-ddsc-prod \
  --command "python manage.py migrate --noinput"

# Collect static files
az containerapp exec \
  --name ddsc-prod-web \
  --resource-group rg-ddsc-prod \
  --command "python manage.py collectstatic --noinput"

# Create superuser
az containerapp exec \
  --name ddsc-prod-web \
  --resource-group rg-ddsc-prod \
  --command "python manage.py createsuperuser"
```

## Monitoring

### View Logs

```powershell
# Web app logs
az containerapp logs show \
  --name ddsc-prod-web \
  --resource-group rg-ddsc-prod \
  --follow

# Celery logs
az containerapp logs show \
  --name ddsc-prod-celery \
  --resource-group rg-ddsc-prod \
  --follow
```

### Metrics

Access metrics in Azure Portal:
- Navigate to Container App
- Select "Metrics" blade
- Available metrics: CPU, Memory, HTTP requests, Response time

## Scaling

### Manual Scaling

```powershell
# Scale web app
az containerapp update \
  --name ddsc-prod-web \
  --resource-group rg-ddsc-prod \
  --min-replicas 2 \
  --max-replicas 10

# Scale celery workers
az containerapp update \
  --name ddsc-prod-celery \
  --resource-group rg-ddsc-prod \
  --min-replicas 2 \
  --max-replicas 5
```

### Auto-scaling

Auto-scaling is configured in the Bicep template based on:
- HTTP concurrent requests (web app)
- CPU/Memory usage (both apps)

## Troubleshooting

### Container fails to start

```powershell
# Check logs
az containerapp logs show --name ddsc-prod-web --resource-group rg-ddsc-prod --tail 100

# Check revision status
az containerapp revision list --name ddsc-prod-web --resource-group rg-ddsc-prod
```

### Database connection issues

```powershell
# Test connection from container
az containerapp exec \
  --name ddsc-prod-web \
  --resource-group rg-ddsc-prod \
  --command "python manage.py dbshell"
```

### Redis connection issues

```powershell
# Test Redis connection
az containerapp exec \
  --name ddsc-prod-web \
  --resource-group rg-ddsc-prod \
  --command "redis-cli -h <redis-host> -p 6380 --tls ping"
```

## Cost Estimation

Estimated monthly costs (Northern Europe region):

| Resource | SKU | Est. Cost/Month |
|----------|-----|-----------------|
| Container Apps (Web) | 1-5 replicas | €50-250 |
| Container Apps (Celery) | 1-3 replicas | €25-75 |
| PostgreSQL Flexible | Standard_B2s | €50 |
| Redis Cache | Basic C1 | €20 |
| Storage Account | Standard LRS | €5-20 |
| Log Analytics | Per GB | €10-30 |
| **Total** | | **€160-445** |

## Support

- [Azure Container Apps Documentation](https://learn.microsoft.com/azure/container-apps/)
- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Azure CLI Reference](https://learn.microsoft.com/cli/azure/)
