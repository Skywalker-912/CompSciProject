# Generated by Django 2.2.6 on 2019-11-07 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookTicket', '0008_journey_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.IntegerField()),
                ('msg', models.CharField(max_length=150)),
            ],
        ),
    ]