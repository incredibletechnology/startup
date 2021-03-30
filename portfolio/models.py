from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Overriding the Default Django Auth User and adding One More Field (user_type)
class User(AbstractUser):
    phone = models.CharField(max_length=15,blank=True,null=True)
    image = models.ImageField(upload_to='server_user',blank=True,null=True)

class client(models.Model):
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100,blank=False,null=False)
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='client', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.name

class contact_us(models.Model):
    name = models.CharField(max_length=50,blank=False,null=False)
    email = models.CharField(max_length=100,blank=False,null=False)
    phone = models.CharField(max_length=50,blank=True,null=True)
    subject = models.CharField(max_length=50,blank=False,null=False)
    message = models.TextField(blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return "{} | {}".format(self.name,self.email)

class app_master(models.Model):
    app_uuid = models.CharField(max_length=255,unique= True,blank=False,null=False)
    api_key = models.CharField(max_length=255,unique=True,blank=False,null=False)
    backup_api_key = models.CharField(max_length=255,blank=False,null=False)
    app_name = models.CharField(max_length=255,blank=False,null=False)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20,blank=True,null=True)
    backend_language = models.CharField(max_length=200,blank=True,null=True)
    frontend_language = models.CharField(max_length=200,blank=True,null=True)
    host_link = models.CharField(max_length=255,blank=True,null=True)
    client = models.ForeignKey(client, on_delete=models.CASCADE,blank=True,null=True)
    deal_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return  self.app_uuid

class admin_logs(models.Model):
    request_url = models.CharField(max_length=512)
    method = models.CharField(max_length=10)
    operation_tag = models.CharField(max_length=15)
    response_code = models.IntegerField()
    details = models.CharField(max_length=512)
    user = models.CharField(max_length=255,default="default")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return (self.id)

class email_configuration(models.Model):
    email_host = models.CharField(max_length=256,blank=True,null=True)
    email_port = models.IntegerField(blank=True,null=True)
    email_from = models.CharField(max_length=256,blank=True,null=True)
    email_username = models.CharField(max_length=256,blank=True,null=True)
    email_password = models.CharField(max_length=256,blank=True,null=True)
    use_tls = models.BooleanField(blank=True,null=True)
    use_ssl = models.BooleanField(blank=True,null=True)
    fail_silently = models.BooleanField(blank=True,null=True)
    timeout = models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.email_username

class app_settings(models.Model):
    app_id = models.CharField(max_length=255,blank=True,null=True)
    api_key = models.CharField(max_length=255,blank=True,null=True)
    is_under_maintenance = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.id




