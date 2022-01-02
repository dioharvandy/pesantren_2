from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser as User
from django.contrib.admin import AdminSite
from .models import Detail_jabatan, Gaji_jabatan, Gaji_kualitas, Jabatan,Pendidikan, Riwayat_pendidikan, Surat_mutasi_jabatan,Pegawai, Universitas, Jurusan
# Register your models here.

class CustomUserAdmin(UserAdmin):
    # ...

    list_display = ('user_name', 'nama', 'is_active', 'is_staff','is_esp','is_superuser')

    def user_name(self, obj):
        return obj.username
    user_name.short_description  = "Identitas"

    exclude = ('email','user_permissions','groups',)
    fieldsets = (
        ('Data Pribadi', {'fields': ('nama', 'password')}),
        ('Tanggal Penting', {'fields': ('last_login', 'date_joined')}),
        ('Hak Akses', {'fields': ('is_active', 'is_staff','is_esp', 'is_superuser')}),
    )
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
