# Generated by Django 4.2 on 2024-11-21 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='duration',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
