# Generated by Django 4.2.4 on 2023-08-10 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0003_alter_anomes_ano_alter_anomes_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastosmensais',
            name='nome',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planner.pessoa'),
        ),
    ]
