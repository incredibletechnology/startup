from django.contrib import admin
from django.urls import path
from . import views
from . import webviews

from django.conf.urls import handler404, handler500

urlpatterns = [
    path('',views.index, name="index"),
    path('about-us',views.about_us, name="about-us"),
    path('services',views.services, name="services"),
    path('contact-us',views.contact_us_page, name="contact-us"),
    path('submit-contact-form',views.submit_contact_form,name="submit-contact-form"),
    
    ##### Authentication #####
    path('login/', webviews.login, name="login"),
    path('logout/', webviews.logout, name="logout"),
    path('password/forgot/', webviews.forgot, name="forgot"),
    path('view-profile', webviews.view_profile, name="view-profile"),
    path('admin-panel', webviews.admin_panel, name="admin-panel"),
    path('add-user', webviews.add_user, name="add-user"),
    path('get-user', webviews.get_user, name="get-user"),
    path('adminindex',webviews.adminindex, name="adminindex"),

    ##### Settings #####
    path('settings', webviews.settings, name="settings"),
    path('update-email-configuration', webviews.update_email_configuration, name="update-email-configuration"),
    path('update-app-detail',webviews.update_app_detail, name="update-app-detail"),
    path('update-maintenance',webviews.update_maintenance, name="update-maintenance"),

    ##### Logs Section #####
    # path('get-logs',webviews.get_logs, name="get-logs"),
    # path('get-admin-logs',webviews.get_admin_logs, name="get-admin-logs"),
    # path('filter-logs',webviews.filter_logs, name="filter-logs"),
    # path('filter-admin-logs',webviews.filter_admin_logs, name="filter-admin-logs"),
    # path('export-api-log',webviews.export_api_log, name="export-api-log"),
    # path('export-admin-log',webviews.export_admin_log, name="export-admin-log"),

    ##### Ajax Request #####
    # path('find-app-api',webviews.find_app_api, name="find-app-api"),
    # path('month-wise-request',webviews.month_wise_request, name="month-wise-request"),

    ##### App Details Section #####
    path('get-app',webviews.get_app, name="get-app"),
    path('add-app',webviews.add_app, name="add-app"),
    path('update-app',webviews.update_app, name="update-app"),
    path('delete-app',webviews.delete_app, name="delete-app"),
    path('reset-api-key',webviews.reset_api_key, name="reset-api-key"),

    ##### Client Section #####
    path('get-clients',webviews.get_clients, name="get-clients"),
    path('add-client',webviews.add_client, name="add-client"),
    path('update-client',webviews.update_client, name="update-client"),
    path('delete-client',webviews.delete_client, name="delete-client"),
    # path('reset-api-key',webviews.reset_api_key, name="reset-api-key"),
]

handler404 = 'portfolio.views.handler404'
handler500 = 'portfolio.views.handler500'
handler403 = 'portfolio.views.handler403'
