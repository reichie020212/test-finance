from django import forms
from django.contrib.auth.models import User
from blog.models import UserInfo

class Step1Form(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = [
            'first_name',
            'middle_name',
            'last_name',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['middle_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'


class Step2Form(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = [
            'gender',
            'occupation',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['occupation'].widget.attrs['class'] = 'form-control'


class Step3Form(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Password',
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Confirm Password',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['confirm_password'].widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='',
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

    def clean(self):
        data = self.cleaned_data
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username=username):
            raise forms.ValidationError(('Username is not existing in our database'))

        user = User.objects.filter(username=username).first()

        if not user.check_password(password):
            raise forms.ValidationError(('Password incorrect'))

        return data
