# Generated by Django 3.1 on 2020-08-16 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200816_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.CharField(choices=[('250g', '250g'), ('400g', '400g'), ('1000g', '1000g')], max_length=200, null=True),
        ),
    ]
