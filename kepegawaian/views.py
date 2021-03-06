from typing import Annotated
from django.db.models.expressions import Subquery
from django.views import generic
from django.http import HttpResponse,HttpResponseRedirect, request
from .models import CustomUser as User
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .utils import render_to_pdf 
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import BulanTahun, Gaji_jabatan, Gaji_kualitas, Jabatan, Jurusan, Pegawai, Pendidikan,Surat_mutasi_jabatan, Detail_jabatan, Riwayat_pendidikan, Universitas

# Create your views here.

def login(request):
    return redirect('pegawai/home')

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


@login_required(login_url='../admin/login')
def home(request):
    return render(request, 'kepegawaian/home.html')

# PEGAWAI
class PegawaiIndexView(generic.ListView):
    model = Pegawai
    template_name = 'kepegawaian/pegawai/index.html'
    paginate_by = 50

    # def get_context_data(self, **kwargs):
    #     context = super(PegawaiIndexView, self).get_context_data(**kwargs)
    #     context['lembaga_list'] = Lembaga.objects.all()
    #     return context

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            return Pegawai.objects.filter(Q(nama_pegawai__icontains = search) | Q(nupy__icontains = search) | Q(tempat_lahir__icontains = search) |
            Q(tanggal_lahir__icontains = search) | Q(alamat__icontains = search) | Q(no_telpon__icontains = search) | 
            Q(tanggal_masuk__icontains = search)).order_by('tanggal_masuk')
        else:
            return Pegawai.objects.order_by('tanggal_masuk')

class PegawaiDetailView(SuperuserRequiredMixin, generic.DetailView):
    model = Pegawai
    template_name = 'kepegawaian/pegawai/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PegawaiDetailView, self).get_context_data(**kwargs)
        context['jabatans'] = Detail_jabatan.objects.filter(nupy=self.get_object()).order_by("status_jabatan","-sk_mutasi_jabatan")
        context['pendidikans'] = Riwayat_pendidikan.objects.filter(nupy=self.get_object())
        context['pendidikan_list'] = Pendidikan.objects.order_by('pendidikan')
        context['jurusan_list'] = Jurusan.objects.order_by('jurusan')
        context['universitas_list'] = Universitas.objects.order_by('universitas')
        context['jabatan_list'] = Jabatan.objects.order_by('nama_jabatan','gaji_pokok')
        return context

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def addpegawai(request):
    if request.method == "POST":
        nupy = request.POST['nupy1'].upper()+request.POST['nupy2']+request.POST['nupy3']+request.POST['nupy4']

        if Pegawai.objects.filter(nupy=nupy).exists():
            messages.warning(request, 'Data Pegawai Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))
        else:
            if 'foto' in request.FILES:
                foto = request.FILES['foto']
            else:
                foto = False
            user = User.objects.create_user(username = nupy, password = request.POST['no_telpon'], nama = request.POST['nama_pegawai'], is_staff = True )
            user.save()
            nama = User.objects.get(username = nupy)
            savepegawai = Pegawai(nama_pegawai = request.POST['nama_pegawai'].title() ,nupy = nupy, user = nama, jenis_kelamin = request.POST['jenis_kelamin'] ,
                            tempat_lahir = request.POST['tempat_lahir'] ,tanggal_lahir = request.POST['tanggal_lahir'] ,alamat = request.POST['alamat'].title() ,
                            no_telpon = request.POST['no_telpon'] ,tanggal_masuk = request.POST['tanggal_masuk'],
                            foto = foto ,ket_pegawai = request.POST['ket_pegawai'])    
            savepegawai.save()
            messages.success(request, 'Data Pegawai Berhasil Ditambahkan.', extra_tags='primary')
            return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def editpegawai(request):
    if request.method == "POST":
        updatepegawai = Pegawai.objects.filter(nupy = request.POST["nupy"])
        if 'foto' in request.FILES:
            foto = Pegawai.objects.get(nupy = request.POST["nupy"])
            foto.foto.delete()
            foto.foto = request.FILES['foto']
            foto.save()
        else:
            foto = False
        updatepegawai.update(nupy = request.POST["nupy"],nama_pegawai = request.POST['nama_pegawai'].title()  ,jenis_kelamin = request.POST['jenis_kelamin'] ,
                         tempat_lahir = request.POST['tempat_lahir'] ,tanggal_lahir = request.POST['tanggal_lahir'] ,alamat = request.POST['alamat'].title() ,
                         no_telpon = request.POST['no_telpon'] ,tanggal_masuk = request.POST['tanggal_masuk'],
                         ket_pegawai = request.POST['ket_pegawai'])
        messages.warning(request, 'Data Pegawai Berhasil Diubah.', extra_tags='warning')
        return HttpResponseRedirect(reverse('kepegawaian:detailPegawai', args=(request.POST['nupy'],)))

    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def deletepegawai(request, pk):
    pegawai = get_object_or_404(Pegawai, pk=pk)
    pegawai.delete()
    user = get_object_or_404(User, username=pk)
    user.delete()
    messages.warning(request, 'Data Pegawai Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))
# END PEGAWAI

# RIWAYAT PENDIDIKAN
# class RiwayatPendidikanIndexView(generic.ListView):
#     model = Riwayat_pendidikan
#     template_name = 'kepegawaian/detail_pegawai/riwayatpendidikan.html'
#     paginate_by = 50
#     def get_queryset(self):
#         search = self.request.GET.get('search')
#         if search:
#             return Riwayat_pendidikan.objects.filter( Q(nupy__nama_pegawai__icontains = search) | Q(nupy__nupy__icontains = search)).order_by("nupy")
#         else:
#             return Riwayat_pendidikan.objects.order_by("nupy")

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def addriwayatpendidikan(request):
    if request.method == "POST":
        nup =  request.POST['nupy']
        nupy = Pegawai.objects.get(nupy = nup)
        try:
            if not request.POST['tahun_lulus']:
                saveriwayat = Riwayat_pendidikan(nupy =nupy, pendidikan_id = request.POST['pendidikan'], jurusan_id = request.POST['jurusan'],
                                             universitas_id = request.POST['universitas'], tahun_lulus = None)
            else:
                tahun_lulus = request.POST['tahun_lulus']
                saveriwayat = Riwayat_pendidikan(nupy =nupy, pendidikan_id = request.POST['pendidikan'], jurusan_id = request.POST['jurusan'],
                                             universitas_id = request.POST['universitas'], tahun_lulus = tahun_lulus)
            saveriwayat.save()
            messages.success(request, 'Data Riwayat Pendidikan Pegawai Berhasil Ditambahkan.', extra_tags='primary')
            return HttpResponseRedirect(reverse('kepegawaian:detailPegawai', args=(request.POST['nupy'],)))
        except IntegrityError:
            if 'unique constraint':
                messages.warning(request, 'Data Riwayat Pendidikan Pegawai Sudah Ada.', extra_tags='danger')
                return HttpResponseRedirect(reverse('kepegawaian:detailPegawai', args=(request.POST['nupy'],)))
        except ValidationError:
                messages.warning(request, 'Data Riwayat Pendidikan Pegawai yang Dimasukan Salah.', extra_tags='danger')
                return HttpResponseRedirect(reverse('kepegawaian:detailPegawai', args=(request.POST['nupy'],)))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def deleteriwayatpendidikan(request):
    if request.method == "POST":
        pendidikan = get_object_or_404(Riwayat_pendidikan, pk=request.POST['pendidikan'])
        pendidikan.delete()
        messages.warning(request, 'Data Riwayat Pendidikan Pegawai Berhasil Dihapus.', extra_tags='danger')
        return HttpResponseRedirect(reverse('kepegawaian:detailPegawai', args=(request.POST['nupy'],)))
    else:
       return HttpResponseRedirect(reverse('kepegawaian:indexPegawai')) 
# END RIWAYAT PENDIDIKAN

# DETAIL JABATAN
# class DetailJabatanIndexView(generic.ListView):
#     model = Detail_jabatan
#     template_name = 'kepegawaian/detail_pegawai/detailjabatan.html'
#     paginate_by = 50

#     def get_queryset(self):
#         search = self.request.GET.get('search')
#         if search:
#             return Detail_jabatan.objects.filter( Q(nupy__nama_pegawai__icontains = search) | Q(nupy__nupy__icontains = search) & Q(status_jabatan="1")).order_by("nupy")
#         else:
#             return Detail_jabatan.objects.filter(status_jabatan="1").order_by("nupy")

class DetailJabatanDetailView(SuperuserRequiredMixin, generic.DetailView):
    model = Detail_jabatan
    template_name = 'kepegawaian/pegawai/detailjabatan.html'

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def adddetailjabatan(request):
    if request.method == "POST":
        nupy = Pegawai.objects.get(nupy = request.POST['nupy'])

        if Detail_jabatan.objects.filter(Q(nupy=request.POST['nupy']) & Q(jabatan_id = request.POST['jabatan']) & Q(status_jabatan ="1")).exists():
            messages.warning(request, 'Data jabatan Pegawai Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:detailPegawai', args=(request.POST['nupy'],)))
        else:
            savedetailjabatan =Detail_jabatan(nupy = nupy, jabatan_id = request.POST['jabatan'], status_jabatan ="1")
            savedetailjabatan.save()
            messages.success(request, 'Data jabatan Pegawai Berhasil Ditambahkan.', extra_tags='primary')
            return HttpResponseRedirect(reverse('kepegawaian:detailPegawai', args=(request.POST['nupy'],)))

    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def adddetailjabatanwithsk(request):
    if request.method == "POST":
        nupy = Pegawai.objects.get(nupy = request.POST['nupy'])
        sk_mutasi_jabatan = Surat_mutasi_jabatan.objects.get(sk_mutasi_jabatan = request.POST['sk_mutasi_jabatan'])

        if request.POST['jabatan_lama'] == request.POST['jabatan_baru']:
           messages.warning(request, 'Data Jabatan Lama dan Jabatan Baru Tidak Boleh Sama.', extra_tags='danger')
           return HttpResponseRedirect(reverse('kepegawaian:detailSkMutasiJabatan', args=(request.POST['sk_mutasi_jabatan'],)))
        
        elif Detail_jabatan.objects.filter(Q(nupy=request.POST['nupy']) & Q(jabatan_id = request.POST['jabatan_baru']) & Q (status_jabatan = '1')).exists():
           messages.warning(request, 'Data Jabatan Baru Sudah Ada.', extra_tags='danger')
           return HttpResponseRedirect(reverse('kepegawaian:detailSkMutasiJabatan', args=(request.POST['sk_mutasi_jabatan'],)))

        else:
            updatestatus = Detail_jabatan.objects.filter(Q(nupy=request.POST['nupy']) & Q(jabatan_id = request.POST['jabatan_lama']))
            updatestatus.update(status_jabatan = "2")
            savedetailjabatan = Detail_jabatan(nupy = nupy, sk_mutasi_jabatan = sk_mutasi_jabatan, jabatan_id = request.POST['jabatan_baru'], status_jabatan = "1")  
            savedetailjabatan.save()
            messages.warning(request, 'Data Jabatan Baru Berhasil Ditambahkan.', extra_tags='primary')
            return HttpResponseRedirect(reverse('kepegawaian:detailSkMutasiJabatan', args=(request.POST['sk_mutasi_jabatan'],)))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def editdetailjabatan(request):
    if request.method == "POST":
        Detail_jabatan.objects.filter(id_detail_jabatan = request.POST['jabatan_id']).update(status_jabatan = request.POST['status_jabatan'])
        messages.success(request, 'Data Status Jabatan Berhasil Diubah.', extra_tags='warning')
        return HttpResponseRedirect(reverse('kepegawaian:detailPegawai', args=(request.POST['nupy'],)))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def deletedetailjabatan(request):
    if request.method == "POST":
        detailjabatan = get_object_or_404(Detail_jabatan, pk=request.POST['jabatan'])
        detailjabatan.delete()
        messages.warning(request, 'Data Jabatan Pegawai Berhasil Dihapus.', extra_tags='danger')

        if 'nupy' in request.POST:
            return HttpResponseRedirect(reverse('kepegawaian:detailPegawai', args=(request.POST['nupy'],)))

        elif 'sk_mutasi_jabatan' in request.POST:
            return HttpResponseRedirect(reverse('kepegawaian:detailSkMutasiJabatan', args=(request.POST['sk_mutasi_jabatan'],)))
    else:
       return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))
# END DETAIL JABATAN

# PRINT TO PDF
class PegawaiPrintView(SuperuserRequiredMixin, generic.View):
     def get(self, request, *args, **kwargs):
        pegawai = Pegawai.objects.order_by('tanggal_masuk')
        # pegawai = Pegawai.objects.all().order_by('status_pegawai','lembaga_id')
        today = timezone.now()
        params = {
            'pegawais':pegawai,
            'today': today,
            'request': request
        }

        pdf = render_to_pdf('kepegawaian/pegawai/pdf.html',params) #getting the template
        return HttpResponse(pdf, content_type='application/pdf')  #rendering the template

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser or u.is_esp)
def gajipegawaiPrintView(request):
    if request.method == "POST":
        bulantahun = BulanTahun.objects.filter(id_bulan_tahun = request.POST["id_bulan_tahun"])
        gaji_kualitas = Pegawai.objects.raw('''
                                        select kepegawaian_pegawai.nama_pegawai, kepegawaian_pegawai.nupy,
                                        kepegawaian_jabatan.nama_jabatan, kepegawaian_jabatan.gaji_pokok, kepegawaian_gaji_jabatan.kuantitas,
                                        kepegawaian_jabatan.gaji_pokok*kepegawaian_gaji_jabatan.kuantitas as gaji_jabatan,
                                        kepegawaian_gaji_kualitas.ekskul,kepegawaian_gaji_kualitas.kinerja,kepegawaian_gaji_kualitas.tunjangan,
                                        totalgaji.jumlah_gaji, totalgaji.total_gaji
                                        from
                                        (select kepegawaian_pegawai.nupy,
                                        SUM(kepegawaian_jabatan.gaji_pokok*kepegawaian_gaji_jabatan.kuantitas)+
                                        (kepegawaian_gaji_kualitas.ekskul+kepegawaian_gaji_kualitas.kinerja)
                                        as jumlah_gaji,
                                        SUM(kepegawaian_jabatan.gaji_pokok*kepegawaian_gaji_jabatan.kuantitas)+
                                        (kepegawaian_gaji_kualitas.ekskul+kepegawaian_gaji_kualitas.kinerja+kepegawaian_gaji_kualitas.tunjangan)
                                        as total_gaji from kepegawaian_pegawai
                                        join kepegawaian_gaji_jabatan on kepegawaian_gaji_jabatan.nupy = kepegawaian_pegawai.nupy
                                        join kepegawaian_jabatan on kepegawaian_jabatan.id_jabatan = kepegawaian_gaji_jabatan.jabatan_id
                                        join kepegawaian_gaji_kualitas on kepegawaian_gaji_kualitas.nupy = kepegawaian_pegawai.nupy
                                        where kepegawaian_gaji_jabatan.bulantahun_id = %s and kepegawaian_gaji_kualitas.bulantahun_id =  %s 
                                        group by kepegawaian_pegawai.nupy) totalgaji, kepegawaian_pegawai
                                        join kepegawaian_gaji_jabatan on kepegawaian_gaji_jabatan.nupy = kepegawaian_pegawai.nupy
                                        join kepegawaian_jabatan on kepegawaian_jabatan.id_jabatan = kepegawaian_gaji_jabatan.jabatan_id
                                        join kepegawaian_gaji_kualitas on kepegawaian_gaji_kualitas.nupy = kepegawaian_pegawai.nupy
                                        where kepegawaian_gaji_jabatan.bulantahun_id =  %s and kepegawaian_gaji_kualitas.bulantahun_id =  %s
                                        and kepegawaian_pegawai.nupy = totalgaji.nupy       
                                        ''', [request.POST["id_bulan_tahun"],request.POST["id_bulan_tahun"],request.POST["id_bulan_tahun"],request.POST["id_bulan_tahun"]])
        today = timezone.now()
        params = {
            'gaji_kualitass': gaji_kualitas,
            'today': today,
            'bulantahuns': bulantahun,
            'request': request
        }                                
        pdf = render_to_pdf('kepegawaian/gaji/pdfgaji.html',params) #getting the template
        return HttpResponse(pdf, content_type='application/pdf')  #rendering the template
    else:
       return HttpResponseRedirect(reverse('kepegawaian:indexBulanTahun'))

@login_required(login_url='../admin/login')
def detailgajiPrintView(request):
    if request.method == "POST":
        gaji_jabatan = Gaji_jabatan.objects.filter(Q(nupy = request.POST["nupy"]) & Q(bulantahun_id = request.POST["id_bulan_tahun"]))
        gaji_kualitas = Gaji_kualitas.objects.filter(Q(nupy = request.POST["nupy"]) & Q(bulantahun_id = request.POST["id_bulan_tahun"]))
        return render(request, 'kepegawaian/gaji/pdfdetailgaji.html', {'gaji_jabatans': gaji_jabatan, 'gaji_kualitass': gaji_kualitas}) 
    else:
       return HttpResponseRedirect(reverse('kepegawaian:indexBulanTahun'))
# END PRINT TO PDF

# TEST DOANG
class tp(generic.ListView):
    model = Pegawai
    template_name = 'kepegawaian/pegawai/pdf.html'
    context_object_name = 'pegawais'
# END TEST DOANG

# SURAT MUTASI JABATAN
class SkMutasiJabatanIndexView(SuperuserRequiredMixin, generic.ListView):
    model = Surat_mutasi_jabatan
    template_name = 'kepegawaian/mutasi_jabatan/index.html'
    paginate_by = 50

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            return Surat_mutasi_jabatan.objects.filter(sk_mutasi_jabatan__icontains = search).order_by("-tanggal_mutasi_jabatan")
        else:
            return Surat_mutasi_jabatan.objects.order_by("-tanggal_mutasi_jabatan")

class SkMutasiJabatanDetailView(SuperuserRequiredMixin, generic.DetailView):
    model = Surat_mutasi_jabatan
    template_name = 'kepegawaian/mutasi_jabatan/detail.html'
    def get_context_data(self, **kwargs):
        context = super(SkMutasiJabatanDetailView, self).get_context_data(**kwargs)
        context['jabatans'] = Detail_jabatan.objects.filter(sk_mutasi_jabatan=self.get_object())
        context['pegawai_list'] = Pegawai.objects.order_by('nama_pegawai')
        context['jabatan_list'] = Jabatan.objects.order_by('nama_jabatan')
        return context

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def addskmutasijabatan(request):
    if request.method == "POST":
        nosk = request.POST["nosk1"]+"-"+request.POST["nosk2"].upper()+"-"+request.POST["nosk3"].upper()+"-"+request.POST["nosk4"].upper()+"-"+request.POST["nosk5"]

        if Surat_mutasi_jabatan.objects.filter(sk_mutasi_jabatan=nosk).exists():
            messages.warning(request, 'Data No Surat Mutasi Jabatan Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:indexSkMutasiJabatan'))
        else:
            if 'file_surat' in request.FILES:
                file_surat = request.FILES['file_surat']
            else:
                file_surat = False
            skmutasijabatan = Surat_mutasi_jabatan(sk_mutasi_jabatan = nosk, tanggal_mutasi_jabatan = request.POST["tanggal_mutasi_jabatan"],
                                                    ket_mutasi_jabatan = request.POST["ket_mutasi_jabatan"], file_surat = file_surat)
            skmutasijabatan.save()
            messages.success(request, 'Data No Surat Mutasi Jabatan Berhasil Ditambahkan.', extra_tags='primary')
            return HttpResponseRedirect(reverse('kepegawaian:indexSkMutasiJabatan'))

    else:
       return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def deleteskmutasijabatan(request, pk):
    skmutasijabatan = get_object_or_404(Surat_mutasi_jabatan, pk=pk)
    skmutasijabatan.delete()
    messages.warning(request, 'Data Surat Mutasi Jabatan Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('kepegawaian:indexSkMutasiJabatan'))
# END SURAT MUTASI JABATAN

# AJAX to Get jabatan lama di surat mutasi jabatan
@login_required(login_url='../admin/login')
def load_jabatans(request):
    nupy = request.GET.get('nupy')
    jabatan = Detail_jabatan.objects.filter(Q(nupy=nupy) & Q(status_jabatan = "1")).all()
    return render(request, 'kepegawaian/mutasi_jabatan/jabatan-dropdown-list.html', {'jabatans': jabatan})

@login_required(login_url='../admin/login')
def load_jabatans1(request):
    nupy = request.GET.get('nupy')
    jabatan = Detail_jabatan.objects.filter(Q(nupy=nupy) & Q(status_jabatan = "1")).all()
    return render(request, 'kepegawaian/gaji/jabatan-input-list.html', {'jabatans': jabatan})
# END AJAX to Get jabatan lama di surat mutasi jabatan

# BULAN TAHUN
class BulanTahunIndexView(generic.ListView):
    model = BulanTahun
    template_name = 'kepegawaian/gaji/index.html'
    paginate_by = 50

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            return BulanTahun.objects.filter(Q(bulan__icontains = search) | Q(tahun__icontains = search)).order_by('bulan', 'tahun')
        else:
            return BulanTahun.objects.order_by('bulan','tahun')

class BulanTahunDetailView(generic.DetailView):
    model = BulanTahun
    template_name = 'kepegawaian/gaji/detail.html'
    # def dispatch(self, *args, **kwargs):
    #     try:
    #         return super(BulanTahunDetailView, self).dispatch(*args, **kwargs)
    #     except ValueError:
    #         return HttpResponseRedirect(reverse('kepegawaian:indexBulanTahun'))
    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search')
        context = super(BulanTahunDetailView, self).get_context_data(**kwargs)
        page_number = self.request.GET.get('page')
        if search:
            context['gaji_kualitass'] = Paginator(Pegawai.objects.raw('''
                                        select kepegawaian_pegawai.nama_pegawai, kepegawaian_pegawai.nupy,
                                        kepegawaian_jabatan.nama_jabatan, kepegawaian_jabatan.gaji_pokok, kepegawaian_gaji_jabatan.kuantitas,
                                        kepegawaian_jabatan.gaji_pokok*kepegawaian_gaji_jabatan.kuantitas as gaji_jabatan,
                                        kepegawaian_gaji_kualitas.ekskul,kepegawaian_gaji_kualitas.kinerja,kepegawaian_gaji_kualitas.tunjangan,
                                        totalgaji.jumlah_gaji, totalgaji.total_gaji
                                        from
                                        (select kepegawaian_pegawai.nupy,
                                        SUM(kepegawaian_jabatan.gaji_pokok*kepegawaian_gaji_jabatan.kuantitas)+
                                        (kepegawaian_gaji_kualitas.ekskul+kepegawaian_gaji_kualitas.kinerja)
                                        as jumlah_gaji,
                                        SUM(kepegawaian_jabatan.gaji_pokok*kepegawaian_gaji_jabatan.kuantitas)+
                                        (kepegawaian_gaji_kualitas.ekskul+kepegawaian_gaji_kualitas.kinerja+kepegawaian_gaji_kualitas.tunjangan)
                                        as total_gaji from kepegawaian_pegawai
                                        join kepegawaian_gaji_jabatan on kepegawaian_gaji_jabatan.nupy = kepegawaian_pegawai.nupy
                                        join kepegawaian_jabatan on kepegawaian_jabatan.id_jabatan = kepegawaian_gaji_jabatan.jabatan_id
                                        join kepegawaian_gaji_kualitas on kepegawaian_gaji_kualitas.nupy = kepegawaian_pegawai.nupy
                                        where kepegawaian_gaji_jabatan.bulantahun_id = %s and kepegawaian_gaji_kualitas.bulantahun_id =  %s
                                        and kepegawaian_pegawai.nupy LIKE %s
                                        group by kepegawaian_pegawai.nupy) totalgaji, kepegawaian_pegawai
                                        join kepegawaian_gaji_jabatan on kepegawaian_gaji_jabatan.nupy = kepegawaian_pegawai.nupy
                                        join kepegawaian_jabatan on kepegawaian_jabatan.id_jabatan = kepegawaian_gaji_jabatan.jabatan_id
                                        join kepegawaian_gaji_kualitas on kepegawaian_gaji_kualitas.nupy = kepegawaian_pegawai.nupy
                                        where kepegawaian_gaji_jabatan.bulantahun_id =  %s and kepegawaian_gaji_kualitas.bulantahun_id =  %s
                                        and kepegawaian_pegawai.nupy = totalgaji.nupy       
                                        ''', [self.kwargs['pk'],self.kwargs['pk'],'%'+search+'%',self.kwargs['pk'],self.kwargs['pk']]),50).get_page(page_number)
        else:
            context['gaji_kualitass'] = Paginator(Pegawai.objects.raw('''
                                        select kepegawaian_pegawai.nama_pegawai, kepegawaian_pegawai.nupy,
                                        kepegawaian_jabatan.nama_jabatan, kepegawaian_jabatan.gaji_pokok, kepegawaian_gaji_jabatan.kuantitas,
                                        kepegawaian_jabatan.gaji_pokok*kepegawaian_gaji_jabatan.kuantitas as gaji_jabatan,
                                        kepegawaian_gaji_kualitas.ekskul,kepegawaian_gaji_kualitas.kinerja,kepegawaian_gaji_kualitas.tunjangan,
                                        totalgaji.jumlah_gaji, totalgaji.total_gaji
                                        from
                                        (select kepegawaian_pegawai.nupy,
                                        SUM(kepegawaian_jabatan.gaji_pokok*kepegawaian_gaji_jabatan.kuantitas)+
                                        (kepegawaian_gaji_kualitas.ekskul+kepegawaian_gaji_kualitas.kinerja)
                                        as jumlah_gaji,
                                        SUM(kepegawaian_jabatan.gaji_pokok*kepegawaian_gaji_jabatan.kuantitas)+
                                        (kepegawaian_gaji_kualitas.ekskul+kepegawaian_gaji_kualitas.kinerja+kepegawaian_gaji_kualitas.tunjangan)
                                        as total_gaji from kepegawaian_pegawai
                                        join kepegawaian_gaji_jabatan on kepegawaian_gaji_jabatan.nupy = kepegawaian_pegawai.nupy
                                        join kepegawaian_jabatan on kepegawaian_jabatan.id_jabatan = kepegawaian_gaji_jabatan.jabatan_id
                                        join kepegawaian_gaji_kualitas on kepegawaian_gaji_kualitas.nupy = kepegawaian_pegawai.nupy
                                        where kepegawaian_gaji_jabatan.bulantahun_id = %s and kepegawaian_gaji_kualitas.bulantahun_id =  %s 
                                        group by kepegawaian_pegawai.nupy) totalgaji, kepegawaian_pegawai
                                        join kepegawaian_gaji_jabatan on kepegawaian_gaji_jabatan.nupy = kepegawaian_pegawai.nupy
                                        join kepegawaian_jabatan on kepegawaian_jabatan.id_jabatan = kepegawaian_gaji_jabatan.jabatan_id
                                        join kepegawaian_gaji_kualitas on kepegawaian_gaji_kualitas.nupy = kepegawaian_pegawai.nupy
                                        where kepegawaian_gaji_jabatan.bulantahun_id =  %s and kepegawaian_gaji_kualitas.bulantahun_id =  %s
                                        and kepegawaian_pegawai.nupy = totalgaji.nupy       
                                        ''', [self.kwargs['pk'],self.kwargs['pk'],self.kwargs['pk'],self.kwargs['pk']]),50).get_page(page_number)
                                            #  annotate(gaji_jabatan=Sum(F('gaji_jabatan__jabatan__gaji_pokok')*F('gaji_jabatan__kuantitas'))+
                                            #             F('gaji_kualitas__ekskul')+F('gaji_kualitas__kinerja')+F('gaji_kualitas__tunjangan')
        context['pegawai_list'] = Pegawai.objects.order_by('nama_pegawai')
        return context

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser or u.is_esp)
def addbulantahun(request):
    if request.method == "POST":
        try:
            bulantahun = BulanTahun(bulan = request.POST["bulan"], tahun = request.POST["tahun"])
            bulantahun.save()
            messages.success(request, 'Tanggal Penggajian Berhasil Ditambahkan.', extra_tags='primary')
            return HttpResponseRedirect(reverse('kepegawaian:indexBulanTahun'))

        except IntegrityError:
            messages.warning(request, 'Tanggal Penggajian Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:indexBulanTahun'))
    else:
       return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser or u.is_esp)
def deletebulantahun(request, pk):
    bulantahun = get_object_or_404(BulanTahun, pk=pk)
    bulantahun.delete()
    messages.warning(request, 'Tanggal Penggajian Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('kepegawaian:indexBulanTahun'))
# END BULAN TAHUN

# GAJI
@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser or u.is_esp)
def addgaji(request):
    if request.method == "POST":
        nupy = Pegawai.objects.get(nupy = request.POST["nupy"])
        try:
            for x in range(1, int(request.POST["length"])+1):
                gaji_jabatan = Gaji_jabatan(nupy = nupy, bulantahun_id = request.POST["bulantahun"], jabatan_id = request.POST["jabatan"+str(x)], 
                                            kuantitas = request.POST["kuantitas"+str(x)])
                gaji_jabatan.save()
            gaji_kualitas = Gaji_kualitas(nupy = nupy, bulantahun_id = request.POST["bulantahun"], ekskul = request.POST["ekskul"], 
                                          kinerja = request.POST["kinerja"], tunjangan = request.POST["tunjangan"], 
                                          ket_gaji = request.POST["ket_gaji"])
            gaji_kualitas.save()
            messages.success(request, 'Data Gaji Pegawai Berhasil Ditambahkan.', extra_tags='primary')
            return HttpResponseRedirect(reverse('kepegawaian:detailGaji', args=( request.POST["bulantahun"],)))

        except IntegrityError:
            messages.warning(request, 'Data Gaji Pegawai Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:detailGaji', args=( request.POST["bulantahun"],)))
    else:
       return HttpResponseRedirect(reverse('kepegawaian:indexGaji'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser or u.is_esp)
def deletegaji(request):
    if request.method == "POST":
        gaji_jabatan = Gaji_jabatan.objects.filter(Q(nupy = request.POST["nupy"]) & Q(bulantahun_id = request.POST["id_bulan_tahun"]))
        gaji_kualitas = Gaji_kualitas.objects.filter(Q(nupy = request.POST["nupy"]) & Q(bulantahun_id = request.POST["id_bulan_tahun"]))
        gaji_jabatan.delete()
        gaji_kualitas.delete()
        messages.warning(request, 'Data Gaji Pegawai Berhasil Dihapus.', extra_tags='danger')

        return HttpResponseRedirect(reverse('kepegawaian:detailGaji', args=(request.POST['id_bulan_tahun'],)))

    else:
       return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))

@login_required(login_url='../admin/login')
def detailgaji(request):
    if request.method == "POST":
        gaji_jabatan = Gaji_jabatan.objects.filter(Q(nupy = request.POST["nupy"]) & Q(bulantahun_id = request.POST["id_bulan_tahun"]))
        gaji_kualitas = Gaji_kualitas.objects.filter(Q(nupy = request.POST["nupy"]) & Q(bulantahun_id = request.POST["id_bulan_tahun"]))
        return render(request, 'kepegawaian/gaji/detailgajipegawai.html', {'gaji_jabatans': gaji_jabatan, 'gaji_kualitass': gaji_kualitas})    
    else:
       return HttpResponseRedirect(reverse('kepegawaian:indexBulanTahun'))
# END GAJI

# -----------------------------------------------------------MAIN DATA------------------------------------------------------------------

# PENDIDIKAN
class PendidikanIndexView(SuperuserRequiredMixin, generic.ListView):
    model = Pendidikan
    template_name = 'kepegawaian/main_data/pendidikan/index.html'
    paginate_by = 50

class PendidikanDetailView(SuperuserRequiredMixin, generic.DetailView):
    model = Pendidikan
    template_name = 'kepegawaian/main_data/pendidikan/detail.html'

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def addpendidikan(request):
    if request.method == "POST":
        if Pendidikan.objects.filter(pendidikan=request.POST['pendidikan'].upper()).exists():
            messages.warning(request, 'Data Pendidikan Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:indexPendidikan'))
        else:
            savependidikan = Pendidikan(pendidikan = request.POST['pendidikan'].upper())    
            savependidikan.save()
            messages.success(request, 'Data Pendidikan Berhasil Ditambahkan.', extra_tags='primary')
            return HttpResponseRedirect(reverse('kepegawaian:indexPendidikan'))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def editpendidikan(request):
    if request.method == "POST":
        updatependidikan = Pendidikan.objects.filter(id_pendidikan = request.POST["id_pendidikan"])

        if Pendidikan.objects.filter(pendidikan=request.POST['pendidikan'].upper()).exists():
            messages.warning(request, 'Data Pendidikan Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:detailPendidikan', args=(request.POST['id_pendidikan'],)))
        else:
            updatependidikan.update(pendidikan = request.POST['pendidikan'].upper())
            messages.success(request, 'Data Pendidikan Berhasil Diubah.', extra_tags='warning')
            return HttpResponseRedirect(reverse('kepegawaian:indexPendidikan'))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexPegawai'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def deletependidikan(request, pk):
    pendidikan = get_object_or_404(Pendidikan, pk=pk)
    pendidikan.delete()
    messages.warning(request, 'Data Pendidikan Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('kepegawaian:indexPendidikan'))
# END PENDIDIKAN

# JURUSAN
class JurusanIndexView(SuperuserRequiredMixin, generic.ListView):
    model = Jurusan
    template_name = 'kepegawaian/main_data/jurusan/index.html'
    paginate_by = 50

class JurusanDetailView(SuperuserRequiredMixin, generic.DetailView):
    model = Jurusan
    template_name = 'kepegawaian/main_data/jurusan/detail.html'

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def addjurusan(request):
    if request.method == "POST":
        if Jurusan.objects.filter(jurusan=request.POST['jurusan'].upper()).exists():
            messages.warning(request, 'Data Jurusan Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:indexJurusan'))
        else:
            savejurusan = Jurusan(jurusan = request.POST['jurusan'].upper())    
            savejurusan.save()
            messages.success(request, 'Data Jurusan Berhasil Ditambahkan.', extra_tags='primary')
            return HttpResponseRedirect(reverse('kepegawaian:indexJurusan'))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexJurusan'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def editjurusan(request):
    if request.method == "POST":
        updatejurusan = Jurusan.objects.filter(id_jurusan = request.POST["id_jurusan"])

        if Jurusan.objects.filter(jurusan = request.POST['jurusan'].upper()).exists():
            messages.warning(request, 'Data Jurusan Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:detailJurusan', args=(request.POST['id_jurusan'],)))
        else:
            updatejurusan.update(jurusan = request.POST['jurusan'].upper())
            messages.success(request, 'Data Jurusan Berhasil Diubah.', extra_tags='warning')
            return HttpResponseRedirect(reverse('kepegawaian:indexJurusan'))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexJurusan'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def deletejurusan(request, pk):
    jurusan = get_object_or_404(Jurusan, pk=pk)
    jurusan.delete()
    messages.warning(request, 'Data Jurusan Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('kepegawaian:indexJurusan'))
# END JURUSAN

# UNIVERSITAS
class UniversitasIndexView(SuperuserRequiredMixin, generic.ListView):
    model = Universitas
    template_name = 'kepegawaian/main_data/universitas/index.html'
    paginate_by = 50

class UniversitasDetailView(SuperuserRequiredMixin, generic.DetailView):
    model = Universitas
    template_name = 'kepegawaian/main_data/universitas/detail.html'

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def adduniversitas(request):
    if request.method == "POST":
        if Universitas.objects.filter(universitas=request.POST['universitas'].upper()).exists():
            messages.warning(request, 'Data Universita/Sekolahs Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:indexUniversitas'))
        else:
            saveuniversitas = Universitas(universitas = request.POST['universitas'].upper())    
            saveuniversitas.save()
            messages.success(request, 'Data Universitas/Sekolah Berhasil Ditambahkan.', extra_tags='primary')
            return HttpResponseRedirect(reverse('kepegawaian:indexUniversitas'))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexUniversitas'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def edituniversitas(request):
    if request.method == "POST":
        updateuniversitas = Universitas.objects.filter(id_universitas = request.POST["id_universitas"])

        if Universitas.objects.filter(universitas = request.POST['universitas'].upper()).exists():
            messages.warning(request, 'Data Universitas/Sekolah Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:detailUniversitas', args=(request.POST['id_universitas'],)))
        else:
            updateuniversitas.update(universitas = request.POST['universitas'].upper())
            messages.success(request, 'Data Universitas/Sekolah Berhasil Diubah.', extra_tags='warning')
            return HttpResponseRedirect(reverse('kepegawaian:indexUniversitas'))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexUniversitas'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def deleteuniversitas(request, pk):
    universitas = get_object_or_404(Universitas, pk=pk)
    universitas.delete()
    messages.warning(request, 'Data Universitas/Sekolah Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('kepegawaian:indexUniversitas'))
# END UNIVERSITAS

# JABATAN
class JabatanIndexView(SuperuserRequiredMixin, generic.ListView):
    model = Jabatan
    template_name = 'kepegawaian/main_data/jabatan/index.html'
    paginate_by = 50

class JabatanDetailView(SuperuserRequiredMixin, generic.DetailView):
    model = Jabatan
    template_name = 'kepegawaian/main_data/jabatan/detail.html'

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def addjabatan(request):
    if request.method == "POST":
        if Jabatan.objects.filter(Q(nama_jabatan = request.POST['jabatan'].upper()) & Q(gaji_pokok = request.POST['gaji_pokok']) & 
                                  Q(satuan_gaji = request.POST['satuan_gaji'])).exists():
            messages.warning(request, 'Data Jabatan Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:indexJabatan'))
        else:
            savejabatan = Jabatan(nama_jabatan = request.POST['jabatan'].upper(), gaji_pokok = request.POST['gaji_pokok'], 
                                  satuan_gaji = request.POST['satuan_gaji'])    
            savejabatan.save()
            messages.success(request, 'Data Jabatan Berhasil Ditambahkan.', extra_tags='primary')
            return HttpResponseRedirect(reverse('kepegawaian:indexJabatan'))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexJabatan'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def editjabatan(request):
    if request.method == "POST":
        updatejabatan = Jabatan.objects.filter(id_jabatan = request.POST["id_jabatan"])

        if Jabatan.objects.filter(Q(nama_jabatan = request.POST['jabatan'].upper()) & Q(gaji_pokok = request.POST['gaji_pokok']) & 
                                  Q(satuan_gaji = request.POST['satuan_gaji'])).exists():
            messages.warning(request, 'Data Jabatan Sudah Ada.', extra_tags='danger')
            return HttpResponseRedirect(reverse('kepegawaian:detailJabatan', args=(request.POST['id_jabatan'],)))
        else:
            updatejabatan.update(nama_jabatan = request.POST['jabatan'].upper(), gaji_pokok = request.POST['gaji_pokok'], 
                                 satuan_gaji = request.POST['satuan_gaji'])
            messages.success(request, 'Data Jabatan Berhasil Diubah.', extra_tags='warning')
            return HttpResponseRedirect(reverse('kepegawaian:indexJabatan'))
    else:
        return HttpResponseRedirect(reverse('kepegawaian:indexJabatan'))

@login_required(login_url='../admin/login')
@user_passes_test(lambda u: u.is_superuser)
def deletejabatan(request, pk):
    jabatan = get_object_or_404(Jabatan, pk=pk)
    jabatan.delete()
    messages.warning(request, 'Data Jabatan Berhasil Dihapus.', extra_tags='danger')
    return HttpResponseRedirect(reverse('kepegawaian:indexJabatan'))
# END JABATAN