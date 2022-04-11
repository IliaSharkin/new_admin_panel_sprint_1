from django.contrib import admin
from .models import Film_work, Genre, Genre_film_work, Person, Person_film_work


class PersonRoleInline(admin.TabularInline):
    model = Person_film_work
    extra = 0


class FilmWorkGanreInline(admin.TabularInline):
    model = Genre_film_work
    extra = 0


@admin.register(Film_work)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
    )

    list_filter = ('type',)

    search_fields = ('title', 'description', 'id',)

    fields = (
        "title",
        "type",
        "description",
        "creation_date",
        "certificate",
        "file_path",
        "rating",
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

    fields = ("name", "description")

    inlines = [FilmWorkGanreInline]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "birth_date")

    fields = ("full_name", "birth_date")

    inlines = [PersonRoleInline]
