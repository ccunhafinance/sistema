from django.urls import path
from .views import *
from .import views
from django.views.decorators.csrf import csrf_exempt


app_name = 'mail'

urlpatterns = [
    path('mail_list/<int:num>/', views.mail_list, name="mail-list"),
    path('category/add/error/<int:num>/', views.mail_list, name="mail-list-error"),
    path('categoria/add/', views.add_categoria, name="categoria-add"),
    path('get_all_templates/', views.get_category_templates, name="get-all-templates"),

    path('add_template/<str:num>/<int:var>/', views.add_template, name="template-view"),

    path('edit_template/<str:num>/<int:var>/', views.edit_template, name="template-edit"),

    path('add_template/<str:num>/', views.add_template, name="template-view"),
    path('delete_template/<str:num>/', views.delete_template, name="delete-template"),
    path('delete_template_one/<str:num>/', views.delete_template_one, name="delete-template-one"),

    path('edit_categ/', views.edit_categ, name="edit_categ"),

    path('cadastrar-template/', views.cadastrar_template, name="cadastrar-template"),
    path('save_edit_template/', views.save_edit_template, name="save-edit-template"),
    path('template-preview/<int:pk>/', views.template_preview, name="template_preview"),
]