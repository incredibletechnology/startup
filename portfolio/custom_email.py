# Email Configuration modules
from django.core.mail import EmailMessage, EmailMultiAlternatives, get_connection, send_mail
from django.core.mail.backends.smtp import EmailBackend

from django.template.loader import render_to_string
from django.utils.html import strip_tags


from .models import *


def send_custom_email_to_admins(name,number,email,subject,message):
    user_data = User.objects.all()
    var = {
        'sender_name': name,
        'sender_email':email,
        'sender_phone': number,
        'sender_subject': subject,
        'sender_message': message,
    }

    to = []
    for i in user_data:
        to.append(i.email)
    # print(to)

    sub = "Messge from {}".format(name)
    # to = ['yeyec14465@bombaya.com']

    edata = email_configuration.objects.get(id=1)

    backend = EmailBackend(host=edata.email_host,port=edata.email_port,username=edata.email_username,password=edata.email_password,
                    use_tls=edata.use_tls,use_ssl=edata.use_ssl,fail_silently=edata.fail_silently)

    html_body = render_to_string('email/contact_us.html',{'var':var})
    text_body = strip_tags(html_body)

    email = EmailMultiAlternatives(
        sub,
        text_body,
        'bharatlvora814',
        to,
        connection=backend
    )
    email.attach_alternative(html_body,"text/html")
    # email.attach_file('Document.pdf')
    email.send()
    return True

def admin_password_reset(email):
    user_data = User.objects.get(email=email)
    slug = (email.split('@')[0])
    password = 'incredible@{}'.format(slug)
    # print("++++++++,",password,",+++++++")
    user_data.set_password(password)
    user_data.save()
    var = {
        'password':password,
        'username': user_data.username,
    }

    sub = "Password Reset Successfully"
    to = [email]

    edata = email_configuration.objects.get(id=1)

    backend = EmailBackend(host=edata.email_host,port=edata.email_port,username=edata.email_username,password=edata.email_password,
                    use_tls=edata.use_tls,use_ssl=edata.use_ssl,fail_silently=edata.fail_silently)

    html_body = render_to_string('email/password_reset.html',{'var':var})
    text_body = strip_tags(html_body)

    email = EmailMultiAlternatives(
        sub,
        text_body,
        'info.incredibletechnology@gmail.com',
        to,
        connection=backend
    )
    email.attach_alternative(html_body,"text/html")
    # email.attach_file('Document.pdf')
    email.send()
    return True