from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import View
from blog.models import UserInfo
from blog import forms
from formtools.wizard.views import NamedUrlSessionWizardView


class InsidePage(TemplateView):
    template_name = 'blog/inside_page.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                self.request,
                'User not found'
            )
            return redirect(reverse('home_page'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object': self.request.user.userinfo,
        })
        return context


class LoginPageView(FormView):
    form_class = forms.LoginForm
    template_name = 'blog/login_page.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        user = User.objects.get(username=username)
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(self.request, user)
        return redirect(reverse('inside_page'))


class HomePage(TemplateView):
    template_name = 'blog/home_page.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('inside_page'))
        return super().dispatch(request, *args, **kwargs)


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(self.request)
        return redirect(reverse('home_page'))

class RegistrationRedirectionView(View):

    def dispatch(self, request, *args, **kwargs):
        if self.request.session.get('step'):
            return redirect(reverse('register_page', kwargs={'step': self.request.session.get('step')}))
        return redirect(reverse('register_page', kwargs={'step': 'step1'}))


class RegistrationPageView(NamedUrlSessionWizardView):
    template_name = 'blog/register.html'
    form_list = [
        ('step1', forms.Step1Form),
        ('step2', forms.Step2Form),
        ('step3', forms.Step3Form),
    ]
    step_titles = {
        'step1': (''),
        'step2': (''),
        'step3': (''),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        previous_url = ''
        if self.steps.current == 'step2':
            previous_url = reverse('register_page', kwargs={'step': 'step1'})
        if self.steps.current == 'step3':
            previous_url = reverse('register_page', kwargs={'step': 'step2'})
        context.update({
            'current_step': self.steps.current,
            'previous_url': previous_url,
        })
        return context

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('step3-username')
        password = self.request.POST.get('step3-password')
        confirm_password = self.request.POST.get('step3-confirm_password')
        if username and password and confirm_password:
            form = self.get_form(data=self.request.POST or None, files=self.request.FILES or None)
            if password != confirm_password:
                messages.error(
                    self.request,
                    'Password and Confirm Password does not match'
                )
                return self.render(form)
            if User.objects.filter(username=username).exists():
                messages.error(
                    self.request,
                    'Username already used'
                )
                return self.render(form)
        self.request.session['step'] = self.steps.next
        return super().post(request, *args, **kwargs)

    def done(self, form_list, form_dict, **kwargs):
        first_name = form_dict['step1'].cleaned_data['first_name']
        middle_name = form_dict['step1'].cleaned_data['middle_name']
        last_name = form_dict['step1'].cleaned_data['last_name']
        gender = form_dict['step2'].cleaned_data['gender']
        occupation = form_dict['step2'].cleaned_data['occupation']
        username = form_dict['step3'].cleaned_data['username']
        password = form_dict['step3'].cleaned_data['password']

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        UserInfo.objects.create(
            user=user,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            gender=gender,
            occupation=occupation,
        )
        if self.request.session.get('step'):
            del self.request.session['step']

        return redirect(reverse('login_page'))
