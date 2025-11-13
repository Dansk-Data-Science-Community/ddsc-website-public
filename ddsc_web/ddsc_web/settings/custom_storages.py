from django.conf import settings

# Use Azure backend if AZURE_ACCOUNT_NAME is set, otherwise fall back to S3
if hasattr(settings, 'AZURE_ACCOUNT_NAME') and settings.AZURE_ACCOUNT_NAME:
    from storages.backends.azure_storage import AzureStorage
    
    class StaticStorage(AzureStorage):
        account_name = settings.AZURE_ACCOUNT_NAME
        account_key = settings.AZURE_ACCOUNT_KEY
        azure_container = settings.AWS_STORAGE_BUCKET_NAME
        location = settings.STATICFILES_LOCATION
        overwrite_files = True
    
    class PublicMediaStorage(AzureStorage):
        account_name = settings.AZURE_ACCOUNT_NAME
        account_key = settings.AZURE_ACCOUNT_KEY
        azure_container = settings.AWS_STORAGE_BUCKET_NAME
        location = settings.PUBLIC_MEDIA_LOCATION
        overwrite_files = False
    
    class PrivateMediaStorage(AzureStorage):
        account_name = settings.AZURE_ACCOUNT_NAME
        account_key = settings.AZURE_ACCOUNT_KEY
        azure_container = settings.AWS_STORAGE_BUCKET_NAME
        location = settings.PRIVATE_MEDIA_LOCATION
        overwrite_files = False
else:
    from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage
    
    class StaticStorage(S3StaticStorage):
        location = settings.STATICFILES_LOCATION
        default_acl = "public-read"

        def get_object_parameters(self, name):
            return {
                "CacheControl": "public, max-age=86400",
            }

    class PublicMediaStorage(S3Boto3Storage):
        location = settings.PUBLIC_MEDIA_LOCATION
        file_overwrite = False
        default_acl = "public-read"

    class PrivateMediaStorage(S3Boto3Storage):
        location = settings.PRIVATE_MEDIA_LOCATION
        default_acl = "private"
        file_overwrite = False
        custom_domain = False
