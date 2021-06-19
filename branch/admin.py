from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Branch

@admin.register(Branch)
class BranchAdmin(ImportExportModelAdmin):
    pass

