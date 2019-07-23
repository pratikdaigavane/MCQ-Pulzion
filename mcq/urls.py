from django.contrib import admin
from django.urls import path
from pages import views
from test_submit.views import submit_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('loggedin/', views.loggedin_view, name='loggedin'),
    path('questions/', views.questions_view, name='questionsView'),
    path('questions/api/', views.questions_api, name='questionsApi'),
    path('logout/', views.logout_request, name='logout'),
    path('loggedout/', views.loggedout_view, name='loggedout'),
    path('', views.register_view, name='register'),
    path('submit_data/', submit_data, name="submit_data")
]
