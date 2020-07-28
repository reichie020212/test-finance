from django.conf.urls import url
from . import views

registration_page_url = views.RegistrationPageView.as_view(
    url_name='register_page',
    done_step_name='done',
)

urlpatterns = [
    url(r'^register/(?P<step>.+)/$', registration_page_url, name='register_page'),
    url(r'^register/$', views.RegistrationRedirectionView.as_view(), name='register_redirection'),
    url(r'^inside/$', views.InsidePage.as_view(), name='inside_page'),
    url(r'^logout/$', views.LogoutView.as_view(), name='account_logout'),
    url(r'^login/$', views.LoginPageView.as_view(), name='login_page'),
    url(r'', views.HomePage.as_view(), name='home_page'),
]
