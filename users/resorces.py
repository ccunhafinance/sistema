from .models import CustomUser
from import_export import resources
from django.contrib.auth.hashers import make_password

class CustomUserResorcers(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        value = row['password']
        row['password'] = make_password(value)

    class Meta:
        model = CustomUser