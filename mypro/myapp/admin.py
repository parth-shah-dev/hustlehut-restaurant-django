from django.contrib import admin
from .models import*

# Register your models here.
@admin.register(AddItemAdmin)
class ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(cat)
class CatAdmin(admin.ModelAdmin):
    pass

@admin.register(book_table)
class Booktable(admin.ModelAdmin):
    pass

@admin.register(Reg)
class Reg(admin.ModelAdmin):
    pass



