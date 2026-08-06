from django.urls import path
from .views import (
    ActivityListView,
    ActivityDetailView,
    ActivityCreateView,
    ActivityUpdateView,
    ActivityDeleteView,
    ActivityBulkUpdateView,
    MyActivitiesView
)

urlpatterns = [
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('activities/my/', MyActivitiesView.as_view(), name='my-activities'),
    path('activities/create/', ActivityCreateView.as_view(), name='activity-create'),
    path('activities/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('activities/<int:pk>/update/', ActivityUpdateView.as_view(), name='activity-update'),
    path('activities/<int:pk>/delete/', ActivityDeleteView.as_view(), name='activity-delete'),
    path('activities/bulk-update/', ActivityBulkUpdateView.as_view(), name='activity-bulk-update'),
]
