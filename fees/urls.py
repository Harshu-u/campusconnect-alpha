from django.urls import path
from . import views

urlpatterns = [
    # /fees/
    path('', views.fees_dashboard_view, name='fees'),
    
    # /fees/structure/
    path('structure/', views.fee_structure_list_view, name='fee_structure_list'),
    
    # /fees/structure/add/
    path('structure/add/', views.add_fee_structure_view, name='add_fee_structure'),
    
    # /fees/structure/edit/1/
    path('structure/edit/<int:pk>/', views.edit_fee_structure_view, name='edit_fee_structure'),
    
    # /fees/payment/add/1/ (Add payment for student ID 1)
    path('payment/add/<int:student_pk>/', views.add_payment_view, name='add_fee_payment'),
    
    # /fees/payment/edit/1/ (Edit payment ID 1)
    path('payment/edit/<int:pk>/', views.edit_payment_view, name='edit_fee_payment'),
]