# Generated by Django 4.2.4 on 2023-08-19 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0005_alter_compra_valor_alter_gastosmensais_total_gasto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recebimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_recebido', models.FloatField()),
                ('ano_e_mes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.anomes')),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.pessoa')),
            ],
            options={
                'verbose_name': 'Recebimento',
                'verbose_name_plural': 'Recebimentos',
            },
        ),
    ]
