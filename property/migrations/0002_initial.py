# Generated by Django 5.0.1 on 2024-02-06 06:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='follow_up_marketer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customer',
            name='contact_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.propectcontactsource'),
        ),
        migrations.AddField(
            model_name='followupreport',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property'),
        ),
        migrations.AddField(
            model_name='customer',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Customer_Property', to='property.property'),
        ),
        migrations.AddField(
            model_name='prospect',
            name='follow_up_marketer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prospect',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Property', to='property.property'),
        ),
        migrations.AddField(
            model_name='followupreport',
            name='prospect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.prospect'),
        ),
        migrations.AddField(
            model_name='prospect',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.prospectlocation'),
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.prospectlocation'),
        ),
        migrations.AddField(
            model_name='reportfeedback',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.followupreport'),
        ),
    ]
