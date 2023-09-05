from django.contrib import admin
from base.models import UserProfileInfo, Author, Ebook, Loan, Review

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Author)
admin.site.register(Ebook)
admin.site.register(Loan)
admin.site.register(Review)