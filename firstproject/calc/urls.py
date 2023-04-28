from django.urls import path
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('add/', views.add, name='add'),
    path('delete/<int:Aadhar>', views.delete, name='delete'),
    path('update/<int:Aadhar>', views.update, name='update'),
    path('do-update/<int:Aadhar>', views.doupdate, name='doupdate'),
    path('TrL/', views.TravellerList.as_view(), name='TrL'),
    path('TrL/<int:pk>', views.Traveller_detail.as_view(), name='TrL'),
    path('users/', views.UserList.as_view(),name='users'),
    path('users/<int:pk>/', views.UserDetail.as_view(),name='users'),
    path('upload/', views.upload_file,name='upload'),
    path('search/', views.search,name='search'),
    path('register/',views.authsignup,name='authsignup'),
    path('login/',views.authlogin,name='authlogin'),
    path('authsignup/',views.authsignup,name='authsignup'),
    path('authlogin/',views.authlogin,name='authlogin'),
    path('verify/<auth_token>/',views.verify,name='verify'),
    path('token_send/',views.token_send,name='token_send'),
]
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
 urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)