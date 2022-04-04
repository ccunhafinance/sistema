from django.contrib import admin
from .models import EmailRf, OfferRf, SerieRf, OfferRvSubscription, OfferRvIpo, ModalidadeIpo

class OfferRFPropertyInline(admin.StackedInline):
    model = SerieRf
    initial_num = 0

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            return max(self.initial_num, 1)
        return self.initial_num

class OfferRFAdmin(admin.ModelAdmin):
    inlines = [OfferRFPropertyInline]


    def property_value(self, obj):
        return obj.get_value()

class OfferRvIpoPropertyInline(admin.StackedInline):
    model = ModalidadeIpo
    initial_num = 0

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            return max(self.initial_num, 0)
        return self.initial_num

class OfferRvIpoAdmin(admin.ModelAdmin):
    inlines = [OfferRvIpoPropertyInline]


    def property_value(self, obj):
        return obj.get_value()


admin.site.register(OfferRf, OfferRFAdmin)
admin.site.register(OfferRvIpo, OfferRvIpoAdmin)
admin.site.register(OfferRvSubscription)
admin.site.register(EmailRf)
