from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
#from library.models import User

# Custom User model with role-based attributes
class User(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure unique email field
    is_librarian = models.BooleanField(default=False)  # Mark if user is a librarian
    is_admin = models.BooleanField(default=False)  # Mark if user is an admin
    
    # Override groups and user_permissions related_name to avoid clashes with the default User model
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Avoid default auth.User model conflict
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Avoid conflict with default permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

# Librarian model extending the User model
class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the custom User model
    employee_id = models.CharField(max_length=10, unique=True)  # Unique employee ID
    contact_number = models.CharField(max_length=15)  # Contact number for librarian

    def __str__(self):
        return f'Librarian: {self.user.username}'

# Member model
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    # Add any other fields as needed

    def __str__(self):
        return self.user.username
    
# Book model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    available_copies = models.PositiveIntegerField()
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

    def __str__(self):
        return f'{self.title} by {self.author}'

# Purchase model
class Purchase(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchase_type = models.CharField(
        max_length=10, choices=[('rent', 'Rent'), ('buy', 'Buy')]
    )
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.member.user.username} - {self.book.title} - {self.purchase_type}'