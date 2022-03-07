from django.urls import path
from user import views

urlpatterns = [
    path('login', views.authorization, name='login_page'),
    path('profile', views.profile, name='profile'),
    path('registration', views.registration, name='registration_page'),
    path('logout', views.logout_def, name='logout_page'),
    path('restore/<user_id>/<token>', views.restore, name='restore'),
    path('reset_password', views.reset_password, name='restore_page'),
    # # url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.profile_page, name='profile_page'),
    path('activate/<user_id>/<token>', views.verification_email, name='activate'),
    # path('profile/<username>', views.profile_page, name='profile_page'),
    # path('profile', views.all_profiles, name='all_profiles'),
]