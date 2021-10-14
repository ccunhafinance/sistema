from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.auth.hashers import make_password
from django.contrib.auth import admin as user_auth


from .models import *


class HashPassword(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        value = str(row['password'])
        row['password'] = make_password(value)

    class Meta:
        model = CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
    resource_class = HashPassword
    list_display = ('type', 'codigo', 'first_name', 'last_name', 'sex', 'telefone', 'email', 'nascimento',)
    import_id_fields = ('isbn',)
    # fieldsets = (
    #     (None, {
    #         'classes':('wide',),
    #         'fields':('type', 'codigo', 'first_name', 'last_name', 'sex', 'telefone', 'email', 'nascimento', 'password', 'password2')}
    #     ),
    # )

# admin.site.register(CustomUserAdmin, user_auth.UserAdmin)









@admin.register(UserProfile)
class CustomUserAdmin(ImportExportModelAdmin):
    pass


# admin.site.register(CustomUser)
# admin.site.register(UserProfile)
