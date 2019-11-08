from django.contrib import admin
from .models import Post, Category, SubCategory, Contact
from userApp.models import UserProfile, Ranks, Messages, Channel


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(Ranks)
admin.site.register(Messages)
admin.site.register(Channel)


