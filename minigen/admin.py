from django.contrib import admin
from minigen.models import MCQPost, Response

@admin.register(MCQPost)
class MCQPostAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('question', 'reference', 'option1', 'option2', 'option3', 'option4', 'answer', 'description')
    ordering = ('-created_at',)

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'mcq_post', 'selected_option', 'is_correct', 'created_at', 'updated_at')
    list_filter = ('is_correct', 'created_at', 'user', 'mcq_post')
    search_fields = ('user__username', 'mcq_post__question', 'selected_option')
    ordering = ('-created_at',)


# If you have any other models to register, include them here as well.
# admin.site.register(AnotherModel)
from django.contrib import admin
from minigen.models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ('is_read', 'created_at')
    ordering = ('-created_at',)




