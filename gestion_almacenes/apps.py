from django.apps import AppConfig 
from django.contrib.admin.apps import AdminConfig


class GestionAlmacenesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_almacenes'
    
    def ready(self):
        super().ready()
        AdminConfig.default_site = 'gestion_almacenes.admin.MyAdminSite'