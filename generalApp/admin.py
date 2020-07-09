from django.contrib import admin

from .models import *

admin.site.register(Users)
admin.site.register(Threads)
admin.site.register(Subjects)
admin.site.register(Comments)
admin.site.register(Ratings)
admin.site.register(Transactions)
admin.site.register(Triggers)
admin.site.register(Notifications)
# login: Admin
# password: Admin
