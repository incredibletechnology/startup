from .models import *
from .log_response import Logs
from django.shortcuts import render, redirect

from rest_framework import status


class AdminCheckerMiddleware:
    def __init__(self, get_response):
        # print("Called __init___")
        self.get_response = get_response

    
    def __call__(self, request):
        response = self.get_response(request)

        path = request.get_full_path()
        # print("----|,",path)
        if path == '/' or path == '/about-us' or path=='/services' or path=='/contact-us' or path=='/submit-contact-form':
            setting = app_settings.objects.get(id=1)
            if not setting.is_under_maintenance:
                pass
            else:
                # Return App Is Under Maintanance Page
                return render(request, 'error/500_maintanence.html')
        else:
            if request.user.is_authenticated:
                pass
            elif request.get_full_path() == '/password/forgot/':
                pass
            else:
                return render(request, 'authentication/login.html')
        
        

        # device,touch_screen = 'No', 'None'
        # if request.user_agent.is_mobile:
        #     device = "Mobile"
        # elif request.user_agent.is_tablet:
        #     device = "Tablet"
        # elif request.user_agent.is_pc:
        #     device = "PC"
        # elif request.user_agent.is_bot:
        #     device = "BOT"
        # else:
        #     device = "None"
        # if request.user_agent.is_touch_capable:
        #     touch_screen = "YES"
        # print("Device - ",device)
        # print("Touch Capable - ",touch_screen)

        # Accessing user agent's browser attributes
        # brower_name = request.user_agent.browser.family
        # browser_version = request.user_agent.browser.version_string
        # print("Browser Info - ",brower_name, browser_version)

        # Operating System properties
        # os_family = request.user_agent.os.family
        # os_version = request.user_agent.os.version_string
        # print("OS - ",os_family,os_version)
        # print(request.POST['id'])
        
        # Device properties
        # device_family = request.user_agent.device.family
        # device_brand = request.user_agent.device.brand
        # device_model = request.user_agent.device.model
        # print("Family - ",device_family,device_brand,device_model)
        # Logs.store_log(request.get_full_path(),request.method,"error",204,"something wents wrong while fetching data",'')
        return response

