from django.urls import path
from django.utils import timezone, dateformat
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'kepegawaian'
now = timezone.localtime(timezone.now()).strftime("%d%m%Y%H%M%S")

urlpatterns = [

    path('', views.login, name='indexLogin'),
    path('home', views.home, name='indexHome'),
    
    path('daftarpegawai', login_required(views.PegawaiIndexView.as_view(), login_url='../admin/login'), name='indexPegawai'),
    path('addpegawai', views.addpegawai, name='addPegawai'),
    path('deletepegawai/<str:pk>', views.deletepegawai, name='deletePegawai'),
    path('printpegawai'+now, login_required(views.PegawaiPrintView.as_view(), login_url='../admin/login'), name='printPegawai'),
    path('detailpegawai/<str:pk>', login_required(views.PegawaiDetailView.as_view(), login_url='../admin/login'), name='detailPegawai'),
    path('editpegawai', views.editpegawai, name='editPegawai'),

    # path('daftarjabatan', views.DetailJabatanIndexView.as_view(), name='indexDetailJabatan'),
    path('adddetailjabatan', views.adddetailjabatan, name='addDetailJabatan'),
    path('adddetailjabatanwithsk', views.adddetailjabatanwithsk, name='addDetailJabatanWithSk'),
    path('detailpegawai/detailjabatan/<str:pk>', login_required(views.DetailJabatanDetailView.as_view(), login_url='../admin/login'), name='detailDetailJabatan'),
    path('deletedetailjabatan', views.deletedetailjabatan, name='deleteDetailJabatan'),
    path('editdetailjabatan', views.editdetailjabatan, name='editDetailJabatan'),
    # path('printjabatan'+now, views.DetailJabatanPrintView.as_view(), name='printDetailJabatan'),

    # path('daftarriwayatpendidikan', views.RiwayatPendidikanIndexView.as_view(), name='indexRiwayatPendidikan'),
    path('addriwayatpendidikan', views.addriwayatpendidikan, name='addRiwayatPendidikan'),
    path('deleteriwayatpendidikan', views.deleteriwayatpendidikan, name='deleteRiwayatPendidikan'),
    # path('printriwayatpendidikan'+now, views.RiwayatPendidikanPrintView.as_view(), name='printRiwayatPendidikan'),

    path('skmutasijabatan', login_required(views.SkMutasiJabatanIndexView.as_view(), login_url='../admin/login'), name='indexSkMutasiJabatan'),
    path('addskmutasijabatan', views.addskmutasijabatan, name='addSkMutasiJabatan'),
    path('deleteskmutasijabatan/<str:pk>', views.deleteskmutasijabatan, name='deleteSkMutasiJabatan'),
    path('detailskmutasijabatan/<str:pk>', login_required(views.SkMutasiJabatanDetailView.as_view(), login_url='../admin/login'), name='detailSkMutasiJabatan'),

    path('ajax/load-jabatans/', views.load_jabatans, name='ajax_load_jabatans'),
    path('ajax/load-jabatans1/', views.load_jabatans1, name='ajax_load_jabatans1'),

    path('gajipegawai', login_required(views.BulanTahunIndexView.as_view(), login_url='../admin/login'), name='indexBulanTahun'),
    path('addbulantahun', views.addbulantahun, name='addBulanTahun'),
    path('deletebulan-tahun/<int:pk>', views.deletebulantahun, name='deleteBulanTahun'),
    path('detailgajipegawai/<int:pk>', login_required(views.BulanTahunDetailView.as_view(), login_url='../admin/login'), name='detailGaji'),

    path('addgaji', views.addgaji, name='addGaji'),
    path('deletegaji', views.deletegaji, name='deleteGaji'),
    path('gaji/detailgaji/detailgajipegawai', views.detailgaji, name='detailGajiPegawai'),
    path('printdetailgaji'+now, views.detailgajiPrintView, name='printDetailGajiPegawai'),

# -------------------------------------------------------MAIN DATA ---------------------------------------------------------------------

    path('pendidikan', login_required(views.PendidikanIndexView.as_view(), login_url='../admin/login'), name='indexPendidikan'),
    path('addpendidikan', views.addpendidikan, name='addPendidikan'),
    path('deletependidikan/<str:pk>', views.deletependidikan, name='deletePendidikan'),
    path('detailpendidikan/<str:pk>', login_required(views.PendidikanDetailView.as_view(), login_url='../admin/login'), name='detailPendidikan'),
    path('editpendidikan', views.editpendidikan, name='editPendidikan'),

    path('jurusan', login_required(views.JurusanIndexView.as_view(), login_url='../admin/login'), name='indexJurusan'),
    path('addjurusan', views.addjurusan, name='addJurusan'),
    path('deletejurusan/<str:pk>', views.deletejurusan, name='deleteJurusan'),
    path('detailjurusan/<str:pk>', login_required(views.JurusanDetailView.as_view(), login_url='../admin/login'), name='detailJurusan'),
    path('editjurusan', views.editjurusan, name='editJurusan'),

    path('universitas', login_required(views.UniversitasIndexView.as_view(), login_url='../admin/login'), name='indexUniversitas'),
    path('adduniversitas', views.adduniversitas, name='addUniversitas'),
    path('deleteuniversitas/<str:pk>', views.deleteuniversitas, name='deleteUniversitas'),
    path('detailuniversitas/<str:pk>', login_required(views.UniversitasDetailView.as_view(), login_url='../admin/login'), name='detailUniversitas'),
    path('edituniversitas', views.edituniversitas, name='editUniversitas'),

    path('jabatan', login_required(views.JabatanIndexView.as_view(), login_url='../admin/login'), name='indexJabatan'),
    path('addjabatan', views.addjabatan, name='addJabatan'),
    path('deletejabatan/<str:pk>', views.deletejabatan, name='deleteJabatan'),
    path('detailjabatan/<str:pk>', login_required(views.JabatanDetailView.as_view(), login_url='../admin/login'), name='detailJabatan'),
    path('editjabatan', views.editjabatan, name='editJabatan'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)