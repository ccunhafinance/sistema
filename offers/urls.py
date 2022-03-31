from django.urls import path
from .views import *
from .import views

app_name = 'offers'

urlpatterns = [
    # Renda Fixa
    # ------------------------------------------------------------------------------------------------------------------

    # Listar
    path('rf/listar/', OfferRfListView.as_view(), name="listar-rf"),
    # Adicionar
    path('rf/adicionar/', views.createrf, name="create-rf"),
    # Editar
    path('rf/editar/<int:pk>/', views.editrf, name="edit-rf"),
    # Deletar
    path('rf/deletar/<int:pk>/', DeleteOfferRfView.as_view(), name="delete-rf"),
    # Send Mail
    path('rf/enviar-email-rf/<int:pk>/', views.sendemailrf, name="send-mail-rf"),
    # Sent View
    path('rf/email-enviado-rf/<int:id>/', views.sentmailrf, name="sent-mail-rf"),

    # Renda Variável
    # ------------------------------------------------------------------------------------------------------------------

    # IPO
    # ------------------------------------------------------------------------------------------------------------------

    # Listar
    path('rv/ipo/listar/', OfferRvIpoListView.as_view(), name="listar-rv-ipo"),
    # Adicionar
    path('rv/ipo/adicionar/', views.creatervipo, name="create-rv-ipo"),
    # Editar
    path('rv/ipo/editar/<int:pk>/', views.editrvipo, name="edit-rv-ipo"),
    # Deletar
    path('rv/ipo/deletar/<int:pk>/', DeleteOfferRvIpoView.as_view(), name="delete-rv-ipo"),
    # Send Mail
    path('rv/ipo/enviar-email-rv-ipo/<int:pk>/', views.sendmailrvipo, name="send-mail-rv-ipo"),
    # Sent View
    path('rv/ipo/email-enviado-rv-ipo/<int:id>/', views.sentmailrvviewipo, name="sent-mail-rv-view-ipo"),

    # Direito de Subscrição
    # ------------------------------------------------------------------------------------------------------------------

    # Listar
    path('rv/direito-de-subscricao/listar/', OfferRvSubscriptionListView.as_view(), name="listar-rv-subscription"),
    # Adicionar
    path('rv/direito-de-subscricao/adicionar/', OfferRvSubscriptionCreateView.as_view(), name="create-rv-subscription"),
    # Editar
    path('rv/direito-de-subscricao/editar/<int:pk>/', OfferRvSubscriptionEditView.as_view(), name="edit-rv-subscription"),
    # Deletar
    path('rv/direito-de-subscricao/deletar/<int:pk>/', OfferRvSubscriptionDeleteView.as_view(), name="delete-rv-subscription"),
    # Get Ticker
    path('rv/get_ticker/', views.get_ticker_price, name="get-ticker"),

    # Fii
    # ------------------------------------------------------------------------------------------------------------------

    # Listar
    path('rv/fii/listar/', views.ofertarvfiiview, name="listar-rv-fii"),
    # Eviar Email
    path('rv/fii/enviar-email-rv-fii/<str:ticker>/<str:emissor>/', views.sendemailrvfii, name="send-mail-rv-fii"),
    # Enviar
    path('rv/fii/envia_email_fii/', views.envia_email_fii, name="envia-email-fii"),

    #EDIT FII

    # Adicionar
    path('rv/fii/adicionar/<str:ticker>/<str:emissor>/', OfferRvFiiCreateView.as_view(), name="create-rv-fii-edit"),
    # Editar
    path('rv/fii/editar/<int:pk>/', OfferRvFiiEditView.as_view(), name="edit-rv-fii-edit"),
    # Deletar
    path('rv/fii/deletar/<int:pk>/', OfferRvFiiDeleteView.as_view(), name="delete-rv-fii-edit"),

    # ---

    # Scrape TICKER11
    path('rv/fii/ticker11/', views.scrapy_ticker11, name="scrape-ticker11"),
    # Scrape ClubeFii
    path('rv/fii/clubefii/', views.scrapy_clubefii, name="scrape-clubefii"),
    # Fiis File Upload
    path('rv/fii/fii-files-upload/', views.fii_files_upload, name="fii-files-upload"),


]