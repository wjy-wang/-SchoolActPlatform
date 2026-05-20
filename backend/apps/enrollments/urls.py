from django.urls import path
from .views import (
    EnrollmentListView,
    ActivityEnrollmentListView,
    EnrollmentCreateView,
    EnrollmentDeleteView
)

urlpatterns = [
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/create/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('enrollments/<int:pk>/', EnrollmentDeleteView.as_view(), name='enrollment-delete'),
    path('activities/<int:activity_id>/enrollments/', ActivityEnrollmentListView.as_view(), name='activity-enrollments'),
]
