from django.contrib import admin
from django.apps import apps

myapp = apps.get_app_config('housing_portal')
# myapp.models

for model in myapp.models.values():
    try:
        admin.site.register(model)
    except Exception as e:
        pass