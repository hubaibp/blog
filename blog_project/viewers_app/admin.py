from django.contrib import admin
from writers_app.models import Blog,UserProfile
from viewers_app.models import Comment
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Blog)
admin.site.register(Comment)