from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Profile, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "created_at", "preview")
    search_fields = ("title", "description")
    list_filter = ("created_at",)
    inlines = [LessonInline]

    def preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" height="50">')
        return "Нет изображения"
    preview.short_description = "Превью"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "video")
    search_fields = ("title", "course__title")
