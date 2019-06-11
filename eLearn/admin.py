from django.contrib import admin
from .models import Course, Video

class ModuleInline(admin.StackedInline):
    model = Video 

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploadDate']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModuleInline]
