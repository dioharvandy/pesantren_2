from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.contrib.admin import AdminSite
from .models import Detail_jabatan, Gaji_jabatan, Gaji_kualitas, Jabatan,Pendidikan, Riwayat_pendidikan, Surat_mutasi_jabatan,Pegawai, Universitas, Jurusan
# Register your models here.

admin.site.unregister(Group)

class CustomUserAdmin(UserAdmin):
    # ...
    exclude = ('groups', 'user_permissions',)
    fieldsets = (
        ('Personal info', {'fields': ('username','first_name','last_name', 'email', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
