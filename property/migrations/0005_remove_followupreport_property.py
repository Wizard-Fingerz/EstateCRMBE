# Generated by Django 5.0.1 on 2024-04-05 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_alter_followupreport_action_plan_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followupreport',
            name='property',
        ),
    ]