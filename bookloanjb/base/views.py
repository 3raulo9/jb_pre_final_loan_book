# Import necessary modules from Django
from django.shortcuts import render
from base.forms import UserForm, UserProfileInfoForm

# Define the 'index' view function
def index(request):
    # Render the 'index.html' template
    return render(request, 'base/index.html')

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
