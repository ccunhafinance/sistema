from import_export import resources
from .models import Clientes

class ClientesResources(resources.ModelResource):
    class Meta:
        model = Clientes