# Generated by Django 3.0.5 on 2020-04-30 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200430_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='price',
            field=models.DecimalField(decimal_places=3, editable=False, max_digits=9),
        ),
    ]
