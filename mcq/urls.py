from django.contrib import admin
from django.urls import path
from pages import views
from test_submit.views import submit_data

urlpatterns = [
    path('admin/', admin.site.urls),					# Admin Panel
    path('questions/', views.questions_view, name='questionsView'),	# Questions Page View
    path('questions/api/', views.questions_api, name='questionsApi'),	# API for fetching Questions
    path('logout/', views.logout_request, name='logout'),		# Logout User
    path('', views.register_view, name='register'),			# Login page (Homepage)
    path('submit_data/', submit_data, name="submit_data"),		# Submit the test
    path('questions/sub/', submit_data, name="submit_data")		# Submit the test
]
