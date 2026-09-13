from django.contrib import admin
from .models import Book, Music, Toy


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'library_code', 'author', 'genre', 'status')
    search_fields = ('name', 'author')


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'library_code', 'artist', 'year', 'status')
    search_fields = ('name', 'artist')


@admin.register(Toy)
class ToyAdmin(admin.ModelAdmin):
    list_display = ('name', 'library_code', 'type', 'age', 'status')