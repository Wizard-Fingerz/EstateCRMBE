# Generated by Django 5.0.1 on 2024-01-29 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_delete_prospect'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contact',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='no_of_followup',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='no_of_wins',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
