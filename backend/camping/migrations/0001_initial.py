# Generated by Django 4.2 on 2023-05-28 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CampingPlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='CampingSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5)),
                ('plot_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('price_per_adult', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price_per_child', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_plate', models.CharField(max_length=25)),
                ('drivers', models.ManyToManyField(related_name='cars', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('number_of_adults', models.SmallIntegerField()),
                ('number_of_children', models.SmallIntegerField()),
                ('number_of_babies', models.SmallIntegerField()),
                ('camping_plot', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='camping.campingplot')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='camping.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('PAYPAL', 'Paypal'), ('PAYU', 'PayU'), ('BLIK', 'BLIK'), ('CC', 'Karta kredytowa'), ('TT', 'Przelew tradycyjny')], max_length=10)),
                ('status', models.CharField(choices=[('WFP', 'Oczekiwanie na płatność'), ('IP', 'W trakcie realizacji'), ('C', 'Anulowana'), ('A', 'Zatwierdzona'), ('R', 'Returned')], default='WFP', max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='camping.reservation')),
            ],
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 'Zły'), (2, 'Średni'), (3, 'Ok'), (4, 'Świetny'), (5, 'Niesamowity')])),
                ('description', models.CharField(blank=True, default='', max_length=500)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('camping_plot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='camping.campingplot')),
            ],
        ),
        migrations.AddField(
            model_name='campingplot',
            name='camping_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camping.campingsection'),
        ),
    ]
