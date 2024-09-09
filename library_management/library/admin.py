# library/admin.py
from django.contrib import admin
from .models import User, Librarian, Book

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_librarian', 'is_admin')
    list_filter = ('is_librarian', 'is_admin')
    search_fields = ('username', 'email')

class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'contact_number')
    search_fields = ('user__username', 'employee_id')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publication_date', 'available_copies')
    search_fields = ('title', 'author', 'isbn')

admin.site.register(User, UserAdmin)
admin.site.register(Librarian, LibrarianAdmin)
admin.site.register(Book, BookAdmin)
