from storages.backends.azure_storage import AzureStorage
from traffic_app_final.settings import AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY, STATIC_LOCATION, MEDIA_LOCATION


class AzureMediaStorage(AzureStorage):
    account_name = AZURE_ACCOUNT_NAME  # Must be replaced by your <storage_account_name>
    account_key = AZURE_ACCOUNT_KEY  # Must be replaced by your <storage_account_key>
    azure_container = MEDIA_LOCATION
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = AZURE_ACCOUNT_NAME  # Must be replaced by your storage_account_name
    account_key = AZURE_ACCOUNT_KEY  # Must be replaced by your <storage_account_key>
    azure_container = STATIC_LOCATION
    expiration_secs = None
