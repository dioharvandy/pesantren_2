from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.conf import settings
import os

# Create your models here.

class Pendidikan (models.Model):
    id_pendidikan = models.BigAutoField(primary_key=True)
    pendidikan = models.CharField(max_length=50)

    def __str__(self):
        return self.pendidikan

    # class Meta:
    #     db_table = 'pendidikan'

class Jurusan (models.Model):
    id_jurusan = models.BigAutoField(primary_key=True)
    jurusan = models.CharField(max_length=50)

    def __str__(self):
        return self.jurusan

class Universitas (models.Model):
    id_universitas = models.BigAutoField(primary_key=True)
    universitas = models.CharField(max_length=50)
    
    def __str__(self):
        return self.universitas

class Riwayat_pendidikan (models.Model):
    id_riwayat_pendidikan = models.BigAutoField(primary_key=True, default=None)
    nupy = models.ForeignKey('Pegawai', on_delete=models.CASCADE, db_column='nupy' )
    pendidikan = models.ForeignKey(Pendidikan, on_delete=models.CASCADE, default=None)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, default=None)
    universitas = models.ForeignKey(Universitas, on_delete=models.CASCADE, default=None)
    tahun_lulus = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # db_table = 'riwayat_pendidikan'
        unique_together = (("nupy","pendidikan","jurusan","universitas"),)

    def __str__(self):
        return str(self.nupy)

class Pegawai (models.Model):
    nupy =  models.CharField(max_length=50, primary_key=True)
    nama_pegawai = models.CharField(max_length=50)
    JKS = (
        ('L','Laki-laki'),
        ('P','Perempuan')
    )
    jenis_kelamin= CharField(max_length=1, choices=JKS)
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    alamat = models.TextField()
    no_telpon = models.CharField(max_length=13)
    tanggal_masuk = models.DateField()
    foto = models.ImageField(upload_to='fotopegawai/')
    ket_pegawai = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_pegawai
    def delete(self, *args, **kwargs):
        storage = self.foto.storage
        if storage.exists(self.foto.name):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.foto.name))
        super(Pegawai,self).delete(*args,**kwargs)

    # class meta:
    #     db_table = 'pegawai'
    pass

class Surat_mutasi_jabatan (models.Model):
    sk_mutasi_jabatan =  models.CharField(max_length=50, primary_key=True)
    tanggal_mutasi_jabatan = models.DateField()
    ket_mutasi_jabatan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sk_mutasi_jabatan
    # class meta:
    #     db_table = 'surat_mutasi_jabatan'

class Jabatan (models.Model):
    id_jabatan = models.BigAutoField(primary_key=True)
    nama_jabatan =  models.CharField(max_length=50)
    gaji_pokok = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_jabatan
    
    # class meta:
    #     db_table = 'jabatan'

class Detail_jabatan (models.Model):
    id_detail_jabatan = models.BigAutoField(primary_key=True, default=None)
    nupy = models.ForeignKey('Pegawai',  on_delete=models.CASCADE,  db_column='nupy')   
    sk_mutasi_jabatan = models.ForeignKey(Surat_mutasi_jabatan, on_delete=models.CASCADE, db_column='sk_mutasi_jabatan', null=True)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # db_table = 'detail_jabatan'
        unique_together = (("nupy","sk_mutasi_jabatan","jabatan"),)

    STATUS_JABATANS = (
        ('1', 'Aktif'),
        ('2', 'Non Aktif')
    )
    status_jabatan = models.CharField(max_length=1,choices=STATUS_JABATANS, default='1' )

    def __str__(self):
        return str(self.nupy)

class BulanTahun(models.Model):
    id_bulan_tahun = models.BigAutoField(primary_key=True, default=None)
    tahun = models.IntegerField()
    BULANS = (
        ('1','Januari'),('2','Februari'),('3','Maret'),('4','April'),
        ('5','Mei'),('6','Juni'),('7','Juli'),('8','Agustus'),
        ('9','September'),('10','Oktober'),('11','November'),('12','Desember')
    )
    bulan = models.CharField(max_length=2, choices=BULANS, default='1')
    class Meta:
        unique_together = (("bulan","tahun"),)

class Gaji_jabatan (models.Model):
    id_gaji_jabatan = models.BigAutoField(primary_key=True, default=None)
    nupy = models.ForeignKey('Pegawai',  on_delete=models.CASCADE,  db_column='nupy')
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE, default=None)
    bulantahun = models.ForeignKey(BulanTahun, on_delete=models.CASCADE, default=None)
    class Meta:
        # db_table = 'gaji'
        unique_together = (("nupy","jabatan","bulantahun"),)

    kuantitas = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nupy

class Gaji_kualitas (models.Model):
    id_gaji_kualitas = models.BigAutoField(primary_key=True, default=None)
    nupy = models.ForeignKey('Pegawai', on_delete=models.CASCADE, db_column='nupy')
    bulantahun = models.ForeignKey(BulanTahun, on_delete=models.CASCADE, default=None)
    ekskul = models.IntegerField(default=None)
    kinerja = models.IntegerField()
    tunjangan = models.IntegerField()
    ket_gaji = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # db_table = 'gaji'
        unique_together = (("nupy","bulantahun"),)

    def __str__(self):
        return self.nupy