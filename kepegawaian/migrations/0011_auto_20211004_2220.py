# Generated by Django 3.2.3 on 2021-10-04 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kepegawaian', '0010_alter_pegawai_alamat'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cuti',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='cuti',
            name='nupy',
        ),
        migrations.RemoveField(
            model_name='cuti',
            name='surat',
        ),
        migrations.AlterUniqueTogether(
            name='surat_mutasi_keluar',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='surat_mutasi_keluar',
            name='nupy',
        ),
        migrations.AlterUniqueTogether(
            name='surat_pensiun',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='surat_pensiun',
            name='nupy',
        ),
        migrations.RemoveField(
            model_name='pegawai',
            name='lembaga',
        ),
        migrations.RemoveField(
            model_name='pegawai',
            name='status_pegawai',
        ),
        migrations.AddField(
            model_name='gaji',
            name='ekskul',
            field=models.IntegerField(default=None),
        ),
        migrations.DeleteModel(
            name='Absensi',
        ),
        migrations.DeleteModel(
            name='Cuti',
        ),
        migrations.DeleteModel(
            name='Lembaga',
        ),
        migrations.DeleteModel(
            name='Surat_cuti',
        ),
        migrations.DeleteModel(
            name='Surat_mutasi_keluar',
        ),
        migrations.DeleteModel(
            name='Surat_pensiun',
        ),
        migrations.DeleteModel(
            name='Tanggal_absen',
        ),
    ]