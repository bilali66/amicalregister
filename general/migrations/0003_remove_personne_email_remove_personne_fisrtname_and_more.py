# Generated by Django 5.0.6 on 2024-05-26 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personne',
            name='email',
        ),
        migrations.RemoveField(
            model_name='personne',
            name='fisrtname',
        ),
        migrations.RemoveField(
            model_name='personne',
            name='lastname',
        ),
    ]
