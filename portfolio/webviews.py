from django.shortcuts import render, redirect
from .models import *
# from .custom_response import Custom
# from .serializers import *
from startup.settings import *
from .custom_email import *

import json
import datetime
from datetime import timedelta
from datetime import datetime
from django.utils import timezone
import random
import string
import csv

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view 
from rest_framework import status
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.models import User,auth

from django.views.decorators.csrf import csrf_exempt

# Email Configuration modules
from django.core.mail import EmailMessage, EmailMultiAlternatives, get_connection, send_mail
from django.core.mail.backends.smtp import EmailBackend

#Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .log_response import Logs

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required 

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

def adminindex(request):
    user = request.user
    if request.method == 'GET':
        client_count = client.objects.all().count()
        taken = app_master.objects.filter(status='Taken').count()
        ongoing = app_master.objects.filter(status='Onging').count()
        completed = app_master.objects.filter(status='Completed').count()
        app_data = app_master.objects.all()

        var = {
            'taken':taken,
            'ongoing': ongoing,
            'completed': completed,
            'client_count':client_count,
            'app_data':app_data,
            'is_photo': False if user.image == '' else True,
            'nbar': 'home',
        }
        # Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"display all weather data.",user)
        return render(request, 'index.html',var)

#################### Authentication Section ####################

def login(request):
    if request.method == 'GET':
        # Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"Login page",'')
        return render(request, 'authentication/login.html')

    elif request.method == 'POST':
        uemail = request.POST['email']
        upass1 = request.POST['password']
        remember = request.POST.get('remember',False)
        # print(uemail,upass1,remember)

        User = get_user_model()
        if User.objects.filter(email=uemail).exists() or User.objects.filter(username=uemail).exists():
            if User.objects.filter(email=uemail).exists():
                user_data = User.objects.get(email=uemail)
                user = auth.authenticate(username=user_data.username, password=upass1)
                # print("222",user)
            else:
                user = auth.authenticate(username=uemail, password=upass1)
                
            if user is not None:
                auth.login(request,user)
                if remember:
                    request.session.set_expiry(604800)
                else:
                    request.session.set_expiry(10800)
                Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"user ({}) login successfully.".format(user),user)
                return redirect('adminindex')
                #return redirect(request.GET.get('next'))
                #return redirect('index')
            else:
                # Logs.store_admin_log(request.get_full_path(),request.method,"error",400,"entered wrong password",'')
                messages.error(request, "Kindly check your password.")
                return redirect('login')
        else:
            # Logs.store_admin_log(request.get_full_path(),request.method,"error",404,"email id not found in database.",'')
            messages.error(request, "Email Id/Username does not found in Database.")
            return redirect('login')

def logout(request):
    user = request.user
    Logs.store_admin_log(request.get_full_path(),request.method,"success",200," user ({}) logout successfully".format(user),user)
    auth.logout(request)
    # time.sleep(1.000)
    return redirect('login')

def forgot(request):
    if request.method == 'GET':
        return render(request, 'authentication/forget_password.html')
    else:
        user_email = request.POST['uemail']
        if User.objects.filter(email=user_email).exists():
            send = admin_password_reset(user_email)
        else:
            Logs.store_admin_log(request.get_full_path(),request.method,"error",404,"email id not found in database",'')
            messages.info(request,"Email '"+user_email+"' is not found in database.")
            return redirect('forgot')
        messages.success(request, "Email sent successfully")
        return redirect('forgot')

#################### Admin Activity Section ####################

def admin_panel(request):
    user = request.user
    Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"visit Django Admin Panel",user)
    return redirect('/admin/')

def add_user(request):
    user = request.user
    if request.method == 'GET':
        var = {
            'is_photo': False if user.image == '' else True,
            'nbar': 'adduser',
        }
        Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"add user page.",user)
        return render(request, 'authentication/add_user.html',var)
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        role = request.POST['role']
        try:
            photo = request.FILES['photo']
        except:
            pass
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if pass1 == pass2:
            superuser, staff = False, False
            if role == '2':
                staff = True
            elif role == '3':
                superuser = True
                staff = True
            user = User.objects.create_user(password=pass1,username=username,email=email,is_staff=staff,is_superuser=superuser)
            user.save()
            Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"user ({}) added successfully".format(email),user)
            messages.success(request, "user added successfully")
            return redirect('add-user')
        else:
            Logs.store_admin_log(request.get_full_path(),request.method,"error",400,"password not match while adding user ({})".format(email),user)
            messages.error(request,"password not match.")
            return redirect('add-user')

def get_user(request):
    user = request.user
    if request.method == 'GET':
        server_user = User.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(server_user,10)
        try:
            userlist = paginator.page(page)
        except PageNotAnInteger:
            userlist = paginator.page(1)
        except EmptyPage:
            userlist = paginator.page(paginator.num_pages)
        var = {
            'userlist':userlist,
            'is_photo': False if user.image == '' else True,
            'nbar': 'getuser',
        }
        return render(request, 'user/get_users.html',var)

def view_profile(request):
    user = request.user
    if request.method == 'GET':
        var = {
            'is_photo': False if user.image == '' else True,
        }
        Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"view profile page",user)
        return render(request, 'authentication/view_profile.html',var)
    elif request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        is_change = request.POST.get('is_change',False)
        user = User.objects.get(email=email)
        user.first_name = fname
        user.last_name = lname
        try:
            photo = request.FILES['photo']
            # print(photo)
            user.image = photo
        except:
            pass
        if is_change:
            pass1 = request.POST['password1']
            pass2 = request.POST['password2']
            if pass1 == pass2:
                user.set_password(pass1)
                user.save()
                Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"profile updated successfully",user)
                messages.success(request, "profile updated successfully")
                return redirect('view-profile')
            else:
                Logs.store_admin_log(request.get_full_path(),request.method,"error",400,"password not match.",user)
                messages.error(request,"password not match.")
                return redirect('view-profile')
        else:
            user.save()
            Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"profile updated successfully",user)
            messages.success(request, "profile updated successfully")
            return redirect('view-profile')

def get_admin_logs(request):
    user = request.user
    log_data = admin_logs.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(log_data,10)
    try:
        loglist = paginator.page(page)
    except PageNotAnInteger:
        loglist = paginator.page(1)
    except EmptyPage:
        loglist = paginator.page(paginator.num_pages)

    var = {
        'loglist':loglist,
        'log_data':log_data,
        'is_photo': False if user.image == '' else True,
        'nbar': 'adminlog',
    }
    Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"display admin logs.",user)
    return render(request, 'logs/admin_logs.html',var)

def filter_admin_logs(request):
    user = request.user
    if request.method == 'GET':
        current, time_threshold,time_name,time = '', '','', ''

        property_name = request.GET['property'] if request.GET['property'] != '' else 'None'
        from_date = request.GET['from'] if request.GET['from'] != '' else 'None'
        to_date = request.GET['to'] if request.GET['to'] != '' else 'None'
        # time = request.GET['time'] if request.GET['time'] != '' else 'None'

        if (from_date != 'None' and to_date == 'None') or (from_date == 'None' and to_date != 'None'):
            messages.info(request, 'Valid From and To date required.')
            return redirect('get-admin-logs')

        # print(datetime.now())
        if property_name != 'None' and from_date != 'None':
            time_name = 'time'
            log_data = admin_logs.objects.filter(method=property_name,created_at__range=[from_date,to_date])
        elif property_name != 'None' and from_date == 'None':
            log_data = admin_logs.objects.filter(method=property_name)
        elif property_name == 'None' and from_date != 'None':
            time_name = 'time'
            log_data = admin_logs.objects.filter(created_at__range=[from_date, to_date])
        else:
            messages.info(request, 'Please choose at least one filter parameter.')
            return redirect('get-admin-logs')

        page = request.GET.get('page', 1)
        paginator = Paginator(log_data,15)
        try:
            loglist = paginator.page(page)
        except PageNotAnInteger:
            loglist = paginator.page(1)
        except EmptyPage:
            loglist = paginator.page(paginator.num_pages)
        var = {
            'loglist':loglist,
            'log_data':log_data,
            'is_photo': False if user.image == '' else True,
            'nbar': 'adminlog',
            'current': current,
            'time_threshold': time_threshold,
            'property_name':property_name,
            'time_name': time_name,
            'from_date':from_date,
            'to_date':to_date,
            'result': 'yes',
        }
        Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"filtered admin logs.",user)
        return render(request, 'logs/admin_logs.html',var)

def month_wise_request(request):
    if request.method == 'GET':
        monthly_get_request = []
        monthly_post_request = []
        monthly_put_request = []
        monthly_delete_request = []

        for count in range(1,13):
            
            if count <= 9:
                count = "0{}".format(count)
            else:
                pass
            api_log_data = api_logs.objects.filter(method='GET')
            jan = 0
            for i in api_log_data:
                month = (i.created_at).strftime('%m')
                if month == count:
                    jan += 1
            monthly_get_request.append(jan)

            api_log_data = api_logs.objects.filter(method='POST')
            jan = 0
            for i in api_log_data:
                month = (i.created_at).strftime('%m')
                if month == count:
                    jan += 1
            monthly_post_request.append(jan)

            api_log_data = api_logs.objects.filter(method='PUT')
            jan = 0
            for i in api_log_data:
                month = (i.created_at).strftime('%m')
                if month == count:
                    jan += 1
            monthly_put_request.append(jan)

            api_log_data = api_logs.objects.filter(method='DELETE')
            jan = 0
            for i in api_log_data:
                month = (i.created_at).strftime('%m')
                if month == count:
                    jan += 1
            monthly_delete_request.append(jan)


        # print("GET-",monthly_get_request)
        # print("POST-",monthly_post_request)
        # print("PUT-",monthly_put_request)
        # print("DELETE-",monthly_delete_request)
        var = {
            'get':monthly_get_request,
            'post':monthly_post_request,
            'put':monthly_put_request,
            'delete': monthly_delete_request,
        }
        return JsonResponse(var)

def find_app_api(request):
    if request.method == 'GET':
        app_data = app_master.objects.all()
        log_data = api_logs.objects.all()
        final = []
        for app in app_data:
            temp,local,weather = [],0,0
            location_data = location_master.objects.filter(app_master=app)
            count = 0
            for loc in location_data:
                count += 1
            for log in log_data:
                request_url = log.request_url
                appid = (request_url.split('&')[2]).split('=')[1]
                if app.app_uuid == appid:
                    used_weather_api = log.used_weather_api
                    if used_weather_api:
                        weather += 1
                    else:
                        local += 1
            # print("Weather API - ",weather,"LOCAL - ",local)
            app_uuid = app.app_uuid
            name = app.app_name
            total_count = count
            temp.append(app_uuid)
            temp.append(name)
            temp.append(total_count)
            temp.append(weather)
            temp.append(local)
            final.append(temp)
        return JsonResponse(final, safe=False)

def send_custom_email_to_admins(request):
    user_data = User.objects.all()
    var = {
        'u':udata,
    }
    to = ['jetivak413@lidte.com']

    edata = email_configuration.objects.get(id=1)
    print("Before Backend")
    backend = EmailBackend(host=edata.email_host,port=edata.email_port,username=edata.email_username,password=edata.email_password,
                    use_tls=edata.use_tls,use_ssl=edata.use_ssl,fail_silently=edata.fail_silently)
    print("After Backend")
    html_body = render_to_string('email/contact_us.html',{'var':var})
    text_body = strip_tags(html_body)

    email = EmailMultiAlternatives(
        "Just for Testing - 2",
        text_body,
        'bharatlvora814',
        to,
        connection=backend
    )
    email.attach_alternative(html_body,"text/html")
    # email.attach_file('Document.pdf')
    email.send()
    return True


#################### Settings Section ####################

def settings(request):
    user = request.user
    if request.method == 'GET':

        tls_style, ssl_style, fs_style,edata = '', '', '', ''
        try:
            edata = email_configuration.objects.get(id=1)
            if edata.use_tls == True:
                tls_style = "checked"
            if edata.use_ssl == True:
                ssl_style = "checked"
            if edata.fail_silently == True:
                fs_style = "checked"
            
        except:
            pass
        setting, maintenance_style = '', ''
        
        try:
            setting = app_settings.objects.get(id=1)
            if setting.is_under_maintenance == True:
                maintenance_style = "checked"
            
        except:
            pass

        var = {
            'is_photo': False if user.image == '' else True,
            'nbar': 'setting',
            'edata':edata,
            'tls_style':tls_style,
            'ssl_style':ssl_style,
            'fs_style': fs_style,
            'setting': setting,
            'maintenance_style': maintenance_style,
        }
        Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"settings list page.",user)
        return render(request, 'authentication/settings.html',var)

def update_email_configuration(request):
    user = request.user
    if request.method == 'POST':
        ehost = request.POST['ehost']
        eport = request.POST['eport']
        efrom = request.POST['efrom']
        eusername = request.POST['eusername']
        epassword = request.POST['epassword']
        use_tls = request.POST.get('tls',False)
        use_ssl = request.POST.get('ssl',False)
        fail_silently = request.POST.get('fail_silently',False)
        timeout = request.POST['etimeout'] if request.POST['etimeout'] != '' else 0.0

        print(ehost,eport,efrom,eusername,epassword,use_tls,use_ssl,fail_silently,timeout)

        try:
            edata = email_configuration.objects.get(id=1)
        except:
            if email_configuration.objects.all().count() < 1:
                edata = email_configuration.objects.create(email_host=ehost,email_port=eport,email_from=efrom,email_username=eusername,
                        email_password=epassword,use_tls=use_tls,use_ssl=use_ssl,fail_silently=fail_silently,timeout=timeout)
                edata.save()
                Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"email configuration created successfully.",user)
                messages.success(request, 'Email Configuration created successfully.')
                return redirect('settings')
            else:
                Logs.store_admin_log(request.get_full_path(),request.method,"error",500,"multiple entry of email table in database",user)
                messages.error(request, 'Found Multiple Entry of Email Table in Database.')
                return redirect('settings')

        edata.email_host = ehost
        edata.email_port = eport
        edata.email_from = efrom
        edata.email_username = eusername
        edata.email_password = epassword
        edata.use_tls = use_tls
        edata.use_ssl = use_ssl
        edata.fail_silently = fail_silently
        edata.timeout = timeout
        edata.save()
        Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"email configuration updated successfully.",user)
        messages.success(request, 'Email Configuration updated successfully.')
        return redirect('settings')

def update_app_detail(request):
    user = request.user
    if request.method == 'POST':
        app_id = request.POST['app_id']
        api_key = request.POST['api_key']
        # print(freeuser,prouser)

        try:
            setting = app_settings.objects.get(id=1)
            setting.app_id = app_id
            setting.api_key = api_key
            setting.save()
        except:
            if app_settings.objects.all().count() < 1:
                setting = app_settings.objects.create(app_id=app_id,api_key=api_key)
                setting.save()
            else:
                Logs.store_admin_log(request.get_full_path(),request.method,"error",500,"multiple entry of email table in database",user)
                messages.error(request, 'Found Multiple Entry in Settings Table in Database.')
                return redirect('settings')
        
        Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"App Details updated successfully.",user)
        messages.success(request, 'App Details updated successfully.')
        return redirect('settings')

def update_maintenance(request):
    user = request.user
    if request.method == 'POST':
        maintenance = request.POST.get('maintenance',False)

        try:
            setting = app_settings.objects.get(id=1)
            setting.is_under_maintenance = maintenance
            setting.save()
        except:
            if app_settings.objects.all().count() < 1:
                setting = app_settings.objects.create(is_under_maintenance=maintenance)
                setting.save()
            else:
                Logs.store_admin_log(request.get_full_path(),request.method,"error",500,"multiple entry of email table in database",user)
                messages.error(request, 'Found Multiple Entry in Settings Table in Database.')
                return redirect('settings')
        if maintenance:
            Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"Application is under maintenance now.",user)
            messages.success(request, 'Application is under maintenance now.')
        else:
            Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"Application is live now.",user)
            messages.success(request, 'Application is live now.')
        return redirect('settings')



#################### Application Section ##################

def get_random_app_id():
    current_year = datetime.now().year
    # choose from [0-9] and [A-Z]
    letters = string.ascii_uppercase + string.digits
    result_str1 = ''.join(random.choice(letters) for i in range(4))
    result_str2 = ''.join(random.choice(letters) for i in range(4))
    app_id = '{}-{}-{}'.format(current_year,result_str1,result_str2)
    return app_id

def get_random_api_key():
    # choose from [0-9], [a-z] and [A-Z]
    letters = string.ascii_uppercase + string.digits + string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(12))
    api_key = 'key_{}'.format(result_str)
    return api_key

def get_app(request):
    user = request.user
    if request.method == 'GET':
        app_data = app_master.objects.all()

        var = {
            'app_data':app_data,
            'is_photo': False if user.image == '' else True,
            'nbar': 'appdetails',
        }
        return render(request, 'app/get_app.html',var)

def add_app(request):
    user = request.user
    if request.method == 'GET':

        getRandomId = get_random_app_id()
        getRandomAPI = get_random_api_key()
        app_data = app_master.objects.all()
        if app_master.objects.filter(app_uuid=getRandomId).exists():
            return redirect('add-app')
        else:
            if app_master.objects.filter(api_key=getRandomAPI).exists():
                return redirect('add-app')
            else:
                clientlist = client.objects.all()
                var = {
                    'app_id': getRandomId,
                    'api_key': getRandomAPI,
                    'app_data':app_data,
                    'userlist': User.objects.all(),
                    'clientlist': clientlist,
                    'is_photo': False if user.image == '' else True,
                    'nbar': 'appdetails',
                }
                Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"add app page",user)
                return render(request, 'app/add_app.html',var)

    elif request.method == 'POST':
        api_key = request.POST['api_key']
        # backup_api_key = api_key
        app_id = request.POST['app_id']
        app_name = request.POST['app_name']
        backup_api_key = request.POST['backup_api_key']
        deal_by = request.POST['deal_by']
        cemail = request.POST['client']
        frontend = request.POST['frontend']
        backend = request.POST['backend']
        host_link = request.POST['host_link']
        astatus = request.POST['status']
        is_active = request.POST.get('is_active',False)

        try:
            user_data = User.objects.get(username=deal_by)
            client_data = client.objects.get(email=cemail)
            app_data = app_master.objects.create(app_uuid=app_id,api_key=api_key,app_name=app_name,backup_api_key=backup_api_key,is_active=is_active,
                        deal_by=user_data,client=client_data,status=astatus,frontend_language=frontend,backend_language=backend,host_link=host_link)
            app_data.save()
        except:
            # Logs.store_admin_log(request.get_full_path(),request.method,"error",500,"Something wents wrong. Please try again.",user)
            messages.error(request, 'Something wents wrong. Please try again.')
            return redirect('add-app')

        # Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"App added successfully",user)
        messages.success(request, 'App added successfully')
        return redirect('get-app')

def update_app(request):
    user = request.user
    if request.method == 'GET':
        id = request.GET['id']
        app_data = app_master.objects.get(id=id)

        active_style = 'checked' if app_data.is_active else ''
        taken = 'selected' if app_data.status == 'Taken' else ''
        onging = 'selected' if app_data.status == 'Onging' else ''
        completed = 'selected' if app_data.status == 'Completed' else ''
        var = {
            'app_data':app_data,
            'taken':taken,
            'onging': onging,
            'completed': completed,
            'is_photo': False if user.image == '' else True,
            'nbar': 'appdetails',
            'active_style':active_style,
        }
        Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"update app ({}) page".format(app_data.app_name),user)
        return render(request, 'app/update_app.html',var)

    elif request.method == 'POST':
        api_key = request.POST['api_key']
        # backup_api_key = api_key
        app_id = request.POST['app_id']
        app_name = request.POST['app_name']
        deal_by = request.POST['deal_by']
        cemail = request.POST['client']
        frontend = request.POST['frontend']
        backend = request.POST['backend']
        host_link = request.POST['host_link']
        is_active = request.POST.get('is_active',False)
        astatus = request.POST['status']
        id = request.POST['aid']

        try:
            user_data = User.objects.get(username=deal_by)
            client_data = client.objects.get(email=cemail)
            app_data = app_master.objects.get(id=id)
            app_data.app_uuid=app_id
            app_data.api_key=api_key
            app_data.app_name=app_name
            app_data.is_active=is_active
            app_data.deal_by = user_data
            app_data.client = client_data
            app_data.frontend_language = frontend
            app_data.backend_language = backend
            app_data.host_link = host_link
            app_data.status = astatus
            app_data.save()
        except:
            Logs.store_admin_log(request.get_full_path(),request.method,"error",500,"Something wents wrong. Please try again.",user)
            messages.error(request, 'Something wents wrong. Please try again.')
            return redirect(request.get_full_path())

        Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"App added successfully",user)
        messages.success(request, 'App ({}) updated successfully'.format(app_name))
        return redirect('get-app')

def delete_app(request):
    user = request.user
    id = request.GET['id']
    app_data = app_master.objects.get(id=id)
    name = app_data.app_name
    try:
        app_data.delete()
        Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"App ({}) deleted successfully".format(name),user)
        messages.success(request, 'App ({}) deleted successfully'.format(name))
        return redirect('get-app')
    except:
        Logs.store_admin_log(request.get_full_path(),request.method,"error",500,"Something wents wrong. Please try again.",user)
        messages.error(request, 'Something wents wrong. Please try again.')
        return redirect('get-app')

@csrf_exempt
def reset_api_key(request):
    user = request.user
    print("111")
    if request.method == 'POST':

        id = request.POST['id']
        print("tt",id)
        getRandomAPI = get_random_api_key()
        app_data = app_master.objects.all()
        if app_master.objects.filter(api_key=getRandomAPI).exists():
            return redirect('reset-api-key')
        else:
            # app_data = app_master.objects.get(id=id)
            # app_data.api_key = getRandomAPI
            # app_data.save()
            print("CHANGE")
            Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"API key reset successfully",user)
            # messages.success(request, 'API key reset successfully')
            return JsonResponse(getRandomAPI,safe=False)

################## Client Section #########################

def get_clients(request):
    user = request.user
    if request.method == 'GET':
        clientlist = client.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(clientlist,10)
        try:
            clientlist = paginator.page(page)
        except PageNotAnInteger:
            clientlist = paginator.page(1)
        except EmptyPage:
            clientlist = paginator.page(paginator.num_pages)

        var = {
            'clientlist':clientlist,
            'is_photo': False if user.image == '' else True,
            'nbar': 'getclients',
        }
        return render(request, 'clients/get_clients.html',var)

def add_client(request):
    user = request.user
    if request.method == 'GET':
        var = {
            'is_photo': False if user.image == '' else True,
            'nbar': 'getclients',
        }
        return render(request, 'clients/add_client.html',var)
    elif request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        company = request.POST['company']
        address = request.POST['address']
        remark = request.POST['remark']
        try:
            photo = request.FILES['photo']
        except:
            photo = ''
        if client.objects.filter(email=email).exists():
            messages.error(request,'Client with email {} already exists.'.format(email))
            return redirect(request.get_full_path())
        else:
            client_data = client.objects.create(name=name,email=email,phone=phone,company=company,address=address,
                        remark=remark,image=photo)
            client_data.save()
            messages.success(request,'Client added successfully.')
            return redirect('get-clients')

def update_client(request):
    user = request.user
    if request.method == 'GET':
        id = request.GET['id']
        client_data = client.objects.get(id=id)
        var = {
            'client_data': client_data,
            'is_photo': False if user.image == '' else True,
            'nbar': 'getclients',
        }
        return render(request, 'clients/update_client.html',var)
    elif request.method == 'POST':
        id = request.POST['cid']
        client_data = client.objects.get(id=id)
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        company = request.POST['company']
        address = request.POST['address']
        remark = request.POST['remark']
        try:
            photo = request.FILES['photo']
        except:
            photo = ''

        if client_data.image:
            if photo != '':
                client_data.image = photo
            else:
                pass
        else:
            if photo != '':
                client_data.image = photo
            else:
                pass

        if email == client_data.email:
            pass
        else:
            if client.objects.filter(email=email).exists():
                messages.error(request,'Client with email {} already exists.'.format(email))
                return redirect(request.get_full_path())
        client_data.name = name
        client_data.email = email
        client_data.phone = phone
        client_data.company = company
        client_data.address = address
        client_data.remark = remark
        client_data.save()
        messages.success(request,'Client updated successfully.')
        return redirect(request.get_full_path())

def delete_client(request):
    user = request.user
    id = request.GET['id']
    client_data = client.objects.get(id=id)
    name = client_data.name
    try:
        client_data.delete()
        # Logs.store_admin_log(request.get_full_path(),request.method,"success",200,"App ({}) deleted successfully".format(name),user)
        messages.success(request, 'Client ({}) deleted successfully'.format(name))
        return redirect('get-clients')
    except:
        # Logs.store_admin_log(request.get_full_path(),request.method,"error",500,"Something wents wrong. Please try again.",user)
        messages.error(request, 'Something wents wrong. Please try again.')
        return redirect('get-clients')

################## Export in CSV ##########################

def export_api_log(request):
    user = request.user
    if request.method == 'GET':
        current, time_threshold,time_name,time = '', '','', ''

        property_name = request.GET['property'] if request.GET['property'] != '' else 'None'
        from_date = request.GET['from'] if request.GET['from'] != '' else 'None'
        to_date = request.GET['to'] if request.GET['to'] != '' else 'None'
        # time = request.GET['time'] if request.GET['time'] != '' else 'None'

        if (from_date != 'None' and to_date == 'None') or (from_date == 'None' and to_date != 'None'):
            messages.info(request, 'Valid From and To date required.')
            return redirect('get-logs')

        print(datetime.now())
        if property_name != 'None' and from_date != 'None':
            time_name = 'time'
            log_data = api_logs.objects.filter(method=property_name,created_at__range=[from_date,to_date])
        elif property_name != 'None' and from_date == 'None':
            log_data = api_logs.objects.filter(method=property_name)
        elif property_name == 'None' and from_date != 'None':
            time_name = 'time'
            log_data = api_logs.objects.filter(created_at__range=[from_date, to_date])
        else:
            export_data = api_logs.objects.all()

        date = datetime.now().strftime('%d-%m-%Y')
        exportof = "{}_API Logs".format(date)
        file_name = "{}.csv".format(exportof)
        response = HttpResponse(content_type='text/csv')  
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)  
        writer = csv.writer(response)
        try:
            name = 'API Logs'
            export_data = export_data
            writer.writerow(['id','request_url','method','operation_tag','used_weather_api','response_code','details','user','created_at','updated_at','deleted_at'])
            for i in export_data:
                writer.writerow([i.id,i.request_url,i.method,i.operation_tag,i.used_weather_api,i.response_code,i.details,i.user,i.created_at,i.updated_at,i.deleted_at])
        except:
            messages.error(request, 'Something wents wrong while exporting.')
            return redirect('get-logs')
      
        return response


