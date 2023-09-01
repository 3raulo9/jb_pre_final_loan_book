from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    birth_year = models.IntegerField()
    nationality = models.CharField(max_length=100)

class Ebook(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    year_published = models.IntegerField()
    loan_type = models.IntegerField()  # You can use choices to restrict values
    ebook_content = models.TextField()

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    loan_date = models.DateField()
    loan_delete = models.BooleanField(default=False)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    text_field = models.TextField()
    date = models.DateField()
