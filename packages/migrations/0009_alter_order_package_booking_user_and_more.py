# Generated by Django 5.1.1 on 2025-03-07 11:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0008_alter_order_payment_id_alter_tourpackage_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.package'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='booking',
            name='no_of_people',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.DeleteModel(
            name='TourPackage',
        ),
    ]
