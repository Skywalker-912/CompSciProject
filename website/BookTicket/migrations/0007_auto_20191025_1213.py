# Generated by Django 2.2.6 on 2019-10-25 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookTicket', '0006_auto_20191024_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journey',
            name='PNR_No',
            field=models.CharField(max_length=10),
        ),
    ]
