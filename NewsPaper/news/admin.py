from django.contrib import admin
from .models import *


# напишем уже знакомую нам функцию обнуления товара на складе
def nullfy_rating(modeladmin, request, queryset):
    # все аргументы уже должны быть вам знакомы,
    # самые нужные из них это request — объект хранящий информацию о запросе и queryset —
    # грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(authorRating=0)
    nullfy_rating.short_description = 'Обнулить рейтинг автора'
    # описание для более понятного представления в админ панеле задаётся, как будто это объект

# создаём новый класс для представления товаров в админке
class AuthorAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # генерируем список имён всех полей для более красивого отображения
    list_display = ('authorUser', 'authorRating', 'above_zero_rating')
    list_filter = ('authorUser', 'authorRating')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('authorRating', 'authorUser__id')  # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_rating]  # добавляем действия в список

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]
    list_filter = ('text', 'rating')
    search_fields = ('text', 'commentUser__email')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('theme',)
    list_filter = ('theme',)
class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'category', 'postAuthor', 'date')
    list_filter = ('topic', 'category')

# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)

