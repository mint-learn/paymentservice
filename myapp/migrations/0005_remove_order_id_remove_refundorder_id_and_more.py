# Generated by Django 4.2.1 on 2023-05-10 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_order_from_account_alter_order_to_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.RemoveField(
            model_name='refundorder',
            name='id',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='refundorder',
            name='payment_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='refundorder',
            name='refund_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]