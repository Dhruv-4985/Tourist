from django.contrib import admin
from .models import service


class serviceadmin(admin.ModelAdmin):
    list_display = ('icon','title','description')
    search_fields = ('icon','title','description')

admin.site.register(service,serviceadmin)


# Register your models here.
