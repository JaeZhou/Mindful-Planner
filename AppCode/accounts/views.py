from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_encode
from .forms import RegistrationForm
from .utils import PasswordGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your Mindful Planner Account!'
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': PasswordGenerator() 
    })


def register(request):
    args = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            form.save()
            send_activation_email() # sending the user an activation email
            return redirect('login')
        
    else: 
        form = RegistrationForm()
    
    args['form'] = form
    return render(request, 'registration/signup.html', args)