from django.core.checks import messages
from accounts.models import User
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import RegistrationForm
from .utils import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
import threading

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your Mindful Planner Account!'
    email_body = render_to_string('registration/activation.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email=EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    EmailThread(email).start()

# Making sending the verification email into its own thread so the user doesn't have to wait around
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()


def register(request):
    args = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            send_activation_email(user, request)
            return redirect('login')
        
    else: 
        form = RegistrationForm()
    
    args['form'] = form
    return render(request, 'registration/signup.html', args)

def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None
    
    if user and generate_token.check_token(user, token):
        user.email_verified = True
        user.save()

        #messages.add_message(request, messages.SUCCESS, 'Email successfully verified!')
        return redirect(reverse('login'))
    
    return render(request, 'registration/activation-failed.html', {"user":user})
    