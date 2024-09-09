# library/urls.py

from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from .views import member_dashboard, purchase_book

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home_redirect'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('librarian/', views.librarian_dashboard, name='librarian_dashboard'),
    path('member/', views.member_dashboard, name='member_dashboard'),

    # User management
    path('users/', views.manage_users, name='manage_users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    # Librarian management
    path('librarian/dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('librarian/add_book/', views.add_book, name='add_book'),
    path('librarian/edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('librarian/delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('admin/manage_books/', views.admin_manage_books, name='admin_manage_books'),

    # Book management
    path('books/', views.manage_books, name='manage_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),

    # Registration
    path('register/', views.user_register, name='register'),
    
    path('dashboard/', member_dashboard, name='member_dashboard'),
    path('purchase/<int:book_id>/<str:purchase_type>/', purchase_book, name='purchase_book'),
]
