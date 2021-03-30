from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(app_master)
admin.site.register(contact_us)
admin.site.register(app_settings)
admin.site.register(admin_logs)
admin.site.register(email_configuration)