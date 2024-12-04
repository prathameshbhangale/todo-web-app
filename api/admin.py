from django.contrib import admin
from .models import Task, Tag

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'timestamp', 'due_date')
    list_filter = ('status', 'due_date', 'timestamp')
    search_fields = ['title', 'description']
    fields = ('title', 'description', 'status', 'due_date', 'tags', 'timestamp')
    readonly_fields = ['timestamp']

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)
