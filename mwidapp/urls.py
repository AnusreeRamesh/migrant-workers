from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name="home"),
    path('about/', views.about , name="about"),
    path('contact/', views.contact , name="contact"),
    path('contact/', views.contact , name="contact"),
    path('authority_registration/', views.authority_registration , name="authority_registration"),
    path('login1/',views.login1,name='login1'),
    path('authority_base/',views.authority_base,name='authority_base'),
    path('logout1/',views.logout1,name='logout1'),
    path('authority_details/<str:name>', views.authority_details, name="authority_details"),
    path('authorityEdit/<int:id>',views.authorityEdit,name='authorityEdit'),


    path('user_base/',views.user_base,name='user_base'),
    path('user_registration/', views.user_registration , name="user_registration"),
    path('user_details/<str:name>', views.user_details, name="user_details"),
    path('userEdit/<int:id>',views.userEdit,name='userEdit'),
    path('submit_application/',views.submit_application, name='submit_application'),
    path('view_users/',views.view_users,name='view_users'),
    path('view_full_data/<str:name>',views.view_full_data,name='view_full_data'),
    path('approve_user/<str:name>',views.approve_user,name='approve_user'),
    path('reject_user/<str:name>',views.reject_user,name='reject_user'),
    path('approved_user_list/',views.approved_user_list,name='approved_user_list'),
    path('rejected_user_list/',views.rejected_user_list,name='rejected_user_list'),

    path('view_card/<int:pk>',views.view_card,name='view-card'),
    path('download_card/<str:name>',views.download_card,name='download_card'),
    path('download_noc/<str:name>',views.download_noc,name='download_noc')

    ]

