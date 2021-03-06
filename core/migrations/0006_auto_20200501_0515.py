# Generated by Django 3.0.5 on 2020-04-30 23:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_auto_20200430_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteCosmetic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cosmetic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='core.Cosmetic')),
                ('profile', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='favorite_cosmetics', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='favoritecosmetic',
            constraint=models.UniqueConstraint(fields=('profile', 'cosmetic'), name='unique_favorite_cosmetics'),
        ),
    ]
