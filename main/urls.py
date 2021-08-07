from django.urls import path

from main.views import ClientsListView, ClientDetailView, HistoryListView

urlpatterns = [
    path('history', HistoryListView.as_view()),
    path('clients', ClientsListView.as_view()),
    path('clients/<uuid:pk>', ClientDetailView.as_view()),
]