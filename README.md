# Danish Data Science Community - website
Welcome!

## Introduction
This is Danish Data Science Communities internal website repository.
If you are new to the Django webframework please take a look at the [Django documentation](https://www.djangoproject.com)

## Table of Contents
- [Local Development Setup](#local-development-setup)
- [Azure Deployment](#azure-deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Local Development Setup

### Installing dependencies (Linux/MacOs)
In the root folder of the repository you will find a `requirements.txt`.
While positioned in the root folder, run the following commands.

```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Installing dependencies (Windows)
```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### App dependencies
The application has a range of dependencies used in production. To make developing look as much as production as possible we use docker compose to run Redis, MinIO and PostgreSQL. If you haven't got docker go get docker desktop [here](https://docs.docker.com/desktop/)

If you have docker compose, run the following command while positioned in the root folder of the repository
```bash
docker compose up
```
This will start a range of backend applications needed.

### Database Setup
While positioned at `/ddsc-website/ddsc_web/` (same folder as manage.py file) run the following commands.

```bash
python manage.py migrate --settings=ddsc_web.settings.dev
python manage.py collectstatic --no-input --settings=ddsc_web.settings.dev
```
This will first create the tables in your database for the website application and then collect static files and put them into the S3 bucket.

### Starting the development server with Celery
To run the website development server, run the following command.

```bash
python manage.py runserver --settings=ddsc_web.settings.dev
```
To start the Celery task executioner run the below executable from a separate terminal. NOTE that you will need to activate your virtual environment again in the new terminal.
```bash
./start_dev_celery.sh
```

If you want to be able to access `/admin` you need a user with superuser status. Run the command below to create one.

```bash
python manage.py createsuperuser --settings=ddsc_web.settings.dev
```

## Azure Deployment

This application is ready for deployment to Azure Container Apps with all necessary infrastructure.

### Quick Start - Azure Deployment

#### Prerequisites
- Azure CLI installed ([Install Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
- Docker Desktop ([Install Guide](https://docs.docker.com/desktop/))
- Azure subscription with appropriate permissions

#### Option 1: Deploy with Bicep (Recommended)
```powershell
# Login to Azure
az login

# Navigate to infrastructure directory
cd infra

# Deploy to production
.\deploy.ps1 -Environment prod -ResourceGroup rg-ddsc-prod -Location northeurope
```

#### Option 2: Local Testing with Azure Configuration
```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit .env with your values
notepad .env

# Start Azure-compatible local environment
docker-compose -f docker-compose.azure.yml up -d
```

### Documentation
- **[AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)** - Complete Azure deployment guide
- **[AZURE_QUICK_REFERENCE.md](AZURE_QUICK_REFERENCE.md)** - Quick command reference
- **[infra/README.md](infra/README.md)** - Infrastructure as Code documentation

### Azure Resources
The deployment creates:
- Azure Container Apps (Web + Celery workers)
- Azure Database for PostgreSQL
- Azure Cache for Redis
- Azure Blob Storage
- Log Analytics Workspace

### Key Files
- `Dockerfile` - Web application container
- `Dockerfile.celery` - Celery worker container
- `docker-compose.azure.yml` - Azure-compatible local testing
- `ddsc_web/ddsc_web/settings/azure.py` - Azure production settings
- `infra/main.bicep` - Infrastructure as Code template
- `.github/workflows/azure-deploy.yml` - CI/CD pipeline

## Documentation

### Product & Technical Documentation
- **[PRODUCT_REQUIREMENTS.md](PRODUCT_REQUIREMENTS.md)** - Product requirements and features
- **[TECHNICAL_REQUIREMENTS.md](TECHNICAL_REQUIREMENTS.md)** - Technical architecture and stack
- **[ROADMAP.md](ROADMAP.md)** - Development roadmap
- **[NEWS.md](NEWS.md)** - Release notes and updates

### Deployment Documentation
- **[AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)** - Complete Azure deployment guide
- **[AZURE_QUICK_REFERENCE.md](AZURE_QUICK_REFERENCE.md)** - Quick command reference for Azure

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python manage.py test --settings=ddsc_web.settings.dev`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

See LICENSE file for details.

---

**For deployment issues or questions, see [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) or contact the maintainers.**
