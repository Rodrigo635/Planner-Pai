from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum
from django.db.models import Q

class AnoMes(models.Model):
    class Meta:
        verbose_name = 'Ano e mês'
        verbose_name_plural = 'Anos e meses'
        unique_together = ['ano', 'mes']

    ano = models.PositiveIntegerField()
    mes = models.PositiveIntegerField(choices=[
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ])

    def __str__(self):
        return f"{self.get_mes_display()} de {self.ano}"

class Pessoa(models.Model):
    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    pessoa = models.CharField(max_length=100)

    def __str__(self):
        return self.pessoa

class Compra(models.Model):
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    ano_e_mes = models.ForeignKey(AnoMes, on_delete=models.CASCADE)
    nome = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    data_de_inicio = models.DateField('Dia da compra', default=timezone.now)
    compra = models.CharField(max_length=100)
    valor = models.IntegerField()
    parcela_atual = models.PositiveIntegerField(default=1)
    numero_de_parcelas = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.compra}, {self.ano_e_mes}, {self.valor}, {self.parcela_atual}x, {self.numero_de_parcelas}"

class GastosMensais(models.Model):
    class Meta:
        verbose_name = 'Gasto Mensal'
        verbose_name_plural = 'Gastos Mensais'

    ano_e_mes = models.ForeignKey('AnoMes', on_delete=models.CASCADE)
    nome = models.ForeignKey('Pessoa', on_delete=models.CASCADE, null=True, blank=True)
    total_gasto = models.IntegerField(default=0)
    numero_de_compras = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Gastos de {self.ano_e_mes} - {self.nome}"

@receiver(post_save, sender=Compra)
def criar_gasto_mensal(sender, instance, created, **kwargs):
    if created:
        # Obter o ano e mês da compra
        ano_e_mes = instance.ano_e_mes

        # Obter a pessoa associada à compra
        pessoa = instance.nome

        # Obter o total gasto da pessoa para o mesmo AnoMes
        total_gasto_pessoa = Compra.objects.filter(
            ano_e_mes=ano_e_mes,
            nome=pessoa
        ).aggregate(Sum('valor'))['valor__sum'] or 0

        # Verificar se já existe um GastoMensal para a mesma pessoa e AnoMes
        gasto_mensal, created = GastosMensais.objects.get_or_create(
            ano_e_mes=ano_e_mes,
            nome=pessoa
        )

        # Atualizar o total gasto e número de compras no GastoMensal da pessoa
        gasto_mensal.total_gasto = total_gasto_pessoa
        gasto_mensal.numero_de_compras = Compra.objects.filter(
            ano_e_mes=ano_e_mes,
            nome=pessoa
        ).count()

        # Salvar os valores calculados
        gasto_mensal.save()
