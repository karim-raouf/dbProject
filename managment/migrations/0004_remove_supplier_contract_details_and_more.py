# Generated by Django 5.1.4 on 2025-01-05 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managment', '0003_supplier_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='contract_details',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='restock_terms',
        ),
        migrations.AddField(
            model_name='supplier',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='start_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
