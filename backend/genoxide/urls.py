from django.urls import path
from . import views

urlpatterns = [
    path('gene/<str:gene_name>/', views.get_gene_data, name='get_gene_data'),
]
