# Generated by Django 4.2.1 on 2023-05-10 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('balance', models.FloatField()),
                ('email', models.EmailField(max_length=255)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RefundOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_time', models.CharField(max_length=255)),
                ('payment_time', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('refund_id', models.CharField(max_length=255)),
                ('payment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.order')),
            ],
        ),
    ]
