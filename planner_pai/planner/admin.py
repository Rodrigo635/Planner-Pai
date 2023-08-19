from django.contrib import admin
from .models import AnoMes, Pessoa, Compra, GastosMensais, Recebimento
from django.db.models import Sum
from django.contrib.admin import DateFieldListFilter
from django.utils.translation import gettext_lazy as _
from django.db.models import F

class AnoMesFilter(admin.SimpleListFilter):
    title = _('Ano e Mês')
    parameter_name = 'ano_mes'

    def lookups(self, request, model_admin):
        anos_meses = AnoMes.objects.all()
        return [(am.id, f"{am.ano} - {am.get_mes_display()}") for am in anos_meses]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ano_e_mes_id=self.value())
        return queryset

class ParcelasAtuaisFilter(admin.SimpleListFilter):
    title = _('Compras com parcelas pendentes')
    parameter_name = 'parcelas_atuais_menores'

    def lookups(self, request, model_admin):
        return (
            ('sim', _('Sim')),
            ('nao', _('Não')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'sim':
            return queryset.filter(parcela_atual__lt=F('numero_de_parcelas'))
        elif self.value() == 'nao':
            return queryset.filter(parcela_atual=F('numero_de_parcelas'))
        return queryset

class CompraAdmin(admin.ModelAdmin):
    list_display = ('ano_e_mes', 'data_de_inicio', 'nome', 'compra', 'valor', 'parcela_atual', 'numero_de_parcelas')
    list_filter = (AnoMesFilter, ParcelasAtuaisFilter)

    def ano_e_mes(self, obj):
        return f"{obj.ano_e_mes}"

    def data_de_inicio(self, obj):
        return f"{obj.data_de_inicio}"

    def nome(self, obj):
        return f"{obj.nome}"

    def compra(self, obj):
        return f"{obj.compra}"

    def valor(self, obj):
        return f"{obj.valor}"

    def parcela(self, obj):
        return f"{obj.parcela_atual} - {obj.numero_de_parcelas}"

class GastosMensaisAdmin(admin.ModelAdmin):
    list_display = ('ano_e_mes', 'nome', 'total_gasto_pessoa', 'total_gasto_geral')
    list_filter = (AnoMesFilter,)

    def ano_e_mes(self, obj):
        return f"{obj.ano_e_mes}"
    
    def nome(self, obj):
        return f"{obj.nome}"

    def total_gasto_pessoa(self, obj):
        total_gasto = Compra.objects.filter(
            ano_e_mes=obj.ano_e_mes,
            nome=obj.nome
        ).aggregate(Sum('valor'))['valor__sum'] or 0
        return total_gasto
    
    total_gasto_pessoa.short_description = 'Total gasto por pessoa'
    
    def total_gasto_geral(self, obj):
        total_gasto = Compra.objects.filter(
            ano_e_mes=obj.ano_e_mes
        ).aggregate(Sum('valor'))['valor__sum'] or 0
        return total_gasto
    
    total_gasto_geral.short_description = 'Total gasto geral'

class RecebimentoAdmin(admin.ModelAdmin):
    list_display = ('ano_e_mes', 'pessoa', 'valor_recebido', 'valor_restante')
    list_filter = (AnoMesFilter,)

    def ano_e_mes(self, obj):
        return f"{obj.ano_e_mes}"

    def pessoa(self, obj):
        return f"{obj.pessoa}"

    def valor_recebido(self, obj):
        return f"{obj.valor_recebido}"

    def valor_restante(self, obj):
        total_gasto = Compra.objects.filter(
            ano_e_mes=obj.ano_e_mes,
            nome=obj.pessoa
        ).aggregate(Sum('valor'))['valor__sum'] or 0
        saldo_restante = obj.valor_recebido - total_gasto
        return saldo_restante

admin.site.register(AnoMes)
admin.site.register(Compra, CompraAdmin)
admin.site.register(Pessoa)
admin.site.register(GastosMensais, GastosMensaisAdmin)
admin.site.register(Recebimento, RecebimentoAdmin)
