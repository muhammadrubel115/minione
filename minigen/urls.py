from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# all imoprt for urls are here
from django.urls import path

from django.urls import path
from minigen import views

# Write urls for minigen here !!

urlpatterns = [
    path('', views.Mini, name="mini"),
    path('home/', views.Home, name="home"),
    path('postmcq/', views.Postmcqview, name="postmcq"),
    
    path('notification/', views.Notification, name="notification"),
    path('search/', views.Search, name="search"),
    path('profile/', views.Profile, name="profile"),
    
    path('profile_view/<str:username>/', views.profile_view, name='profile_view'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),

    path('support/', views.Support, name="support"),
    path('settings/', views.Settings, name="settings"),

    



    path('logout/', views.logout_view, name='logout'),
    path('change_username/', views.Change_username, name='change_username'),

    path('change_account_name/', views.Change_acc_name, name='change_account_name'),
    path('change_email/', views.Change_email, name='change_email'),

    path('change_remail/', views.Change_remail, name='change_remail'),
    path('change_password/', views.Change_password, name='change_password'),
    path('change_profile_picture/', views.ChangeProfilePicture, name='change_profile_picture'),
    path('change_bio/', views.ChangeBio, name='change_bio'),
    path('change_account_category/', views.ChangeAccountCategory, name='change_account_category'),
    path('update_country/', views.UpdateCountry, name='update_country'),
    path('change_gender/', views.ChangeGender, name='change_gender'),
    path('change_dob/', views.ChangeDOB, name='change_dob'),
    path('change_phone_number/', views.ChangePhoneNumber, name='change_phone_number'),
    path('edit_profile/', views.Edit_Profile, name="edit_profile"),
   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)