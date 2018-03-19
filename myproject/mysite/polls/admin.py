from django.contrib import admin

# Register your models here.
from .models import Question

#tell the admin that Question objects have an admin interface
admin.site.register(Question)
