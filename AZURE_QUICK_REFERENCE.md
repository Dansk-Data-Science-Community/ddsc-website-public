# Azure Deployment Quick Reference

## Pre-Deployment Checklist

- [ ] Azure CLI installed and logged in
- [ ] Docker Desktop installed
- [ ] Python 3.11.9 installed
- [ ] Azure subscription with sufficient quota
- [ ] Email SMTP credentials ready
- [ ] Domain name (if using custom domain)

## Environment Variables Required

### Critical Secrets
```
SECRET_KEY                  # Django secret key (50+ characters)
POSTGRES_PASSWORD           # Database admin password
REDIS_PASSWORD              # Redis access key
AZURE_ACCOUNT_KEY          # Storage account key
EMAIL_PASSWORD             # Email SMTP password
```

### Configuration
```
DJANGO_SETTINGS_MODULE=ddsc_web.settings.azure
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
POSTGRES_HOST=server.postgres.database.azure.com
POSTGRES_DB=ddsc_production
POSTGRES_USER=django_admin
POSTGRES_PORT=5432
REDIS_HOST=cache.redis.cache.windows.net
REDIS_PORT=6380
REDIS_SSL=true
AZURE_ACCOUNT_NAME=storageaccount
AZURE_STORAGE_CONTAINER=ddsc
AZURE_STORAGE_LOCATION=prod
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your@email.com
```

## Quick Deployment Commands

### 1. Local Testing
```powershell
# Start local Azure-compatible environment
docker-compose -f docker-compose.azure.yml up -d

# Check status
docker-compose -f docker-compose.azure.yml ps

# View logs
docker-compose -f docker-compose.azure.yml logs -f web

# Stop
docker-compose -f docker-compose.azure.yml down
```

### 2. Build Docker Images
```powershell
# Web application
docker build -t ddsc-web:latest -f Dockerfile .

# Celery worker
docker build -t ddsc-celery:latest -f Dockerfile.celery .

# Test locally
docker run -p 8000:8000 --env-file .env ddsc-web:latest
```

### 3. Deploy with Bicep
```powershell
# Navigate to infra directory
cd infra

# Deploy (with what-if preview)
.\deploy.ps1 -Environment prod -ResourceGroup rg-ddsc-prod -Location northeurope

# Deploy without confirmation
.\deploy.ps1 -Environment prod -ResourceGroup rg-ddsc-prod -Location northeurope -WhatIf:$false
```

### 4. Post-Deployment Setup
```powershell
$RESOURCE_GROUP = "rg-ddsc-prod"
$WEB_APP = "ddsc-prod-web"

# Run migrations
az containerapp exec `
  --name $WEB_APP `
  --resource-group $RESOURCE_GROUP `
  --command "python manage.py migrate --noinput"

# Collect static files
az containerapp exec `
  --name $WEB_APP `
  --resource-group $RESOURCE_GROUP `
  --command "python manage.py collectstatic --noinput"

# Create superuser (interactive)
az containerapp exec `
  --name $WEB_APP `
  --resource-group $RESOURCE_GROUP `
  --command "python manage.py createsuperuser"

# Create event groups
az containerapp exec `
  --name $WEB_APP `
  --resource-group $RESOURCE_GROUP `
  --command "python manage.py event_groups"
```

## Common Operations

### View Logs
```powershell
# Follow web app logs
az containerapp logs show --name ddsc-prod-web --resource-group rg-ddsc-prod --follow

# Follow celery logs
az containerapp logs show --name ddsc-prod-celery --resource-group rg-ddsc-prod --follow

# Last 100 lines
az containerapp logs show --name ddsc-prod-web --resource-group rg-ddsc-prod --tail 100
```

### Scale Applications
```powershell
# Scale web app
az containerapp update `
  --name ddsc-prod-web `
  --resource-group rg-ddsc-prod `
  --min-replicas 2 `
  --max-replicas 10

# Scale celery
az containerapp update `
  --name ddsc-prod-celery `
  --resource-group rg-ddsc-prod `
  --min-replicas 2 `
  --max-replicas 5
```

### Update Environment Variables
```powershell
# Update a single variable
az containerapp update `
  --name ddsc-prod-web `
  --resource-group rg-ddsc-prod `
  --set-env-vars ALLOWED_HOSTS=newdomain.com,www.newdomain.com

# Update a secret
az containerapp secret set `
  --name ddsc-prod-web `
  --resource-group rg-ddsc-prod `
  --secrets secret-key=new-secret-key-value
```

### Database Operations
```powershell
# Backup database
az postgres flexible-server backup create `
  --resource-group rg-ddsc-prod `
  --name ddsc-postgres-prod

# List backups
az postgres flexible-server backup list `
  --resource-group rg-ddsc-prod `
  --name ddsc-postgres-prod

# Connect to database
az postgres flexible-server connect `
  --name ddsc-postgres-prod `
  --admin-user django_admin `
  --database ddsc_production
```

### Restart Applications
```powershell
# Restart web app
az containerapp revision restart `
  --name ddsc-prod-web `
  --resource-group rg-ddsc-prod

# Restart celery
az containerapp revision restart `
  --name ddsc-prod-celery `
  --resource-group rg-ddsc-prod
```

## Troubleshooting

### Container Won't Start
```powershell
# Check revision status
az containerapp revision list `
  --name ddsc-prod-web `
  --resource-group rg-ddsc-prod `
  --output table

# Get detailed logs
az containerapp logs show `
  --name ddsc-prod-web `
  --resource-group rg-ddsc-prod `
  --tail 200
```

### Database Connection Issues
```powershell
# Test from container
az containerapp exec `
  --name ddsc-prod-web `
  --resource-group rg-ddsc-prod `
  --command "python manage.py dbshell"

# Check firewall rules
az postgres flexible-server firewall-rule list `
  --resource-group rg-ddsc-prod `
  --name ddsc-postgres-prod
```

### Redis Connection Issues
```powershell
# Get Redis info
az redis show `
  --name ddsc-redis-prod `
  --resource-group rg-ddsc-prod

# Test Redis from container
az containerapp exec `
  --name ddsc-prod-web `
  --resource-group rg-ddsc-prod `
  --command "python -c 'import redis; r=redis.from_url(\"rediss://...\"); print(r.ping())'"
```

### Static Files Not Loading
```powershell
# Re-collect static files
az containerapp exec `
  --name ddsc-prod-web `
  --resource-group rg-ddsc-prod `
  --command "python manage.py collectstatic --noinput --clear"

# Check blob container
az storage blob list `
  --account-name ddscstorprod `
  --container-name ddsc `
  --output table
```

## GitHub Actions Secrets

Configure these secrets in GitHub repository settings:

```
AZURE_CREDENTIALS          # Service principal JSON
ACR_USERNAME               # Container registry username
ACR_PASSWORD               # Container registry password
ALLOWED_HOSTS              # Comma-separated hostnames
POSTGRES_HOST              # PostgreSQL server FQDN
POSTGRES_DB                # Database name
POSTGRES_USER              # Database username
POSTGRES_PASSWORD          # Database password (as secret ref)
REDIS_HOST                 # Redis server FQDN
REDIS_PASSWORD             # Redis access key (as secret ref)
AZURE_ACCOUNT_NAME         # Storage account name
AZURE_STORAGE_KEY          # Storage account key (as secret ref)
EMAIL_USER                 # SMTP username
EMAIL_PASSWORD             # SMTP password (as secret ref)
```

## Monitoring URLs

- **Azure Portal**: https://portal.azure.com
- **Resource Group**: `https://portal.azure.com/#@/resource/subscriptions/{sub-id}/resourceGroups/rg-ddsc-prod`
- **Container Apps**: Navigate to resource group → Container Apps
- **Logs**: Container App → Monitoring → Log stream
- **Metrics**: Container App → Monitoring → Metrics

## Cost Monitoring

```powershell
# View current costs
az consumption usage list `
  --start-date 2024-01-01 `
  --end-date 2024-01-31 `
  --query "[?resourceGroup=='rg-ddsc-prod']"

# Set budget alert (via Portal recommended)
```

## Support Resources

- **Documentation**: See `AZURE_DEPLOYMENT.md` for detailed guide
- **Infrastructure Code**: See `infra/` directory
- **Azure Support**: https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade
- **Container Apps Docs**: https://learn.microsoft.com/azure/container-apps/
