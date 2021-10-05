from django.urls import path
from django.utils import timezone, dateformat
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'kepegawaian'
now = timezone.localtime(timezone.now()).strftime("%d%m%Y%H%M%S")

urlpatterns = [
    # path('tp', views.tp.as_view(), name='tp'),

    path('', views.PegawaiIndexView.as_view(), name='indexPegawai'),
    path('addpegawai', views.addpegawai, name='addPegawai'),
    path('deletepegawai/<str:pk>', views.deletepegawai, name='deletePegawai'),
    path('printpegawai'+now, views.PegawaiPrintView.as_view(), name='printPegawai'),
    path('detailpegawai/<str:pk>', views.PegawaiDetailView.as_view(), name='detailPegawai'),
    path('editpegawai', views.editpegawai, name='editPegawai'),

    path('daftarjabatan', views.DetailJabatanIndexView.as_view(), name='indexDetailJabatan'),
    path('adddetailjabatan', views.adddetailjabatan, name='addDetailJabatan'),
    path('adddetailjabatanwithsk', views.adddetailjabatanwithsk, name='addDetailJabatanWithSk'),
    path('detailpegawai/detailjabatan/<str:pk>', views.DetailJabatanDetailView.as_view(), name='detailDetailJabatan'),
    path('deletedetailjabatan', views.deletedetailjabatan, name='deleteDetailJabatan'),
    path('editdetailjabatan', views.editdetailjabatan, name='editDetailJabatan'),
    path('printjabatan'+now, views.DetailJabatanPrintView.as_view(), name='printDetailJabatan'),

    path('daftarriwayatpendidikan', views.RiwayatPendidikanIndexView.as_view(), name='indexRiwayatPendidikan'),
    path('addriwayatpendidikan', views.addriwayatpendidikan, name='addRiwayatPendidikan'),
    path('deleteriwayatpendidikan', views.deleteriwayatpendidikan, name='deleteRiwayatPendidikan'),
    path('printriwayatpendidikan'+now, views.RiwayatPendidikanPrintView.as_view(), name='printRiwayatPendidikan'),

    path('skmutasijabatan', views.SkMutasiJabatanIndexView.as_view(), name='indexSkMutasiJabatan'),
    path('addskmutasijabatan', views.addskmutasijabatan, name='addSkMutasiJabatan'),
    path('deleteskmutasijabatan/<str:pk>', views.deleteskmutasijabatan, name='deleteSkMutasiJabatan'),
    path('detailskmutasijabatan/<str:pk>', views.SkMutasiJabatanDetailView.as_view(), name='detailSkMutasiJabatan'),

    path('ajax/load-jabatans/', views.load_jabatans, name='ajax_load_jabatans'),
    path('ajax/load-jabatans1/', views.load_jabatans1, name='ajax_load_jabatans1'),

    path('gajipegawai', views.BulanTahunIndexView.as_view(), name='indexBulanTahun'),
    path('addbulantahun', views.addbulantahun, name='addBulanTahun'),
    path('deletebulan-tahun/<int:pk>', views.deletebulantahun, name='deleteBulanTahun'),
    path('detailgajipegawai/<int:pk>', views.BulanTahunDetailView.as_view(), name='detailGaji'),

    path('addgaji', views.addgaji, name='addGaji'),
    path('deletegaji', views.deletegaji, name='deleteGaji'),
    path('gaji/detailgaji/detailgajipegawai', views.detailgaji, name='detailGajiPegawai'),
    path('printdetailgaji'+now, views.detailgajiPrintView, name='printDetailGajiPegawai'),

# -------------------------------------------------------MAIN DATA ---------------------------------------------------------------------

    path('pendidikan', views.PendidikanIndexView.as_view(), name='indexPendidikan'),
    path('addpendidikan', views.addpendidikan, name='addPendidikan'),
    path('deletependidikan/<str:pk>', views.deletependidikan, name='deletePendidikan'),
    path('detailpendidikan/<str:pk>', views.PendidikanDetailView.as_view(), name='detailPendidikan'),
    path('editpendidikan', views.editpendidikan, name='editPendidikan'),

    path('jurusan', views.JurusanIndexView.as_view(), name='indexJurusan'),
    path('addjurusan', views.addjurusan, name='addJurusan'),
    path('deletejurusan/<str:pk>', views.deletejurusan, name='deleteJurusan'),
    path('detailjurusan/<str:pk>', views.JurusanDetailView.as_view(), name='detailJurusan'),
    path('editjurusan', views.editjurusan, name='editJurusan'),

    path('universitas', views.UniversitasIndexView.as_view(), name='indexUniversitas'),
    path('adduniversitas', views.adduniversitas, name='addUniversitas'),
    path('deleteuniversitas/<str:pk>', views.deleteuniversitas, name='deleteUniversitas'),
    path('detailuniversitas/<str:pk>', views.UniversitasDetailView.as_view(), name='detailUniversitas'),
    path('edituniversitas', views.edituniversitas, name='editUniversitas'),

    path('jabatan', views.JabatanIndexView.as_view(), name='indexJabatan'),
    path('addjabatan', views.addjabatan, name='addJabatan'),
    path('deletejabatan/<str:pk>', views.deletejabatan, name='deleteJabatan'),
    path('detailjabatan/<str:pk>', views.JabatanDetailView.as_view(), name='detailJabatan'),
    path('editjabatan', views.editjabatan, name='editJabatan'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)