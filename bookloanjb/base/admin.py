from django.contrib import admin
from base.models import Author, Ebook, Loan, Review

# Register your models here.
admin.site.register(Author)
admin.site.register(Ebook)
admin.site.register(Loan)
admin.site.register(Review)