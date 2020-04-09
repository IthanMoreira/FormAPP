# Generated by Django 3.0.4 on 2020-04-07 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('formulario', '0004_auto_20200406_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulos',
            name='desde',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha desde'),
        ),
        migrations.AlterField(
            model_name='articulos',
            name='hasta',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha hasta'),
        ),
        migrations.AlterField(
            model_name='articulos',
            name='valor_bruto',
            field=models.IntegerField(blank=True, null=True, verbose_name='Precio bruto'),
        ),
        migrations.AlterField(
            model_name='detalleorden',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]