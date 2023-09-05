from django.apps import AppConfig

# Configuration for the 'base' app
class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Define the default primary key field
    name = 'base'  # Set the name of the app as 'base'

