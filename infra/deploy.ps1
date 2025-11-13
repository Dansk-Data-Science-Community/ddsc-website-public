# Azure Infrastructure Deployment Script for DDSC Website
# This script automates the deployment of all Azure resources using Bicep

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('dev', 'staging', 'prod')]
    [string]$Environment,
    
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroup,
    
    [Parameter(Mandatory=$true)]
    [string]$Location,
    
    [Parameter(Mandatory=$false)]
    [string]$SubscriptionId,
    
    [Parameter(Mandatory=$false)]
    [switch]$WhatIf
)

# Script configuration
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BicepFile = Join-Path $ScriptDir "main.bicep"
$ParametersFile = Join-Path $ScriptDir "parameters.$Environment.json"

Write-Host "=================================="
Write-Host "DDSC Azure Deployment Script"
Write-Host "=================================="
Write-Host "Environment: $Environment"
Write-Host "Resource Group: $ResourceGroup"
Write-Host "Location: $Location"
Write-Host ""

# Check if Azure CLI is installed
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "✓ Azure CLI version: $($azVersion.'azure-cli')" -ForegroundColor Green
} catch {
    Write-Host "✗ Azure CLI is not installed. Please install it from https://aka.ms/installazurecliwindows" -ForegroundColor Red
    exit 1
}

# Set subscription if provided
if ($SubscriptionId) {
    Write-Host "Setting subscription to: $SubscriptionId"
    az account set --subscription $SubscriptionId
}

# Get current subscription
$currentSubscription = az account show --output json | ConvertFrom-Json
Write-Host "✓ Using subscription: $($currentSubscription.name) ($($currentSubscription.id))" -ForegroundColor Green
Write-Host ""

# Check if resource group exists
$rgExists = az group exists --name $ResourceGroup
if ($rgExists -eq "false") {
    Write-Host "Creating resource group: $ResourceGroup in $Location"
    az group create --name $ResourceGroup --location $Location
    Write-Host "✓ Resource group created" -ForegroundColor Green
} else {
    Write-Host "✓ Resource group already exists" -ForegroundColor Green
}
Write-Host ""

# Validate Bicep file
Write-Host "Validating Bicep template..."
try {
    az deployment group validate `
        --resource-group $ResourceGroup `
        --template-file $BicepFile `
        --parameters $ParametersFile `
        --output none
    Write-Host "✓ Bicep template is valid" -ForegroundColor Green
} catch {
    Write-Host "✗ Bicep template validation failed:" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}
Write-Host ""

# Preview changes with What-If
Write-Host "Previewing deployment changes..."
az deployment group what-if `
    --resource-group $ResourceGroup `
    --template-file $BicepFile `
    --parameters $ParametersFile

Write-Host ""
Write-Host "What-If analysis complete. Review the changes above."
Write-Host ""

# If WhatIf switch is set, exit here
if ($WhatIf) {
    Write-Host "WhatIf mode enabled. Exiting without deploying." -ForegroundColor Yellow
    exit 0
}

# Confirm deployment
$confirmation = Read-Host "Do you want to proceed with the deployment? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "Deployment cancelled by user." -ForegroundColor Yellow
    exit 0
}

# Deploy infrastructure
Write-Host ""
Write-Host "Starting deployment..."
$deploymentName = "ddsc-deployment-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

try {
    $deployment = az deployment group create `
        --name $deploymentName `
        --resource-group $ResourceGroup `
        --template-file $BicepFile `
        --parameters $ParametersFile `
        --output json | ConvertFrom-Json
    
    Write-Host ""
    Write-Host "=================================="
    Write-Host "✓ Deployment completed successfully!" -ForegroundColor Green
    Write-Host "=================================="
    Write-Host ""
    Write-Host "Deployment Outputs:"
    Write-Host "------------------"
    
    $outputs = $deployment.properties.outputs
    foreach ($output in $outputs.PSObject.Properties) {
        Write-Host "$($output.Name): $($output.Value.value)" -ForegroundColor Cyan
    }
    
    Write-Host ""
    Write-Host "Web Application URL: https://$($outputs.webAppUrl.value)" -ForegroundColor Green
    Write-Host "Azure Portal: https://portal.azure.com/#@/resource/subscriptions/$($currentSubscription.id)/resourceGroups/$ResourceGroup" -ForegroundColor Cyan
    
    # Save outputs to file
    $outputsFile = Join-Path $ScriptDir "deployment-outputs-$Environment.json"
    $outputs | ConvertTo-Json -Depth 10 | Out-File $outputsFile
    Write-Host ""
    Write-Host "Deployment outputs saved to: $outputsFile"
    
} catch {
    Write-Host ""
    Write-Host "✗ Deployment failed:" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}

# Post-deployment steps
Write-Host ""
Write-Host "=================================="
Write-Host "Post-Deployment Steps"
Write-Host "=================================="
Write-Host ""
Write-Host "1. Run database migrations:"
Write-Host "   az containerapp exec --name ddsc-$Environment-web --resource-group $ResourceGroup --command 'python manage.py migrate --noinput'" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Collect static files:"
Write-Host "   az containerapp exec --name ddsc-$Environment-web --resource-group $ResourceGroup --command 'python manage.py collectstatic --noinput'" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Create superuser (interactive):"
Write-Host "   az containerapp exec --name ddsc-$Environment-web --resource-group $ResourceGroup --command 'python manage.py createsuperuser'" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Configure custom domain (if needed):"
Write-Host "   See AZURE_DEPLOYMENT.md for instructions" -ForegroundColor Yellow
Write-Host ""
Write-Host "Deployment complete! 🎉"
