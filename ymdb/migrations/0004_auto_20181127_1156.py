# Generated by Django 2.1.3 on 2018-11-27 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ymdb', '0003_auto_20181126_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artobject',
            name='ArtBlocks',
            field=models.IntegerField(blank=True, default=1, verbose_name='Томов / Сезонов (и т.п)'),
        ),
        migrations.AlterField(
            model_name='artobject',
            name='ArtParts',
            field=models.IntegerField(blank=True, default=1, verbose_name='Эпизодов / Глав (и т.п)'),
        ),
    ]
