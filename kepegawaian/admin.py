from django.contrib import admin
from .models import Detail_jabatan, Gaji_jabatan, Gaji_kualitas, Jabatan,Pendidikan, Riwayat_pendidikan, Surat_mutasi_jabatan,Pegawai, Universitas, Jurusan
# Register your models here.



admin.site.register(Jabatan)
admin.site.register(Pegawai)
admin.site.register(Pendidikan)
admin.site.register(Jurusan)
admin.site.register(Universitas)
admin.site.register(Gaji_jabatan)
admin.site.register(Gaji_kualitas)
admin.site.register(Surat_mutasi_jabatan)
admin.site.register(Detail_jabatan)
admin.site.register(Riwayat_pendidikan)