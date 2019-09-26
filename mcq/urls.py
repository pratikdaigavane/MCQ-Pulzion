from django.contrib import admin
from django.urls import path
from pages import views
from test_submit.views import submit_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('questions/', views.questions_view, name='questionsView'),
    path('questions/api/', views.questions_api, name='questionsApi'),
    path('logout/', views.logout_request, name='logout'),
    path('', views.register_view, name='register'),
    path('submit_data/', submit_data, name="submit_data"),
    path('questions/sub/', submit_data, name="submit_data")
]
