from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

def nullfy_rating(modeladmin, request, queryset): # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating_of_post=0)
nullfy_rating.short_description = 'Обнулить рейтинг' # описание для более понятного представления в админ панеле задаётся, как будто это объект

class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('headline', 'author') # генерируем список имён всех полей для более красивого отображения
    list_filter = ('headline', 'author')
    search_fields = ('headline', 'author__author__username')
    actions = [nullfy_rating]
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
