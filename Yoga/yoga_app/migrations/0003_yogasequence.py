# Generated by Django 5.1.1 on 2024-10-12 15:18

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yoga_app', '0002_remove_yogapose_image_path_yogapose_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='YogaSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('duration', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('poses', models.ManyToManyField(related_name='sequences', to='yoga_app.yogapose')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
