"""vaxicare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login_get/', views.login_get),
    path('login_post/',views.login_post),
    path('log_out/',views.log_out),
    path('adm_home/',views.adm_home),
    path('adm_addvaccination_info/',views.adm_addvaccination_info),
    path('adm_addvaccination_info_post/',views.adm_addvaccination_info_post),
    path('adm_change_password_get/',views.adm_change_password_get),
    path('adm_edit_vaccine_info_get/<id>',views.adm_edit_vaccine_info_get),
    path('adm_view_accepthospital_get/',views.adm_view_accepthospital_get),
    path('adm_viewvaccinationinfo_get/',views.adm_viewvaccinationinfo_get),
    path('adm_edit_vaccine_info_post/',views.adm_edit_vaccine_info_post),
    path('adm_delete_vaccine_info/<id>',views.adm_delete_vaccine_info),

    path('adm_view_vaccine_document_get/',views.adm_view_vaccine_document_get),
    path('adm_view_vaccine_report_get/',views.adm_view_vaccine_report_get),
    path('adm_view_vaccine_stock_get/<id>',views.adm_view_vaccine_stock_get),
    path('adm_view_hospital_get/',views.adm_view_hospital_get),
    path('adm_view_rejecthospital_get/',views.adm_view_rejecthospital_get),
    path('adm_viewuser_get/',views.adm_viewuser_get),
    path('adm_accepthospital/<id>',views.adm_accepthospital),
    path('adm_rejecthospital/<id>',views.adm_rejecthospital),
    path('adm_add_country_vaccine_get/',views.adm_add_country_vaccine_get),
    path('adm_view_country_vaccine_get/',views.adm_view_country_vaccine_get),
    path('adm_addcountryvaccin_info_post/',views.adm_addcountryvaccin_info_post),
    path('adm_Edit_country_vaccine_get/<id>',views.adm_Edit_country_vaccine_get),
    path('adm_delete_country_vaccine/<id>',views.adm_delete_country_vaccine),
    path('adm_Edit_countryvaccin_info_post/',views.adm_Edit_countryvaccin_info_post),
    path('A_changepassword_get/',views.A_changepassword_get),
    path('A_changepassword_post/',views.A_changepassword_post),
    path('user_sigup_get/',views.user_sigup_get),
    path('user_signup_post/',views.user_signup_post),
    path('user_document_upload/',views.user_document_upload),
    path('user_add_document_get/',views.user_add_document_get),
    path('user_edit_document/<id>',views.user_edit_document),
    path('user_edit_document_post/',views.user_edit_document_post),
    path('user_view_document/',views.user_view_document),
    path('delete_document_info/<id>',views.delete_document_info),
    path('user_view_country_vaccine_get/',views.user_view_country_vaccine_get),
    path('hospital_signup_get/',views.hospital_signup_get),
    path('hospital_signup_post/', views.hospital_signup_post),
    path('h_view_vaccine_info/', views.h_view_vaccine_info),
    path('h_home/', views.h_home),
    path('H_view_profile/', views.H_view_profile),
    path('h_add_stock_get/<id>', views.h_add_stock_get),
    path('h_add_stock_post/', views.h_add_stock_post),
    path('view_vaccine_stock/', views.view_vaccine_stock),
    path('H_edit_profile_get/', views.H_edit_profile_get),
    path('H_edit_profile_post/', views.H_edit_profile_post),
    path('H_changepassword_get/', views.H_changepassword_get),
    path('H_changepassword_post/', views.H_changepassword_post),
    path('h_slot_get/', views.h_slot_get),
    path('h_slot_post/', views.h_slot_post),
    path('h_slot_Edit_get/<id>', views.h_slot_Edit_get),
    path('h_slot_Edit_post/', views.h_slot_Edit_post),
    path('h_slot_delete/<id>', views.h_slot_delete),
    path('h_view_slot_get/', views.h_view_slot_get),




    path('User_home/', views.User_home),
    path('U_view_vaccinr_information/', views.U_view_vaccinr_information),
    path('U_view_profile/', views.U_view_profile),
    path('U_edit_profile_get/', views.U_edit_profile_get),
    path('U_edit_profile_post/', views.U_edit_profile_post),
    path('U_view_hospital/', views.U_view_hospital),
    path('U_changepassword_get/', views.U_changepassword_get),
    path('U_changepassword_post/', views.U_changepassword_post),
    path('P_view_vaccinr_information/', views.P_view_vaccinr_information),
    path('P_view_hospital_get/', views.P_view_hospital_get),
    path('P_view_country_vaccine_get/', views.P_view_country_vaccine_get),
    path('p_home_get/', views.p_home_get),
    # path(
    #     'U_view_vaccinr_information/',
    #     views.U_view_vaccinr_information,
    #     name='U_view_vaccinr_information'
    # ),

    path(
        'U_view_hospital_vaccine_get/<int:id>/',
        views.U_view_hospital_vaccine_get,
        name='U_view_hospital_vaccine_get'
    ),

    path(
        'U_view_slot_get/<int:hospital_id>/<int:vaccine_id>/',
        views.U_view_slot_get,
        name='U_view_slot_get'
    ),

    path(
        'U_view_slot_get/<int:hospital_id>/<int:vaccine_id>/<str:date>/',
        views.U_view_slot_get,
        name='U_view_slot_get_date'
    ),    path('Add_child_get/', views.Add_child_get),
    path('Add_child_post/', views.Add_child_post),
    path('U_view_child_get/', views.U_view_child_get),
    path('U_edit_child_info_get/<id>', views.U_edit_child_info_get),
    path('U_edit_child_post/', views.U_edit_child_post),
    path('delete_child_info/<id>', views.delete_child_info),
    path('U_view_vaccin_information/', views.U_view_vaccin_information),
    path('U_view_hospital_vaccine_get/<id>', views.U_view_hospital_vaccine_get),
    path('U_view_conform_slot/<id>', views.U_view_conform_slot),
    path('book_vaccine/', views.book_vaccine),
    path('U_view_booking/', views.U_view_booking),
    path('H_view_booking/', views.H_view_booking),
    path('H_view_booking/', views.H_view_booking),
    path('H_view_document/', views.H_view_document),
    path('h_confirm_vaccination/<id>', views.h_confirm_vaccination),
    path('H_approve_documnet/<id>', views.H_approve_documnet),
    path('H_reject_document/<id>', views.H_reject_document),
    path('H_view_approved_doc/', views.H_view_approved_doc),
    path('landing_get/', views.landing_get),
    path('and_forget_password_post/', views.and_forget_password_post),
    path('and_forget_password/', views.and_forget_password),
    path('adm_view_document/', views.adm_view_document),
    path('adm_view_booking/', views.adm_view_booking),
    path('U_emergency_vacc/', views.U_emergency_vacc),
    path('H_emergency_vacc/', views.H_emergency_vacc),
    path('U_vaccine_card_view/', views.U_vaccine_card_view),
    path('test_vaccine_notification/', views.test_vaccine_notification),













]
