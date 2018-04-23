from django.contrib import admin
from apps.operation import models
# Register your models here.
@admin.register(models.UserAsk)
class UserAskAdmin(admin.ModelAdmin):
    '''用户表单我要学习'''

    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


#
@admin.register(models.UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    '''用户课程学习'''

    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']


@admin.register(models.UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    '''用户消息后台'''

    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


@admin.register(models.CourseComments)
class CourseCommentsAdmin(admin.ModelAdmin):
    '''用户评论后台'''

    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']


@admin.register(models.UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    '''用户收藏后台'''

    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']



