from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

# 首页
    path('landing/', views.landing, name='landing'), 
    
    path('creator_view/', views.creator_view, name='creator_view'),   
    
    path('player_view/', views.player_view, name='player_view'),  
    

# 个人相关
    path('create_studio/', views.create_studio, name='create_studio'),



    path('personal_page/<int:user_id>/', views.personal_page, name='personal_page'),
    
#评分功能

    path('studio_overview/', views.studio_overview, name='studio_overview'),
    path('studio/<int:studio_id>/rate/', views.rate_studio_page, name='rate_studio_page'),
    path('studio/<int:studio_id>/rate/submit', views.rate_studio, name='rate_studio'),



    
    path('studio_index', views.studio_index, name='studio_index'),
    path('studio/<int:pk>/upgrade/',views.upgrade_to_IOS, name='upgrade_to_IOS'),
    path('studio/<int:pk>/manage/', views.studio_manage, name='studio_manage'),

    path('studio_wallet_manage/<int:pk>/', views.studio_wallet_manage, name='studio_wallet_manage'),


    
    path('clear_data/', views.clear_data, name='clear_data'),
    path('initialize/', views.initialize, name='initialize'),
    path('initialize_sorter/', views.initialize_sorter, name='initialize_sorter'),
    
    
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
]

