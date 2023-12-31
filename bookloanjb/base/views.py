# Import necessary modules from Django
from random import randint
import random
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from base.forms import UserForm, ReviewForm,  EbookForm
from base.models import Author, Ebook, Loan, Review
from django.contrib.admin.views.decorators import staff_member_required

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
        # Create UserForm instance with data from the request
        user_form = UserForm(data=request.POST)

        # Check if the form is valid
        if user_form.is_valid():
            # Save the user data from 'user_form'
            user = user_form.save()

            # Hash and save the user's password
            user.set_password(user.password)
            user.save()

            registered = True

        else:
            print(user_form.errors)
            return render(request, 'base/registration.html',
                          {'user_form': user_form,
                           'registered': registered, })

    else:
        # If the request method is not POST, create an empty form
        user_form = UserForm()

    # Render the 'registration.html' template with forms and registration status
    return render(request, 'base/registration.html',
                  {'user_form': user_form,
                   'registered': registered})

# Define the 'user_login' view function
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Log in the user and redirect to the 'index' page
            login(request, user)
            return redirect('/library/profile')
        else:
            # Render the login page with an error message
            error_message = "Incorrect username or password"
            return render(request, 'base/login.html', {'error': error_message})
    else:
        # Render the login page
        return render(request, 'base/login.html', {})

# Define the 'display_books' view function
def display_books(request):
    if request.method == "POST":
        search = request.POST.get('searched')
        ebook_list = Ebook.objects.filter(name__contains=search)
        books_dict = {'book_records': ebook_list}
        return render(request, 'base/ebooks.html', context=books_dict)
    elif request.method == "GET":
        ebook_list = Ebook.objects.order_by('id')
        books_dict = {'book_records': ebook_list}
        return render(request, 'base/ebooks.html', context=books_dict)

# Define the 'author_detail' view function
def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    # Optionally, you can fetch the list of books associated with this author here
    # books = author.books.all()
    return render(request, 'base/author_profile.html', {'author': author})

# Define the 'author_profile' view function
def author_profile(request, authorname):
    author_info = Author.objects.get(name=authorname)
    book_info = Ebook.objects.filter(author=author_info.id)
    info_dict = {'author_info': author_info, 'book_info': book_info}
    return render(request, 'base/author_profile.html', context=info_dict)

# Define the 'display_authors' view function
def display_authors(request):
    if request.method == "POST":
        search = request.POST.get('searchedauthor')
        author_list = Author.objects.filter(name__contains=search)
        authors_dict = {'author_records': author_list}
        return render(request, 'base/authors.html', context=authors_dict)
    elif request.method == "GET":
        author_list = Author.objects.order_by('name')
        authors_dict = {'author_records': author_list}
        return render(request, 'base/authors.html', context=authors_dict)

# Define the 'random_authors' view function
def random_authors(request):
    # Get the minimum and maximum IDs of ebooks in the database
    min_id = Ebook.objects.all().order_by('id').first().id
    max_id = Ebook.objects.all().order_by('-id').first().id

    if min_id is not None and max_id is not None:
        # Generate a random book ID within the range [min_id, max_id]
        random_book_id = random.randint(min_id, max_id)

        try:
            # Try to fetch the ebook with the generated random ID
            random_ebook = Ebook.objects.get(pk=random_book_id)
        except Ebook.DoesNotExist:
            # Handle the case where the random ID doesn't exist
            raise Http404("Random book does not exist.")

        # Build the URL for the random book profile page using the book's name
        random_book_profile_url = reverse('base:book_profile', args=[random_ebook.name])

        # Redirect to the random book profile page
        return redirect(random_book_profile_url)
    else:
        # Handle the case where there are not enough books
        raise Http404("Not enough books to generate a random page.")

# Define the 'index' view function
def index(request):
    try:
        loans = Loan.objects.filter(user=request.user)
        for i in loans:
            if i.loan_delete < datetime.date.today():
                Loan.objects.filter(id=i.id).delete()
    except:
        pass

    # Get a list of authors and ebooks ordered by 'name' and 'id' respectively
    author_list = Author.objects.order_by('name')
    ebook_list = Ebook.objects.order_by('id')
    items_dict = {'book_records': ebook_list, 'author_records': author_list}
    return render(request, 'base/index.html', context=items_dict)

# Define the 'book_profile' view function
def book_profile(request, bookname, ratefilter=False):
    if request.method == "POST":
        review_form = ReviewForm(data=request.POST)
        review_rate = request.POST.get('inlineRadioOptions')
        if review_form.is_valid():
            clean_text = review_form.cleaned_data['text_field']
            ebookdata = Ebook.objects.get(name=bookname)
            Review.objects.create(user=request.user, ebook=ebookdata, rating=review_rate, text_field=clean_text)
            print("review saved")
        else:
            print("error: review not saved")

    book_info = Ebook.objects.get(name=bookname)

    if ratefilter:
        reviews = Review.objects.filter(rating=ratefilter, ebook=book_info)
    else:
        reviews = Review.objects.filter(ebook=book_info).order_by('-date')

    loaned = False
    try:
        loans = Loan.objects.filter(user=request.user, ebook=book_info)
    except:
        loans = []
    if len(loans) != 0:
        loans = loans[0]
        loaned = True

    rating_sum = (0)
    for i in reviews:
        rating_sum += i.rating
    try:
        rating_avg = round(rating_sum / len(reviews), 2)
    except:
        rating_avg = 0

    review_form = ReviewForm()
    info_dict = {'book_info': book_info, 'random': random.randint(0, 300), "review_form": review_form,
                 "reviews": reviews, "reviews_amount": len(reviews), "loaned": loaned, "loans": loans,
                 'rating_avg': rating_avg}
    return render(request, 'base/book_profile.html', context=info_dict)

# Define the 'random_book_profile' view function
def random_book_profile(request, bookid):
    try:
        book_info = Ebook.objects.get(id=bookid)
        info_dict = {'book_info': book_info, 'random': random.randint(0, 500)}
        return render(request, 'base/book_profile.html', context=info_dict)
    except Ebook.DoesNotExist:
        raise Http404("Book not found")

# Loaning book function
@login_required
def loan_book(request, bookname, loan_type):

    if int(loan_type) == 2:
        loan_delete = datetime.date.today() + datetime.timedelta(days=7)
    elif int(loan_type) == 3:
        loan_delete = datetime.date.today() + datetime.timedelta(days=3)
    else:
        loan_delete = datetime.date.today() + datetime.timedelta(days=14)
    ebookdata = Ebook.objects.get(name=bookname)
    Loan.objects.get_or_create(user=request.user, ebook=ebookdata, loan_date=datetime.date.today(),
                               loan_delete=loan_delete)
    bookname = bookname.replace(' ', '%20')
    return redirect(f"/library/book_profile/{bookname}/")

@login_required
def user_profile(request):
    emptyloan = False
    emptyreview = False
    updated = False
    user_info = request.user

    if request.method == 'POST':
        user_form = UserForm(data=request.POST, instance=user_info)
        
        # Check if the user form is valid.
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            updated = True

    user_form = UserForm()

    user_loans = Loan.objects.filter(user=user_info)
    for i in user_loans:
        if i.loan_delete < datetime.date.today():
            Loan.objects.filter(id=i.id).delete()
    if len(user_loans) == 0:
        emptyloan = True
    user_reviews = Review.objects.filter(user=user_info)
    if len(user_reviews) == 0:
        emptyreview = True

    user_dict = {'userinfo': user_info, 'userloans': user_loans, 'userreviews': user_reviews, 'loans': emptyloan,
                 'reviews': emptyreview, 'user_form': user_form, 'updated': updated}
    return render(request, 'base/user_profile.html', context=user_dict)

@login_required
def delete_loan(request, bookname):
    bookname = Ebook.objects.get(name=bookname)
    Loan.objects.filter(user=request.user, ebook=bookname).delete()
    return redirect('/library/profile')

@login_required
def delete_review(request, review_id):
    Review.objects.filter(id=review_id).delete()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def update_review(request, review_id):
    if request.method == 'POST':
        new_text = request.POST.get('review')
        new_rating = request.POST.get('inlineRadioOptions')
        Review.objects.filter(user=request.user, id=review_id).update(rating=new_rating, text_field=new_text)
        return redirect('/library/profile')
    reviews = Review.objects.filter(user=request.user, id=review_id)
    dict = {'review': reviews[0], }
    return render(request, 'base/review_update_form.html', context=dict)

@login_required
def delete_user(request):
    if request.method == 'POST':
        value = request.POST.get('button')
        if value == "abort":
            return redirect('/library/profile')
        elif value == "delete":
            user = request.user
            user.delete()
            return redirect('index')
    return render(request, 'base/user_delete.html')

@staff_member_required
def add_book(request):
    added = False
    add_isnt_valid = False
    
    # Check if the request method is POST (usually for form submissions).
    if request.method == 'POST':
        ebook_form = EbookForm(data=request.POST)
        
        # Check if the form is valid.
        if ebook_form.is_valid():
            ebook_form.save()  # Save the ebook data.
            added = True  # Set added flag to True.
        else:
            add_isnt_valid = True  # Form is not valid.
    
    ebook_form = EbookForm()  # Create a new empty form.
    
    # Render the 'add_book.html' template with the ebook_form and flags.
    return render(request, 'base/add_book.html', {'ebook_form': ebook_form, 'add_isnt_valid': add_isnt_valid, "added": added, 'update': False})

@staff_member_required
def update_book(request, book_id):
    updt_isnt_valid = False
    
    # Get the Ebook object with the given book_id.
    book = Ebook.objects.get(id=book_id)
    
    # Check if the request method is POST (usually for form submissions).
    if request.method == 'POST':
        ebook_form = EbookForm(request.POST, instance=book)
        
        # Check if the form is valid.
        if ebook_form.is_valid():
            ebook_form.save()  # Save the updated ebook data.
            return redirect(f'/library/book_profile/{book.name}')  # Redirect to the book profile page.
        else:
            updt_isnt_valid = True  # Form is not valid.
    
    ebook_form = EbookForm()  # Create a new empty form.
    
    # Render the 'add_book.html' template with the ebook_form, book, and flags.
    return render(request, 'base/add_book.html', {'ebook_form': ebook_form, 'updt_isnt_valid': updt_isnt_valid, 'update': True, 'book': book})

@staff_member_required
def delete_book(request, book_id):
    Ebook.objects.filter(id=book_id).delete()  # Delete the ebook with the given book_id.
    return redirect('index')  # Redirect to the index page.