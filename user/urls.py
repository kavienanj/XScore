from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', user_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',
                                                redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/login.html', extra_context={
        'status': 'Successfully Logged Out, Come back again to Explore more! '
    }), name='logout'),
]
