# Generated by Django 3.2.3 on 2021-10-05 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kepegawaian', '0011_auto_20211004_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riwayat_pendidikan',
            name='tahun_lulus',
            field=models.DateField(null=True),
        ),
    ]
