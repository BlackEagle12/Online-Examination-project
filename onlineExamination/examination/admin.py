from django.contrib import admin
from .models import Test,Answer,Attempt,Question
# Register your models here.


admin.site.register(Test)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Attempt)
