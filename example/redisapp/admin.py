from django.contrib import admin

from duckadmin import DuckAdmin

from redisapp.forms import MyRedisForm

@admin.register(MyRedisForm)
class MyRedisAdmin(DuckAdmin):
    duck_form = MyRedisForm
