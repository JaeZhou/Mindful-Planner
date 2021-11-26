from django import forms

from customers.models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)))

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
def clean(self):
        if 'password' in self.cleaned_data:
            p = Profile.objects.get(username__iexact=self.initial['username'])
            if not p.check_password(self.cleaned_data['password']):
                raise forms.ValidationError("Password is wrong.")
        return self.cleaned_data