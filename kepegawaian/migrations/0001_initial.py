# Generated by Django 3.2.3 on 2021-06-20 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jabatan',
            fields=[
                ('id_jabatan', models.BigAutoField(primary_key=True, serialize=False)),
                ('nama_jabatan', models.CharField(max_length=25)),
                ('gaji_pokok', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Jurusan',
            fields=[
                ('id_jurusan', models.BigAutoField(primary_key=True, serialize=False)),
                ('jurusan', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Lembaga',
            fields=[
                ('id_lembaga', models.BigAutoField(primary_key=True, serialize=False)),
                ('nama_lembaga', models.CharField(max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pegawai',
            fields=[
                ('nupy', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('nama_pegawai', models.CharField(max_length=50)),
                ('jenis_kelamin', models.CharField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], max_length=1)),
                ('tempat_lahir', models.CharField(max_length=25)),
                ('tanggal_lahir', models.DateField()),
                ('alamat', models.CharField(max_length=50)),
                ('no_telpon', models.CharField(max_length=13)),
                ('tanggal_masuk', models.DateField()),
                ('status_pegawai', models.CharField(choices=[('A', 'Aktif'), ('P', 'Pensiun'), ('K', 'Keluar')], default='A', max_length=1)),
                ('foto', models.ImageField(upload_to='fotopegawai/')),
                ('ket_pegawai', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lembaga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.lembaga')),
            ],
        ),
        migrations.CreateModel(
            name='Pendidikan',
            fields=[
                ('id_pendidikan', models.BigAutoField(primary_key=True, serialize=False)),
                ('pendidikan', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Surat_cuti',
            fields=[
                ('id_surat', models.BigAutoField(primary_key=True, serialize=False)),
                ('no_surat', models.CharField(max_length=25)),
                ('tanggal_surat_cuti', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Surat_mutasi_jabatan',
            fields=[
                ('sk_mutasi_jabatan', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('tanggal_mutasi_jabatan', models.DateField()),
                ('ket_mutasi_jabatan', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tanggal_absen',
            fields=[
                ('id_tanggal_absen', models.BigAutoField(primary_key=True, serialize=False)),
                ('Tanggal_absen', models.DateTimeField(verbose_name='tanggal absen')),
            ],
        ),
        migrations.CreateModel(
            name='Universitas',
            fields=[
                ('id_universitas', models.BigAutoField(primary_key=True, serialize=False)),
                ('universitas', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Surat_pensiun',
            fields=[
                ('id_surat_pensiun', models.BigAutoField(default=None, primary_key=True, serialize=False)),
                ('sk_pensiun', models.CharField(max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tanggal_pensiun', models.DateField()),
                ('usia', models.IntegerField()),
                ('ket_pensiun', models.TextField()),
                ('nupy', models.ForeignKey(db_column='nupy', on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.pegawai')),
            ],
            options={
                'unique_together': {('nupy', 'sk_pensiun')},
            },
        ),
        migrations.CreateModel(
            name='Surat_mutasi_keluar',
            fields=[
                ('id_surat_mutasi_keluar', models.BigAutoField(default=None, primary_key=True, serialize=False)),
                ('sk_mutasi_keluar', models.CharField(max_length=25)),
                ('tanggal_mutasi_keluar', models.DateField()),
                ('ket_mutasi_keluar', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nupy', models.ForeignKey(db_column='nupy', on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.pegawai')),
            ],
            options={
                'unique_together': {('nupy', 'sk_mutasi_keluar')},
            },
        ),
        migrations.CreateModel(
            name='Riwayat_pendidikan',
            fields=[
                ('id_riwayat_pendidikan', models.BigAutoField(default=None, primary_key=True, serialize=False)),
                ('tahun_lulus', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('jurusan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.jurusan')),
                ('nupy', models.ForeignKey(db_column='nupy', on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.pegawai')),
                ('pendidikan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.pendidikan')),
                ('universitas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.universitas')),
            ],
            options={
                'unique_together': {('nupy', 'pendidikan', 'jurusan', 'universitas')},
            },
        ),
        migrations.CreateModel(
            name='Gaji',
            fields=[
                ('id_gaji', models.BigAutoField(default=None, primary_key=True, serialize=False)),
                ('tahun', models.IntegerField()),
                ('bulan', models.CharField(choices=[('Ja', 'Januari'), ('Fe', 'Februari'), ('Ma', 'Maret'), ('Ap', 'April'), ('Me', 'Mei'), ('Jn', 'Juni'), ('Jl', 'Juli'), ('Ag', 'Agustus'), ('Se', 'September'), ('Ok', 'Oktober'), ('No', 'November'), ('De', 'Desember')], default='Ja', max_length=2)),
                ('kuantitas', models.IntegerField()),
                ('kinerja', models.IntegerField()),
                ('tunjangan', models.IntegerField()),
                ('ket_gaji', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('jabatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.jabatan')),
                ('nupy', models.ForeignKey(db_column='nupy', on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.pegawai')),
            ],
            options={
                'unique_together': {('nupy', 'jabatan', 'tahun', 'bulan')},
            },
        ),
        migrations.CreateModel(
            name='Detail_jabatan',
            fields=[
                ('id_detail_jabatan', models.BigAutoField(default=None, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status_jabatan', models.CharField(choices=[('1', 'Aktif'), ('2', 'Non Aktif')], default='1', max_length=1)),
                ('jabatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.jabatan')),
                ('nupy', models.ForeignKey(db_column='nupy', on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.pegawai')),
                ('sk_mutasi_jabatan', models.ForeignKey(db_column='sk_mutasi_jabatan', null=True, on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.surat_mutasi_jabatan')),
            ],
            options={
                'unique_together': {('nupy', 'sk_mutasi_jabatan', 'jabatan')},
            },
        ),
        migrations.CreateModel(
            name='Cuti',
            fields=[
                ('id_cuti', models.BigAutoField(default=None, primary_key=True, serialize=False)),
                ('tanggal_mulai_cuti', models.DateField()),
                ('tanggal_habis_cuti', models.DateField()),
                ('lama_cuti', models.CharField(max_length=3)),
                ('ket_cuti', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nupy', models.ForeignKey(db_column='nupy', on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.pegawai')),
                ('surat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.surat_cuti')),
            ],
            options={
                'unique_together': {('nupy', 'surat', 'tanggal_mulai_cuti')},
            },
        ),
        migrations.CreateModel(
            name='Absensi',
            fields=[
                ('id_absensi', models.BigAutoField(default=None, primary_key=True, serialize=False)),
                ('status_absen', models.CharField(choices=[('H', 'Hadir'), ('I', 'Izin'), ('S', 'Sakit'), ('A', 'Absen')], default='A', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nupy', models.ForeignKey(db_column='nupy', on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.pegawai')),
                ('tanggal_absen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepegawaian.tanggal_absen')),
            ],
            options={
                'unique_together': {('nupy', 'tanggal_absen')},
            },
        ),
    ]
