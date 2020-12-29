from django.contrib import admin

from char.models import UserCharRecord


@admin.register(UserCharRecord)
class UserCharRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'send', 'receive', 'content', 'create_time', 'status')
