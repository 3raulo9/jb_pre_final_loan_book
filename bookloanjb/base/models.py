from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

# UserProfileInfo model to store additional user information
class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User model
    country_of_residence = models.CharField(max_length=256, blank=True)  # User's country of residence
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)  # User's profile picture

    def __str__(self):
        return self.user.username


# Author model to store information about authors
class Author(models.Model):

    name = models.CharField(max_length=64)  # Author's name
    birth_year = models.IntegerField()  # Author's birth year
    nationality = models.CharField(max_length=64)  # Author's nationality

    def __str__(self):
        return self.name


# Ebook model to store information about ebooks
class Ebook(models.Model):
    name = models.CharField(max_length=64)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    year_published = models.IntegerField()  # Store year as an integer
    loan_type = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(3),
            MinValueValidator(1)
        ]
    )
    ebook_content = models.CharField(max_length=2560)

    def __str__(self):
        return self.name



# Loan model to track ebook loans
class Loan(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )  # Foreign key to User model for the user who borrowed the ebook

    ebook = models.ForeignKey(Ebook,  on_delete=models.CASCADE)  # Foreign key to Ebook model for the borrowed ebook
    loan_date = models.DateField()  # Date the ebook was borrowed
    loan_delete = models.DateField()  # Date the ebook is expected to be returned

    def __str__(self):
        return str(self.id)


# Review model to store ebook reviews
class Review(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )  # Foreign key to User model for the user who wrote the review

    ebook = models.ForeignKey(Ebook,  on_delete=models.CASCADE)  # Foreign key to Ebook model for the reviewed ebook
    rating = models.IntegerField(validators=[
                                    MaxValueValidator(5),
                                    MinValueValidator(1)
                                        ])  # Rating for the ebook (1 to 5)
    text_field = models.CharField(max_length=500)  # Text field for the review

