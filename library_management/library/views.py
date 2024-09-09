from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import UserForm, EditUserForm, LibrarianForm, BookForm, LoginForm, RegisterForm
from .models import Purchase, User, Librarian, Book
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import PermissionDenied

# ------------------- DASHBOARD VIEWS -------------------

# Admin Dashboard View
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Librarian Dashboard View
@login_required
def librarian_dashboard(request):
    return render(request, 'librarian_dashboard.html')

# Member Dashboard View
@login_required
def member_dashboard(request):
    return render(request, 'member_dashboard.html')

# ------------------- USER MANAGEMENT VIEWS -------------------

# View to manage users
@login_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

# View to add a new user
@login_required
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

# View to edit an existing user
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

# View to delete a user
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_users')
    return render(request, 'delete_user.html', {'user': user})

# ------------------- LIBRARIAN MANAGEMENT VIEWS -------------------

@login_required
def librarian_dashboard(request):
    if not request.user.is_librarian:
        return redirect('home')

    books = Book.objects.all()
    return render(request, 'librarian_dashboard.html', {'books': books})

@login_required
def add_book(request):
    if not request.user.is_librarian:
        return redirect('home')
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('librarian_dashboard')  # Redirect to librarian dashboard
    else:
        form = BookForm()
    
    return render(request, 'add_book.html', {'form': form})

@login_required
def edit_book(request, book_id):
    if not request.user.is_librarian:
        return redirect('home')
    
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('librarian_dashboard')  # Redirect to librarian dashboard
    else:
        form = BookForm(instance=book)
    
    return render(request, 'edit_book.html', {'form': form})

@login_required
def delete_book(request, book_id):
    if not request.user.is_librarian:
        return redirect('home')
    
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('librarian_dashboard')  # Redirect to librarian dashboard
    
    return render(request, 'confirm_delete.html', {'book': book})

# ------------------- BOOK MANAGEMENT VIEWS -------------------

@login_required
def admin_manage_books(request):
    if not request.user.is_admin:
        return redirect('home')  # or any other page

    books = Book.objects.all()
    return render(request, 'admin_manage_books.html', {'books': books})

@login_required
def manage_books(request):
    books = Book.objects.all()
    return render(request, 'manage_books.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_books')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('manage_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('manage_books')
    return render(request, 'delete_book.html', {'book': book})

# ------------------- USER AUTHENTICATION VIEWS -------------------

# User Login View with Role Selection
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            user = authenticate(request, username=username, password=password)
            if user is not None and _check_role(user, role):
                auth_login(request, user)  # Corrected login function alias
                if role == 'admin':
                    return redirect('admin_dashboard')
                elif role == 'librarian':
                    return redirect('librarian_dashboard')
                else:
                    return redirect('member_dashboard')
            else:
                form.add_error(None, "Invalid username, password, or role.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Helper function to check user role
def _check_role(user, role):
    if role == 'admin':
        return user.is_superuser
    elif role == 'librarian':
        return hasattr(user, 'is_librarian') and user.is_librarian
    elif role == 'member':
        return hasattr(user, 'is_librarian') and not user.is_librarian
    return False

# User Registration View
def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Home View
def home(request):
    return render(request, 'home.html')  # Render a template for the homepage

def user_logout(request):
    auth_logout(request)
    return redirect('login')  # Ensure 'login' matches the URL name for your login page

@login_required
def member_dashboard(request):
    books = Book.objects.all()
    return render(request, 'member_dashboard.html', {'books': books})

@login_required
def purchase_book(request, book_id, purchase_type):
    book = get_object_or_404(Book, id=book_id)
    
    # Ensure the user has a related Member profile
    if not hasattr(request.user, 'member'):
        raise PermissionDenied("User does not have a member profile.")
    
    if purchase_type not in ['rent', 'buy']:
        return redirect('member_dashboard')  # or some error handling

    # Create a Purchase record
    Purchase.objects.create(
        member=request.user.member,
        book=book,
        purchase_type=purchase_type
    )
    
    # Update available copies if it's a rental
    if purchase_type == 'rent':
        book.available_copies -= 1
        book.save()
    
    return redirect('member_dashboard')  # Redirect to dashboard or a confirmation page