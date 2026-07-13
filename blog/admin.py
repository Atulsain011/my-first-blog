from django.contrib import admin
from .models import Post, Category, Tag
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']  
    prepopulated_fields = {'slug': ('name',)}
   
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'created_date', 'published_date', 'thumbnail_preview']
    list_filter = ['category', 'published_date']
    prepopulated_fields = {'slug': ('title',)}

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50"  style="border-radius: 10px;">', 
             obj.image.url 
            )
            return "-"


              