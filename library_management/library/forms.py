from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Librarian, Book
from django.contrib.auth import authenticate

# User Form (if needed, or otherwise you might have intended to use RegisterForm)
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_librarian', 'is_admin', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        # Remove the help_text for all fields
        help_texts = {
            'username': '',
            'email': '',
            'is_librarian': '',
            'is_admin': '',
            'password': '',
        }

    # Optionally, clean the password field for better UX
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('This field is required.')
        return password

# User Registration Form with Role Selection
class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('librarian', 'Librarian'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        if role == 'librarian':
            user.is_librarian = True
        else:
            user.is_librarian = False
        if commit:
            user.save()
        return user

# User Login Form
class LoginForm(forms.Form):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('librarian', 'Librarian'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        role = cleaned_data.get("role")
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None or not self._check_role(user, role):
                raise forms.ValidationError("Invalid username, password, or role.")
        return cleaned_data

    def _check_role(self, user, role):
        if role == 'admin':
            return user.is_superuser
        if role == 'librarian':
            return user.is_librarian
        if role == 'member':
            return not user.is_librarian
        return False

# Edit User Form
class EditUserForm(UserChangeForm):
    password = None  # Remove the password field for editing

    class Meta:
        model = User
        fields = ['username', 'email', 'is_librarian', 'is_admin']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_librarian': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Librarian Form
class LibrarianForm(forms.ModelForm):
    class Meta:
        model = Librarian
        fields = ['employee_id', 'contact_number']  # Fields from the Librarian model

    # This will allow selecting a user when adding a librarian
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_librarian=False))

    def save(self, commit=True):
        # Override the save method to create the librarian and set is_librarian=True
        librarian = super().save(commit=False)
        librarian.user.is_librarian = True  # Set the user as a librarian
        if commit:
            librarian.user.save()
            librarian.save()
        return librarian

# Book Form
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date', 'available_copies']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'available_copies': forms.NumberInput(attrs={'class': 'form-control'}),
        }
