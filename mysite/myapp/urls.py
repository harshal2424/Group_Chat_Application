from django.urls import path
from .views import chat_view
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView
from .views import CustomLogoutView

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path



urlpatterns = [
    # Home chat page
    path('', chat_view, name='chat'),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
   # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout')
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),
    
    path('clear-chat/', views.clear_chat, name='clear_chat'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile_view, name='profile_view'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

