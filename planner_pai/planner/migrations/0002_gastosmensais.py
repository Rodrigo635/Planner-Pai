# Generated by Django 4.2.4 on 2023-08-10 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GastosMensais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_gasto', models.IntegerField(default=0)),
                ('numero_de_compras', models.PositiveIntegerField(default=0)),
                ('ano_e_mes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.anomes')),
                ('nome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.pessoa')),
            ],
            options={
                'verbose_name': 'Gasto Mensal',
                'verbose_name_plural': 'Gastos Mensais',
            },
        ),
    ]
