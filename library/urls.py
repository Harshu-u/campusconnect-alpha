from django.urls import path
from . import views

urlpatterns = [
    # /library/
    path('', views.library_dashboard_view, name='library'),
    
    # /library/books/
    path('books/', views.book_list_view, name='book_list'),
    
    # /library/books/add/
    path('books/add/', views.add_book_view, name='add_book'),
    
    # /library/books/edit/1/
    path('books/edit/<int:pk>/', views.edit_book_view, name='edit_book'),
    
    # /library/return/1/
    path('return/<int:pk>/', views.return_book_view, name='return_book'),
    
    # The 'issue_book' path has been removed, as that logic
    # is now handled by the dashboard view.
]