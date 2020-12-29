from django.contrib import admin

from char.models import UserCharRecord, UserNotice


@admin.register(UserCharRecord)
class UserCharRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'send', 'receive', 'content', 'create_time', 'status')


@admin.register(UserNotice)
class UserNoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'work', 'examine', 'status', 'create_time')
