import smtplib

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from datetime import datetime,timedelta
from django.views.decorators.cache import never_cache
import random
import smtplib
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect

# Create your views here.
from myapp.models import Users, Hospital, vaccine_information, Vaccinestock, country_vaccine, slot, Booking, Child, \
    VaccineDocument


def login_get(request):
    return render(request,'loginindex.html')


def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    lobj=authenticate(request,username=username,password=password)
    if lobj is not None:

        login(request,lobj)
        if lobj.groups.filter(name='Admin'):
            return redirect('/myapp/adm_home/')

        elif lobj.groups.filter(name='Hospital'):

            if Hospital.objects.filter(AUTHUSER_id=lobj.id,status="accepted"):
                return redirect('/myapp/h_home/')
            else:
                messages.error(request, 'Hospital not verified yet')
                return redirect('/myapp/login_get/')
        elif lobj.groups.filter(name='User'):
            return redirect('/myapp/User_home/')


        else:
            messages.error(request,'user not found')
            return redirect('/myapp/login_get/')
    else:
        messages.error(request,'invaild username and password')
        return redirect('/myapp/login_get/')




def log_out(request):
    logout(request)
    return redirect('/myapp/login_get/')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_home(request):
    return render(request,'Admins/Adminindex.html')


@never_cache
@login_required(login_url='/myapp/login_get')
def adm_addvaccination_info(request):
    return render(request,'Admins/Add_vaccinationinfo.html')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_addvaccination_info_post(request):
    vaccinename=request.POST['vaccinename']
    if vaccine_information.objects.filter(Vaccinename=vaccinename).exists():
        messages.error(request, 'Vaccine name already exists')
        return redirect('/myapp/adm_addvaccination_info/#t')
    else:
        Age_group=request.POST['Age_group']
        Dose_number=request.POST['Dose_number']
        discription=request.POST['discription']
        Side_effect=request.POST['Side_effect']
        m_companie=request.POST['m_companie']
        Emergency=request.POST['Emergency']

        vobj=vaccine_information()
        vobj.Vaccinename=vaccinename
        vobj.Age=Age_group
        vobj.Description=discription
        vobj.Dose_number=Dose_number

        vobj.Side_effect=Side_effect
        vobj.Manufacture=m_companie
        vobj.Emergency_type=Emergency
        vobj.save()
        messages.success(request,'Added successfully')
        return redirect('/myapp/adm_addvaccination_info/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_change_password_get(requset):
    return render(requset,'Admins/Change_password.html')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_edit_vaccine_info_get(request,id):
    data=vaccine_information.objects.get(id=id)
    return render(request,'Admins/Edit_vaccination_infro.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_edit_vaccine_info_post(request):
    vaccinename = request.POST['vaccinename']
    Age_group = request.POST['Age_group']
    Dose_number = request.POST['Dose_number']
    discription = request.POST['discription']
    Side_effect = request.POST['Side_effect']
    m_companie = request.POST['m_companie']
    Emergency = request.POST['Emergency']
    id=request.POST['id']

    vobj = vaccine_information.objects.get(id=id)
    vobj.Vaccinename = vaccinename
    vobj.Age = Age_group
    vobj.Description = discription
    vobj.Dose_number = Dose_number

    vobj.Side_effect = Side_effect
    vobj.Manufacture = m_companie
    vobj.Emergency_type = Emergency
    vobj.save()
    messages.success(request, 'Edited successfully')
    return redirect('/myapp/adm_viewvaccinationinfo_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_view_accepthospital_get(request):
    data = Hospital.objects.filter(status='accepted')
    return render(request,'Admins/view_accepthospital.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_viewvaccinationinfo_get(request):
    data=vaccine_information.objects.all()
    return render(request,'Admins/View_vaccination_information.html',{'data':data})


@never_cache
@login_required(login_url='/myapp/login_get')
def adm_add_country_vaccine_get(request):
    data=vaccine_information.objects.all()
    return render(request,'Admins/Add_country_vaccine.html',{'data':data})


@never_cache
@login_required(login_url='/myapp/login_get')
def adm_addcountryvaccin_info_post(request):
    Destination_country=request.POST['Destination_country']
    Discription =request.POST['Discription']
    vaccine=request.POST['vaccine']

    chk=country_vaccine.objects.filter(Destination_country=Destination_country,VACCINATIONINFORMATION_id=vaccine)
    if chk:
        messages.error(request,"This vaccine is already registered for the selected destination country.")
        return redirect('/myapp/adm_add_country_vaccine_get/#t')

    else:
        cobj = country_vaccine()
        cobj.Destination_country = Destination_country
        cobj.Discription = Discription
        cobj.VACCINATIONINFORMATION_id=vaccine
        cobj.save()
        messages.success(request, 'Added successfully')
        return redirect('/myapp/adm_add_country_vaccine_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_Edit_country_vaccine_get(request,id):
    data = country_vaccine.objects.get(id=id)
    data2=vaccine_information.objects.all()

    return render(request, 'Admins/Edit_country_vaccine.html', {'data': data,'data2':data2})

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_Edit_countryvaccin_info_post(request):
    Destination_country = request.POST['Destination_country']
    Discription = request.POST['Discription']
    vaccine = request.POST['vaccine']
    id = request.POST['id']

    cobj = country_vaccine.objects.get(id=id)
    cobj.Destination_country = Destination_country
    cobj.Discription = Discription
    cobj.VACCINATIONINFORMATION_id = vaccine
    cobj.save()
    messages.success(request, 'Edited successfully')
    return redirect('/myapp/adm_view_country_vaccine_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_delete_country_vaccine(request,id):
    country_vaccine.objects.get(id=id).delete()
    messages.success(request,"Deleted successfully")
    return redirect('/myapp/adm_view_country_vaccine_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_view_country_vaccine_get(request):
    data=country_vaccine.objects.all()
    return render(request,'Admins/View_country_vaccine.html',{'data':data})


@never_cache
@login_required(login_url='/myapp/login_get')
def adm_delete_vaccine_info(request,id):
    vaccine_information.objects.filter(id=id).delete()
    messages.success(request,"Deleted successfully")
    return redirect('/myapp/adm_viewvaccinationinfo_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_view_vaccine_document_get(request):
    return render(request,'Admins/View_vaccine_document.html')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_view_vaccine_report_get(request):
    return render(request,'Admins/View_vaccine_report.html')


@never_cache
@login_required(login_url='/myapp/login_get')
def adm_view_vaccine_stock_get(request,id):
    data=Vaccinestock.objects.filter(HOSPITAL_id=id)
    return render(request,'Admins/View_vaccine_stock.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_view_hospital_get(request):
    data=Hospital.objects.filter(status='pending')
    return render(request,'Admins/viewhospital.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_accepthospital(request,id):
    Hospital.objects.filter(id=id).update(status='accepted')
    messages.success(request,"Accepted successfully")
    return redirect('/myapp/adm_view_hospital_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_rejecthospital(request,id):
    Hospital.objects.filter(id=id).update(status='Rejected')
    messages.success(request,"Rejected successfully")
    return redirect('/myapp/adm_view_hospital_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_view_rejecthospital_get(request):
    data = Hospital.objects.filter(status='Rejected')
    return render(request,'Admins/viewrejecthospital.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_viewuser_get(request):
    data=Users.objects.all()
    return render(request,'Admins/viewuser.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_view_document(request):

    data = VaccineDocument.objects.all()
    return render(request,'Admins/View_document.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def adm_view_booking(request):
    data = Booking.objects.all()
    return render(request, 'Admins/View_booking.html', {'data': data})





def user_sigup_get(request):
    return render(request,'User/signup.html')


def user_signup_post(request):
    name=request.POST['name']
    gender=request.POST['gender']
    dob=request.POST['dob']
    email=request.POST['email']
    Phone_number=request.POST['Phone_number']
    place=request.POST['place']
    city=request.POST['city']
    state=request.POST['state']
    pincode=request.POST['pincode']
    upload_photo=request.FILES['upload_photo']

    if User.objects.filter(username=email).exists():
        messages.error(request,"An account with this email already exists")
        return redirect('/myapp/user_sigup_get/')

    else:
        date=datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
        fs=FileSystemStorage()
        fs.save(date,upload_photo)
        path=fs.url(date)
        password=request.POST['password']

        aobj=User.objects.create_user(username=email,password=password)
        aobj.groups.add(Group.objects.get(name='User'))
        aobj.save()

        uobj=Users()
        uobj.name=name
        uobj.place=place
        uobj.state=state
        uobj.city=city
        uobj.pincode=pincode
        uobj.gender=gender
        uobj.Dob=dob
        uobj.Upload_photo= path
        uobj.email=email
        uobj.phone=Phone_number
        uobj.AUTHUSER=aobj
        uobj.save()
        return redirect('/myapp/login_get/')

@never_cache
@login_required(login_url='/myapp/login_get')
def user_view_country_vaccine_get(request):
    data=country_vaccine.objects.all()
    return render(request,'User/View_country_vaccine.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def user_add_document_get(request):
    data=Hospital.objects.all()
    return render(request,'User/upload_vaccine_documnet.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def user_document_upload(request):
    document=request.FILES['document']
    hospital=request.POST['hospital']
    date=datetime.now().strftime("%Y%m%d-%H%M%S")+".pdf"
    fs=FileSystemStorage()
    fs.save(date,document)
    path=fs.url(date)


    uobj=VaccineDocument()
    uobj.Document= path
    uobj.status='pending'
    uobj.Date= datetime.now().date()
    uobj.HOSPITAL=Hospital.objects.get(id=hospital)
    uobj.USER=Users.objects.get(AUTHUSER=request.user)
    uobj.save()
    messages.success(request,'Uploaded successfully')
    return redirect('/myapp/user_view_document/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def user_view_document(request):

    d = VaccineDocument.objects.filter(USER__AUTHUSER=request.user)
    return render(request,'User/View_document.html',{'data':d})


@never_cache
@login_required(login_url='/myapp/login_get')
def user_edit_document(request,id):
    data=Hospital.objects.all()

    d=VaccineDocument.objects.get(id=id)
    return render(request,'User/Edit_upload_vaccine_documnet.html',{'data':d,'data2':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def user_edit_document_post(request):
    id = request.POST['id']
    hospital = request.POST['hospital']
    hobj = VaccineDocument.objects.get(id=id)
    if 'document' in request.FILES:
        document = request.FILES['document']
        if document != "":
            date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".pdf"
            fs = FileSystemStorage()
            fs.save(date, document)
            path = fs.url(date)
            hobj.Document = path
            hobj.save()

    hobj.Date = datetime.now().date()
    hobj.HOSPITAL=Hospital.objects.get(id=hospital)

    hobj.save()
    messages.success(request, 'Edit successfully')
    return redirect('/myapp/user_view_document/')

@never_cache
@login_required(login_url='/myapp/login_get')
def delete_document_info(request,id):
    VaccineDocument.objects.filter(id=id).delete()
    return redirect('/myapp/user_view_document/')



def hospital_signup_get(request):
    return render(request,'Hospital/signup.html')


def hospital_signup_post(request):
    name=request.POST['name']
    email=request.POST['email']
    Phone_number=request.POST['Phone_number']
    place=request.POST['place']
    city=request.POST['city']
    state=request.POST['state']
    pincode=request.POST['pincode']
    upload_photo=request.FILES['upload_photo']
    date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    fs = FileSystemStorage()
    fs.save(date, upload_photo)
    path = fs.url(date)
    licensenumber=request.POST['license_number']
    password=request.POST['password']
    if User.objects.filter(username=email).exists():
        messages.error(request, "An account with this email already exists")
        return redirect('/myapp/hospital_signup_get/')
    else:
        aobj = User.objects.create_user(username=email, password=password)
        aobj.groups.add(Group.objects.get(name='Hospital'))
        aobj.save()

        hobj=Hospital()
        hobj.hospitalname=name
        hobj.hospitalplace=place
        hobj.city=city
        hobj.hospitalstate=state
        hobj.hospitalpincode=pincode
        hobj.email=email
        hobj.phone=Phone_number
        hobj.pincode=pincode
        hobj.Upload_photo=path
        hobj.licensenumber=licensenumber
        hobj.status='pending'
        hobj.AUTHUSER = aobj
        hobj.save()
        return redirect('/myapp/login_get/')

@never_cache
@login_required(login_url='/myapp/login_get')
def h_view_vaccine_info(request):
    d = vaccine_information.objects.all().order_by('-id')
    return render(request,'Hospital/View_vaccination_information.html',{'data':d})

@never_cache
@login_required(login_url='/myapp/login_get')
def h_add_stock_get(request,id):
    return render(request,'Hospital/Add_stock.html',{'id':id})

@never_cache
@login_required(login_url='/myapp/login_get')
def h_add_stock_post(request):
    stock=request.POST['stock']
    id=request.POST['id']
    if Vaccinestock.objects.filter(VACCINATIONINFORMATION_id=id).exists():
        vv=Vaccinestock.objects.get(VACCINATIONINFORMATION_id=id)
        vv.stock_no=int(vv.stock_no)+int(stock)
        vv.save()
        messages.success(request, "Stock Added successfully")
        return redirect('/myapp/view_vaccine_stock/#t')
    else:
        sobj=Vaccinestock()
        sobj.VACCINATIONINFORMATION=vaccine_information.objects.get(id=id)
        sobj.HOSPITAL=Hospital.objects.get(AUTHUSER_id=request.user.id)
        sobj.stock_no=stock
        sobj.save()
        messages.success(request,"Stock Added successfully")
        return redirect('/myapp/view_vaccine_stock/#t')


@never_cache
@login_required(login_url='/myapp/login_get')
def h_home(request):
    return render(request,'Hospital/Hospitalindex.html')

@never_cache
@login_required(login_url='/myapp/login_get')
def H_view_profile(request):
    d=Hospital.objects.get(AUTHUSER_id=request.user.id)
    return render(request,'Hospital/View_profile.html',{'data':d})

@never_cache
@login_required(login_url='/myapp/login_get')
def H_edit_profile_get(request):
    d = Hospital.objects.get(AUTHUSER_id=request.user.id)
    return render(request, 'Hospital/Edit_profile.html', {'H1': d})

@never_cache
@login_required(login_url='/myapp/login_get')
def H_edit_profile_post(request):
    name = request.POST['name']
    email = request.POST['email']
    Phone_number = request.POST['Phone_number']
    place = request.POST['place']
    city = request.POST['city']
    state = request.POST['state']
    pincode = request.POST['pincode']
    licensenumber = request.POST['license_number']



    hobj = Hospital.objects.get(AUTHUSER_id=request.user.id)
    if 'upload_photo' in request.FILES:
        upload_photo = request.FILES['upload_photo']
        if upload_photo != "":
            date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
            fs = FileSystemStorage()
            fs.save(date, upload_photo)
            path = fs.url(date)
            hobj.Upload_photo = path

    hobj.hospitalname = name
    hobj.hospitalplace = place
    hobj.city = city
    hobj.hospitalstate = state
    hobj.hospitalpincode = pincode
    hobj.email = email
    hobj.phone = Phone_number
    hobj.pincode = pincode
    hobj.licensenumber = licensenumber

    hobj.save()
    messages.success(request, 'Edit successfully')
    return redirect('/myapp/H_view_profile/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def H_view_document(request):
    d = VaccineDocument.objects.filter(HOSPITAL__AUTHUSER=request.user)
    return render(request,'Hospital/View_document.html',{'data':d})



@login_required(login_url='/myapp/login_get')
def H_approve_documnet(request,id):
    VaccineDocument.objects.filter(id=id).update(status='Approved')
    return redirect('/myapp/H_view_document/')

@never_cache
@login_required(login_url='/myapp/login_get')
def H_reject_document(request,id):
    VaccineDocument.objects.filter(id=id).update(status='Rejected')
    return redirect('/myapp/H_view_document/')

@login_required(login_url='/myapp/login_get')
def H_view_approved_doc(request):
    d = VaccineDocument.objects.filter(HOSPITAL__AUTHUSER=request.user,status='Approved')
    return render(request, 'Hospital/view_approved_document.html', {'data': d})

@never_cache
@login_required(login_url='/myapp/login_get')
def User_home(request):
    return render(request,'User/Userindex.html')

@never_cache
@login_required(login_url='/myapp/login_get')
def U_view_vaccinr_information(request):
    data = vaccine_information.objects.all()
    return render(request, 'User/View_vaccination_information.html', {'data': data})

@never_cache
@login_required(login_url='/myapp/login_get')
def view_vaccine_stock(request):
    data =Vaccinestock.objects.filter(HOSPITAL__AUTHUSER=request.user.id).order_by('-id')
    return render(request,'Hospital/Viewstock.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def U_view_profile(request):
    d=Users.objects.get(AUTHUSER_id=request.user.id)
    return render(request,'User/View_profile.html',{'data':d})

@never_cache
@login_required(login_url='/myapp/login_get')
def U_edit_profile_get(request):
    d = Users.objects.get(AUTHUSER_id=request.user.id)
    return render(request, 'User/Edit_profile.html', {'data': d})

@never_cache
@login_required(login_url='/myapp/login_get')
def U_edit_profile_post(request):
    name = request.POST['name']
    gender = request.POST['gender']
    dob = request.POST['dob']
    email = request.POST['email']
    Phone_number = request.POST['Phone_number']
    place = request.POST['place']
    city = request.POST['city']
    state = request.POST['state']
    pincode = request.POST['pincode']

    # aobj = User.objects.create_user(username=email, password=confirm_password)
    # aobj.groups.add(Group.objects.get(name='User'))
    # aobj.save()

    uobj = Users.objects.get(AUTHUSER_id=request.user.id)
    if 'upload_photo' in request.FILES:
        upload_photo = request.FILES['upload_photo']
        if upload_photo !="":
            date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
            fs = FileSystemStorage()
            fs.save(date, upload_photo)
            path = fs.url(date)
            uobj.Upload_photo = path
            uobj.save()

    uobj.name = name
    uobj.place = place
    uobj.state = state
    uobj.city = city
    uobj.pincode = pincode
    uobj.gender = gender
    uobj.Dob = dob
    uobj.email = email
    uobj.phone = Phone_number
    uobj.save()
    messages.success(request, 'Edit successfully')
    return redirect('/myapp/U_view_profile/#t')


@never_cache
@login_required(login_url='/myapp/login_get')
def A_changepassword_get(request):
    return render(request,'Admins/Change_password.html')


@never_cache
@login_required(login_url='/myapp/login_get')
def A_changepassword_post(request):
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    data = request.user
    if data.check_password(current_password):
        if new_password == confirm_password:
            data.set_password(confirm_password)
            data.save()
            messages.success(request, 'Password updated successfully')
            return redirect('/myapp/login_get/')
        else:
            messages.error(request, 'Password dose not match')
            return redirect('/myapp/A_changepassword_get/#t')
    else:
        messages.error(request, 'current password is incorrect')
        return redirect('/myapp/A_changepassword_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def H_changepassword_get(request):
    return render(request,'Hospital/Change_password.html')

@never_cache
@login_required(login_url='/myapp/login_get')
def H_changepassword_post(request):
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    data = request.user
    if data.check_password(current_password):
        if new_password == confirm_password:
            data.set_password(confirm_password)
            data.save()
            return redirect('/myapp/login_get/')
        else:
            messages.error(request, 'Password does not match')
            return redirect('/myapp/H_changepassword_get/#t')
    else:
        messages.error(request, 'Old password does not match')
        return redirect('/myapp/H_changepassword_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def U_view_hospital(request):
    data = Hospital.objects.filter(status='accepted')
    return render(request,'Hospital/view_hospital.html',{'data': data})
@never_cache
@login_required(login_url='/myapp/login_get')
def U_changepassword_get(request):
    return render(request,'User/Change_password.html')

@never_cache
@login_required(login_url='/myapp/login_get')
def U_changepassword_post(request):
    current_password=request.POST['current_password']
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm_password']
    data=request.user
    if data.check_password(current_password):
        if new_password == confirm_password:
            data.set_password(confirm_password)
            data.save()

            return redirect('/myapp/login_get/')
        else:
            messages.error(request,'Password dose not match')
            return redirect('/myapp/U_changepassword_get/')
    else:
        messages.error(request,'Incorrect old password')
        return redirect('/myapp/U_changepassword_get/')

@never_cache
def P_view_vaccinr_information(request):
        data = vaccine_information.objects.all()
        return render(request, 'Public/View_vaccination_information.html', {'data': data})

@never_cache
def P_view_hospital_get(request):
    data=Hospital.objects.filter(status='accepted')
    return render(request,'Public/viewhospital.html',{'data':data})

@never_cache
def P_view_country_vaccine_get(request):
    data=country_vaccine.objects.all()
    return render(request,'Public/View_country_vaccine.html',{'data':data})


@never_cache
def p_home_get(request):
    return render(request,'Public/Publichome.html',)


@never_cache
@login_required(login_url='/myapp/login_get')
def U_view_hospital_vaccine_get(request, id):
    vaccine = vaccine_information.objects.get(id=id)

    data = (
        slot.objects
        .filter(VACCINATIONINFORMATION=vaccine)
        .select_related('HOSPITAL')
        .values(
            'HOSPITAL_id',
            'HOSPITAL__hospitalname',
            'HOSPITAL__hospitalplace',
            'HOSPITAL__email',
            'HOSPITAL__phone',
            'HOSPITAL__Upload_photo',
        )
        .distinct()
    )

    return render(
        request,
        'User/viewhospital.html',
        {
            'data': data,
            'vaccine': vaccine,
        }
    )
#
# def U_view_hospital_vaccine_get(request,id):
#     vaccine=vaccine_information.objects.get(id=id)
#     data=slot.objects.filter(VACCINATIONINFORMATION=vaccine).select_related('HOSPITAL').distinct()
#     return render(request,'User/viewhospital.html',{'data':data,'vaccine':vaccine})

@never_cache
@login_required(login_url='/myapp/login_get')
def U_view_hospital_get(request,id):
    data=Vaccinestock.objects.filter(VACCINATIONINFORMATION_id=id)
    return render(request,'User/viewhospital.html',{'data':data})
# def U_view_slot_get(request,id):
#     data=slot.objects.filter(HOSPITAL_id=id)
#     sdate = slot.objects.filter(HOSPITAL_id=id).values_list('Date', flat=True).distinct()
#     l=[]
#     for i in data:
#         if Booking.objects.filter(USER__AUTHUSER=request.user,SLOT=i.id).exists():
#
#             l.append({'id':i.id,'Fromtime':i.Fromtime,'Date':i.Date,
#
#                      'Vaccinename':i.VACCINATIONINFORMATION.Vaccinename,
#                       'Age':i.VACCINATIONINFORMATION.Age,
#                       'Side_effect':i.VACCINATIONINFORMATION.Side_effect,
#                       'status':'Yes','Hospital':i.HOSPITAL.hospitalname
#
#                       })
#         else:
#             l.append({'id': i.id, 'Fromtime': i.Fromtime, 'Date': i.Date,
#                       'Vaccinename': i.VACCINATIONINFORMATION.Vaccinename,
#                       'Age': i.VACCINATIONINFORMATION.Age,
#                       'Side_effect': i.VACCINATIONINFORMATION.Side_effect,
#                       'status': 'No'
#
#                       })
#     return render(request,'User/Viewslot.html',{'data':data,'sdate':sdate})

# def U_view_slot_get(request, id, date=None):
#
#     sdate = slot.objects.filter(HOSPITAL_id=id).values_list('Date', flat=True).distinct().order_by('Date')
#
#     if date:
#         data = slot.objects.filter( HOSPITAL_id=id,Date=date)
#     else:
#         data = slot.objects.filter(HOSPITAL_id=id)
#
#     l = []
#
#     for i in data:
#
#         if Booking.objects.filter(USER__AUTHUSER=request.user,SLOT=i.id).exists():
#
#             l.append({
#                 'id': i.id,
#                 'Fromtime': i.Fromtime,
#                 'Date': i.Date,
#                 'Vaccinename': i.VACCINATIONINFORMATION.Vaccinename,
#                 'Age': i.VACCINATIONINFORMATION.Age,
#                 'Side_effect': i.VACCINATIONINFORMATION.Side_effect,
#                 'status': 'Yes',
#                 'Hospital': i.HOSPITAL.hospitalname
#             })
#
#         else:
#
#             l.append({
#                 'id': i.id,
#                 'Fromtime': i.Fromtime,
#                 'Date': i.Date,
#                 'Vaccinename': i.VACCINATIONINFORMATION.Vaccinename,
#                 'Age': i.VACCINATIONINFORMATION.Age,
#                 'Side_effect': i.VACCINATIONINFORMATION.Side_effect,
#                 'status': 'No',
#                 'Hospital': i.HOSPITAL.hospitalname
#             })
#
#     return render(request,'User/Viewslot.html',{'data': l,'sdate': sdate,'hospital_id': id,'selected_date': date})

@never_cache
@login_required(login_url='/myapp/login_get')
def U_view_slot_get(request, hospital_id, vaccine_id, date=None):

    vaccine = vaccine_information.objects.get(id=vaccine_id)

    sdate = (
        slot.objects
        .filter(
            HOSPITAL_id=hospital_id,
            VACCINATIONINFORMATION_id=vaccine_id
        )
        .values_list('Date', flat=True)
        .distinct()
        .order_by('Date')
    )

    if date:
        data = slot.objects.filter(
            HOSPITAL_id=hospital_id,
            VACCINATIONINFORMATION_id=vaccine_id,
            Date=date
        ).select_related(
            'HOSPITAL',
            'VACCINATIONINFORMATION'
        )
    else:
        data = slot.objects.filter(
            HOSPITAL_id=hospital_id,
            VACCINATIONINFORMATION_id=vaccine_id
        ).select_related(
            'HOSPITAL',
            'VACCINATIONINFORMATION'
        )

    l = []

    for i in data:

        already_booked = Booking.objects.filter(
            USER__AUTHUSER=request.user,
            SLOT=i.id
        ).exists()

        l.append({
            'id': i.id,
            'Fromtime': i.Fromtime,
            'Date': i.Date,
            'Vaccinename': i.VACCINATIONINFORMATION.Vaccinename,
            'Age': i.VACCINATIONINFORMATION.Age,
            'Side_effect': i.VACCINATIONINFORMATION.Side_effect,
            'status': 'Yes' if already_booked else 'No',
            'Hospital': i.HOSPITAL.hospitalname
        })

    return render(
        request,
        'User/Viewslot.html',
        {
            'data': l,
            'sdate': sdate,
            'hospital_id': hospital_id,
            'vaccine_id': vaccine_id,
            'vaccine': vaccine,
            'selected_date': date
        }
    )



@never_cache
@login_required(login_url='/myapp/login_get')
def Add_child_get(request):
    return render(request,'User/Add_child.html')


@never_cache
@login_required(login_url='/myapp/login_get')
def Add_child_post(request):
    name=request.POST['name']
    gender=request.POST['gender']
    dob = request.POST['dob']
    blood_group = request.POST['blood_group']
    relation = request.POST['relation']
    hobj=Child()
    hobj.Name=name
    hobj.gender=gender
    hobj.Dob=dob
    hobj.blood_group=blood_group
    hobj.relation=relation
    hobj.USER=Users.objects.get(AUTHUSER=request.user)

    hobj.save()
    messages.success(request,'Registered successfully')
    return redirect('/myapp/U_view_child_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def h_slot_get(request):
    data=vaccine_information.objects.all()

    return render(request,'Hospital/Add_slot.html',{'data':data})


# @login_required(login_url='/myapp/login_get')
# def h_slot_post(request):
#     fromtime=request.POST['fromtime']
#     Date =request.POST['Date']
#     vaccine=request.POST['vaccine']
#
#
#     sobj=slot()
#     sobj.Fromtime = fromtime
#     sobj.Date = Date
#     sobj.VACCINATIONINFORMATION_id=vaccine
#     sobj.HOSPITAL=Hospital.objects.get(AUTHUSER=request.user)
#     sobj.save()
#     messages.success(request, 'Added successfully')
#     return redirect('/myapp/h_view_slot_get/#t')



@never_cache
@login_required(login_url='/myapp/login_get')
def h_slot_post(request):

    Date = request.POST['Date']
    vaccine = request.POST['vaccine']

    hospital = Hospital.objects.get(AUTHUSER=request.user)

    check = slot.objects.filter(Date=Date,VACCINATIONINFORMATION_id=vaccine,HOSPITAL=hospital).exists()

    if check:
        messages.error(request,"Slots for this date and vaccine already exist.")
        return redirect('/myapp/h_slot_get/#t')
    else:

        start_time = datetime.strptime("09:00", "%H:%M")
        end_time = datetime.strptime("17:00", "%H:%M")

        current_time = start_time

        while current_time < end_time:

            # Skip 12:30 PM - 1:00 PM
            if current_time.hour == 12 and current_time.minute >= 30:
                current_time = datetime.strptime("13:00", "%H:%M")
                continue

            sobj = slot()
            sobj.Fromtime = current_time.time()
            sobj.Date = Date
            sobj.VACCINATIONINFORMATION_id = vaccine
            sobj.HOSPITAL = hospital
            sobj.save()

            # 10 minute gap
            current_time += timedelta(minutes=10)

        messages.success(request, 'All slots added successfully')
        return redirect('/myapp/h_view_slot_get/#t')


@never_cache
@login_required(login_url='/myapp/login_get')
def h_slot_Edit_get(request,id):
    data =slot.objects.get(id=id)
    data2=vaccine_information.objects.all()

    return render(request, 'Hospital/Edit_slot.html', {'data': data,'data2':data2})

@never_cache
@login_required(login_url='/myapp/login_get')
def h_slot_Edit_post(request):

    Date = request.POST['Date']
    vaccine = request.POST['vaccine']
    id = request.POST['id']

    sobj = slot.objects.get(id=id)

    sobj.Date = Date
    sobj.VACCINATIONINFORMATION_id = vaccine
    sobj.save()

    messages.success(request, 'Edited successfully')
    return redirect('/myapp/h_view_slot_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def h_slot_delete(request,id):
    slot.objects.get(id=id).delete()
    messages.success(request,"Slot deleted successfully")
    return redirect('/myapp/h_view_slot_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def h_view_slot_get(request):
    data=slot.objects.filter(HOSPITAL__AUTHUSER=request.user).order_by('Date','Fromtime')
    return render(request,'Hospital/View_slot.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def H_view_booking(request):
    data = Booking.objects.filter(SLOT__HOSPITAL__AUTHUSER=request.user)
    return render(request, 'Hospital/View_booking.html', {'data': data})


@never_cache
@login_required(login_url='/myapp/login_get')
def h_confirm_vaccination(request,id):
    Booking.objects.filter(id=id).update(status="Vaccinated")
    messages.success(request,"Vaccination confirmed successfully")
    return redirect('/myapp/H_view_booking/#t')



@never_cache
@login_required(login_url='/myapp/login_get')
def H_emergency_vacc(request):
    data=vaccine_information.objects.filter( Emergency_type='Yes')
    return render(request,'Hospital/View_emergency_vaccine.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def U_view_child_get(request):
    data=Child.objects.filter(USER__AUTHUSER=request.user)
    return render(request,'User/View_child.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def U_edit_child_info_get(request,id):
    data=Child.objects.get(id=id)
    return render(request,'User/Editchild.html',{'data':data})

@never_cache
@login_required(login_url='/myapp/login_get')
def U_edit_child_post(request):
    name = request.POST['name']
    gender = request.POST['gender']
    dob = request.POST['dob']
    blood_group = request.POST['blood_group']
    relation = request.POST['relation']
    id=request.POST['id']

    hobj = Child.objects.get(id=id)
    hobj.Name = name
    hobj.gender = gender
    hobj.Dob = dob
    hobj.blood_group = blood_group
    hobj.relation = relation
    hobj.save()
    messages.success(request, 'Edited successfully')
    return redirect('/myapp/U_view_child_get/#t')


@never_cache
@login_required(login_url='/myapp/login_get')
def delete_child_info(request,id):
    Child.objects.filter(id=id).delete()
    messages.success(request,"Deleted successfully")
    return redirect('/myapp/U_view_child_get/#t')

@never_cache
@login_required(login_url='/myapp/login_get')
def U_view_vaccin_information(request):
    data = vaccine_information.objects.all()
    return render(request, 'Public/View_vaccination_information.html', {'data': data})

@never_cache
@login_required(login_url='/myapp/login_get')
def U_view_conform_slot(request,id):
    data=slot.objects.filter(id=id)
    child=Child.objects.filter(USER__AUTHUSER=request.user)
    return render(request,'User/conform_slot.html',{'data':data,'child':child})

# @never_cache
# @login_required(login_url='/myapp/login_get')
# def book_vaccine(request):
#     cid=request.POST['cid']
#     id=request.POST['id']
#     type=''
#     data1=slot.objects.get(id=id).VACCINATIONINFORMATION
#     if data1.Emergency_type=='Yes':
#         type='Emergency'
#     else:
#         type='Normal'
#     data=Booking()
#     data.Discription='pending'
#     data.status='booked'
#     data.Date=datetime.now().date()
#     data.Type=type
#     data.Cid=cid
#     data.SLOT=slot.objects.get(id=id)
#     data.USER=Users.objects.get(AUTHUSER=request.user)
#     data.save()
#     messages.success(request,"Booking successfully Completed")
#     return redirect('/myapp/U_view_booking/#t')


@never_cache
@login_required(login_url='/myapp/login_get')
def book_vaccine(request):
    cid = request.POST['cid']
    id = request.POST['id']
    type = ''

    slot_obj = slot.objects.get(id=id)
    data1 = slot_obj.VACCINATIONINFORMATION

    if data1.Emergency_type == 'Yes':
        type = 'Emergency'
    else:
        type = 'Normal'

    # Corresponding hospital's stock entry for this vaccine
    stock_obj = Vaccinestock.objects.get(
        VACCINATIONINFORMATION=data1,
        HOSPITAL=slot_obj.HOSPITAL   # <-- slot model-il hospital field ulla peru idivide vekkuka
    )

    # stock_no CharField ayath kondu int aakki minus cheyyuka
    current_stock = int(stock_obj.stock_no)

    if current_stock <= 0:
        messages.error(request, "Vaccine out of stock at this hospital")
        return redirect('/myapp/U_view_booking/#t')

    stock_obj.stock_no = str(current_stock - 1)
    stock_obj.save()

    data = Booking()
    data.Discription = 'pending'
    data.status = 'booked'
    data.Date = datetime.now().date()
    data.Type = type
    data.Cid = cid
    data.SLOT = slot_obj
    data.USER = Users.objects.get(AUTHUSER=request.user)
    data.save()

    messages.success(request, "Booking successfully Completed")
    return redirect('/myapp/U_view_booking/#t')
@never_cache
@login_required(login_url='/myapp/login_get')
def U_view_booking(request):
    data = Booking.objects.filter(USER__AUTHUSER=request.user)
    return render(request, 'User/View_booking.html', {'data': data})

@never_cache
@login_required(login_url='/myapp/login_get')
def U_emergency_vacc(request):
    data=vaccine_information.objects.filter( Emergency_type='Yes')
    return render(request,'User/View_emergency_vaccine.html',{'data':data})


# @never_cache
# @login_required(login_url='/myapp/login_get')
# def U_vaccine_card_view(request):
#
#     data=Booking.objects.filter(USER__AUTHUSER=request.user,status="Vaccinated")
#     user=Users.objects.get(AUTHUSER=request.user)
#     return render(request,'User/vaccine_card.html',{'data':data,'user':user})

@never_cache
@login_required(login_url='/myapp/login_get')
def U_vaccine_card_view(request):

    data = Booking.objects.filter(
        USER__AUTHUSER=request.user,
        status="Vaccinated"
    )

    user = Users.objects.get(AUTHUSER=request.user)

    return render(
        request,
        'User/vaccine_card.html',
        {
            'data': data,
            'user': user
        }
    )


def landing_get(request):
    return render(request,'landing.html')






def and_forget_password(request):
    return render(request, 'forgottenpassword.html')




def and_forget_password_post(request):
    if request.method == 'POST':
        email = request.POST['textfield']

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            messages.warning(request, 'Email does not exist.')
            return redirect('/myapp/and_forget_password/')

        psw = random.randint(1000, 9999)

        user.set_password(str(psw))
        user.save()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("haappy110011@gmail.com", "pkunllndarvgujbh")

        subject = "Password Reset - Construction App"
        body = "Your new password is: " + str(psw)
        msg = "Subject: " + subject + "\n\n" + body

        server.sendmail("haappy110011@gmail.com", email, msg)
        server.quit()

        messages.success(request, 'A new password has been sent to your email.')
        return redirect('/myapp/login_get/')

    messages.warning(request, 'Failed to send.')
    return redirect('/myapp/and_forget_password/')



from django.http import HttpResponse

from .notification import check_all_notifications


def test_vaccine_notification(request):

    check_all_notifications()

    return HttpResponse(
        "Vaccine notification checking completed."
    )


# server.login("trainingstarted@gmail.com", "nlxasujxgazlbmgz")  # App Password
