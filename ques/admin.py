from django.contrib import admin
from .models import CommitRecord, SelectRecord, CommitRecordAdmin, SelectRecordAdmin

# Register your models here.

admin.site.register(CommitRecord, CommitRecordAdmin)
admin.site.register(SelectRecord, SelectRecordAdmin)