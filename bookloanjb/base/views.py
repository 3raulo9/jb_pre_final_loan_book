# Import necessary modules from Django
from django.shortcuts import render
from base.forms import UserForm, UserProfileInfoForm
from base.models import Author, Ebook, Loan, Review
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Define the 'index' view function
@login_required
def user_logout(request):
    # Logout the user and redirect to the 'index' page
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# Define the 'register' view function
def register(request):
    # Initialize a variable to track registration status
    registered = False

    # Check if the HTTP request method is POST
    if request.method == 'POST':
        # Create UserForm and UserProfileInfoForm instances with data from the request
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user data from 'user_form'
            user = user_form.save()

            # Hash and save the user's password
            user.set_password(user.password)
            user.save()

            # Create a 'UserProfileInfo' object but don't save it to the database yet
            profile = profile_form.save(commit=False)

            # Associate the user with the profile
            profile.user = user

            # Check if a profile picture is included in the request.FILES
            if 'profile_pic' in request.FILES:
                print('found it')
                # Assign the profile picture to the 'profile_pic' field
                profile.profile_pic = request.FILES['profile_pic']

            # Save the 'UserProfileInfo' object with the associated user
            profile.save()

            # Registration is successful
            registered = True

        else:
            # Print form errors if forms are not valid
            print(user_form.errors, profile_form.errors)

    else:
        # If the request method is not POST, create empty forms
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # Render the 'registration.html' template with forms and registration status
    return render(request, 'base/registration.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })

# Define the 'user_login' view function
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Log in the user and redirect to the 'index' page
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            # Render the login page with an error message
            error_message = "Incorrect username or password"
            return render(request, 'base/login.html', {'error': error_message})
    else:
        # Render the login page
        return render(request, 'base/login.html', {})

# Define the 'display_books' view function
def display_books(request):
    # Get a list of ebooks ordered by 'id'
    ebook_list = Ebook.objects.order_by('id')
    books_dict = {'book_records': ebook_list}
    return render(request, 'base/ebooks.html', context=books_dict)

# Define the 'display_authors' view function
def display_authors(request):
    # Get a list of authors ordered by 'name'
    author_list = Author.objects.order_by('name')
    authors_dict = {'author_records': author_list}
    return render(request, 'base/authors.html', context=authors_dict)

# Define the 'index' view function
def index(request):
    # Get a list of authors and ebooks ordered by 'name' and 'id' respectively
    author_list = Author.objects.order_by('name')
    ebook_list = Ebook.objects.order_by('id')
    items_dict = {'book_records': ebook_list, 'author_records': author_list}
    return render(request, 'base/index.html', context=items_dict)
