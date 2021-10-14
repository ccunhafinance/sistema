from datetime import datetime
from django.db import models

# Ofertas RF -----------------

# Oferta

class OfferRf(models.Model):

    choices_ativo = (("CRA", "CRA"), ("CRI", "CRI"),("LF", "LF"), ("Debenture", "Debenture"), ("Debenture Incentivada", "Debenture Incentivada"))
    choices_ir = (('Sim', 'Sim'), ('Não', 'Não'))
    choices_prof = (('Sim', 'Sim'), ('Não', 'Não'))
    choices_qualy = (('Sim', 'Sim'), ('Não', 'Não'))
    choices_suit = (('A', 'Agressivo'), ('M', 'Moderado'), ('C', 'Conservador'))

    ativo = models.CharField("Ativo", choices=choices_ativo, max_length=100)
    emissor = models.CharField("Emissor", max_length=255)
    vol_total = models.CharField("Volume Total", max_length=200)
    rating = models.CharField("Rating", max_length=100)
    invet_min = models.FloatField("Investimento Mínimo", blank=True, null=True)
    coorder = models.CharField("Coordenadores", max_length=255, blank=True)
    garantia = models.CharField("Garantia", max_length=100, blank=True)
    is_ir = models.CharField("Isento de IR?", choices=choices_ir, default="Sim", max_length=100)
    is_qualy = models.CharField("Investidor Qualificado?", choices=choices_qualy, default="Não", max_length=100)
    is_prof = models.CharField("Investidor Profissional?", choices=choices_prof, default="Não", max_length=100)
    suitability = models.CharField("Suitability", choices=choices_suit, default="Agressivo", max_length=100)
    start_reserv = models.DateField("Início das Reservas")
    end_reserv = models.DateField("Encerramento das Reservas")
    bookbuilding = models.DateField("Bookbuilding")
    liquid = models.DateField("Liquidação")
    about_comp = models.TextField("Sobre a Empresa", blank=True)
    fee = models.TextField("Fee", blank=True)
    link_warning = models.URLField("Aviso ao Mercado")
    link_pub = models.URLField("Material de Divulgação", blank=True)

    def __str__(self):
        return f"{self.ativo} {self.emissor}"

    class Meta:
        verbose_name = 'Renda Fixa'
        verbose_name_plural = 'Renda Fixa'

# Serie RF
class SerieRf(models.Model):
    serie = models.ForeignKey(OfferRf, on_delete=models.CASCADE)

    choices_serie = (('Única', 'Única'), ('1ª Série', '1ª Série'), ('2ª Série', '2ª Série'))

    tipe = models.CharField('Série', choices=choices_serie, max_length=50)
    tax_top = models.CharField("Taxa Teto", max_length=100)
    tax_ref = models.FloatField("Taxa Referêncial")
    venciment = models.DateField("Vencimento")
    duration = models.CharField("Duration (em anos)", max_length=100)
    amort = models.CharField("Amortização", max_length=100)
    amort_beg = models.DateField("Início da Amortização")
    jurus = models.CharField("Jurus", max_length=100)
    current_tax = models.CharField("Taxa Atual Aproximada", max_length=100)
    obs = models.TextField("Observações", null=True, blank=True)

    class Meta:
        verbose_name = 'Série'
        verbose_name_plural = 'Séries'

class EmailRf(models.Model):
    id_oferta = models.ForeignKey(OfferRf, on_delete=models.CASCADE)
    id_sender = models.IntegerField(null=True, blank=True)
    nome_oferta = models.CharField(max_length=100)
    remetente = models.CharField(max_length=100)
    codigo_cliente = models.CharField(max_length=100)
    nome_cliente = models.CharField(max_length=100)
    serie = models.CharField(max_length=100)
    assessor_responsavel = models.CharField(max_length=100)
    taxa = models.CharField(max_length=100)
    valor = models.CharField(max_length=200)
    email_body = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=200)
    assunto = models.CharField(max_length=200)
    data_sent = models.DateTimeField(default=datetime.now, blank=True)

# Ofertas RV -----------------

# IPO
class OfferRvIpo(models.Model):

    choices_tipe = (
        ("Ações Ordinárias", "Ações Ordinárias"),
        ("Ações Preferênciais", "Ações Preferênciais"),
        ("Ações Ordinárias e Preferênciais", "Ações Ordinárias e Preferênciais"),
        ("Certificados de Depósito de Ações Representativo de Ações Ordinárias Classe A",
         "Certificados de Depósito de Ações Representativo de Ações Ordinárias Classe A"),
    )
    choices_pri = (("Sim", "Sim"), ("Não", "Não"))
    choices_sec = (("Sim", "Sim"), ("Não", "Não"))

    tipe = models.CharField("Tipo de Oferta", choices=choices_tipe, max_length=200)
    offer_pri = models.CharField("Oferta Primária", choices=choices_pri, default="Sim", max_length=100)
    offer_sec = models.CharField("Oferta Secundária", choices=choices_sec, default="Sim",  max_length=100)
    company = models.CharField("Empresa", max_length=100)
    ticker = models.CharField("Ticker", max_length=50)
    base_offer = models.CharField("Oferta Base", max_length=255)
    lot_var = models.CharField("Lote Varejo", max_length=100)
    start_fx_ind = models.FloatField("Fixa Indicativa Inicial")
    end_fx_ind = models.FloatField("Fixa Indicativa Final")
    start_per_res = models.DateField("Início do Período de Reserva")
    end_per_res = models.DateField("Fim do Período de Reserva", blank=True)
    end_vinc = models.DateField("Fim Vinculados")
    book = models.DateField("Bookbuilding")
    star_neg = models.DateField("Início das Negociações")
    liquid = models.DateField("Liquidação")
    about_comp = models.TextField("Sobre a Empresa", blank=True)
    coorder = models.TextField("Coordenadores", blank=True)
    dest_resor = models.TextField("Destinação de Recursos", blank=True)
    link_pros = models.URLField("Prospecto")
    link_warning = models.URLField("Aviso ao Mercado")
    link_eleven = models.URLField("Relatório Eleven", blank=True)

    def __str__(self):
        return f"{self.ticker} {self.company}"

    class Meta:
        verbose_name = 'IPO'
        verbose_name_plural = 'IPO'

# Modalidade IPO
class ModalidadeIpo(models.Model):

    modalida = models.ForeignKey(OfferRvIpo, on_delete=models.CASCADE)

    name = models.CharField("Modalidade", max_length=255)
    fee = models.FloatField("Fee")
    garant = models.FloatField("Gaantia Exigida")
    min_reserv = models.FloatField("Reserva Mínima")
    max_reserv = models.FloatField("Reserva Máxima")
    lock_end = models.DateField("Término do Lock-Up", blank=True, null=True)
    obs = models.TextField("Observações", blank=True, null=True)

# Regitro de email
class EmailIpo(models.Model):
    id_oferta = models.ForeignKey(OfferRvIpo, on_delete=models.CASCADE)
    id_sender = models.IntegerField(null=True, blank=True)
    nome_oferta = models.CharField(max_length=100)
    remetente = models.CharField(max_length=100)
    codigo_cliente = models.CharField(max_length=100)
    nome_cliente = models.CharField(max_length=100)
    modalidaade = models.CharField(max_length=100)
    assessor_responsavel = models.CharField(max_length=100)
    vinculo = models.CharField(max_length=10)
    valFim = models.CharField(max_length=100)
    preMax = models.CharField(max_length=100)
    email_body = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=200)
    assunto = models.CharField(max_length=200)
    data_sent = models.DateTimeField(default=datetime.now, blank=True)

# Direito de Subscriçao
class OfferRvSubscription(models.Model):
    company = models.CharField("Empresa", max_length=100)
    ticker = models.CharField("Ticker", max_length=50)
    code_subs = models.CharField("Código do Direito de Subscrição", max_length=100)
    mkt_price = models.FloatField("Preço de Mercado")
    mkt_price_date = models.DateField("Data Preço de Mercado")
    ex_price = models.FloatField("Preço do Exercício")
    dir_price = models.FloatField("Preço do Direito")
    dir_price_date = models.DateField("Data Preço do Direito")
    start_deal_dir = models.DateField("Início da Negociação do Direito")
    end_deal_dir = models.DateField("Fim da Negociação do Direito")
    start_reser = models.DateField("Inicio do Período de Reserva")
    end_reser = models.DateField("Fim do Período de Reserva")
    liquid = models.DateField("Liquidação")
    fee = models.TextField("Fee")
    fact = models.TextField("Fator")
    date_ex = models.DateField("Data Ex.")
    link_pdf = models.URLField("Link PDF")

    def __str__(self):
        return f"{self.ticker} {self.company}"

    class Meta:
        verbose_name = 'Direito de Subscrição'
        verbose_name_plural = 'Direito de Subscrição'

# Fii
class EmailFii(models.Model):
    ticker = models.CharField(max_length=100)
    emissao = models.CharField(max_length=100)
    id_sender = models.IntegerField(null=True, blank=True)
    nome_oferta = models.CharField(max_length=100)
    remetente = models.CharField(max_length=100)
    codigo_cliente = models.CharField(max_length=100)
    nome_cliente = models.CharField(max_length=100)
    assessor_responsavel = models.CharField(max_length=100)
    valor_da_cota = models.CharField(max_length=200)
    valor_financeiro = models.CharField(max_length=200)

    email_body = models.TextField(blank=True, null=True)
    email_body = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=200)
    assunto = models.CharField(max_length=200)
    data_sent = models.DateTimeField(default=datetime.now, blank=True)
