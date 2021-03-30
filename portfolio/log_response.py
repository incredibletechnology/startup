from .models import *

class Logs:
    def store_log(request_url,method,tag,code,details,useapi,user):
        pass
        # if not user:
        #     api_logs_data = api_logs.objects.create(request_url=request_url,method=method,operation_tag=tag,response_code=code,details=details,used_weather_api=useapi)
        # else:
        #     api_logs_data = api_logs.objects.create(request_url=request_url,method=method,operation_tag=tag,response_code=code,details=details,user=user,used_weather_api=useapi)

    def store_admin_log(request_url,method,tag,code,details,user):
        pass
        # if not user:
        #     admin_logs_data = admin_logs.objects.create(request_url=request_url,method=method,operation_tag=tag,response_code=code,details=details)
        # else:
        #     admin_logs_data = admin_logs.objects.create(request_url=request_url,method=method,operation_tag=tag,response_code=code,details=details,user=user)


