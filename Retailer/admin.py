from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.options import ModelAdmin
from Retailer.models import Profile, Report, Notice, Order
from django.contrib.auth.models import User
# Register your models here.

def change_distibutor_remark(modeladmin, request, queryset):
    queryset.update(Distributor_Remark = 'Received')
# Action description
change_distibutor_remark.short_description = "Mark Selected Payments as Received"

class ReportAdmin(ImportExportModelAdmin):
    list_display = ["Payment_Fill_Date","PRM_ID","Retailer_Name","Amount","Payment_Remark","Distributor_Remark"]
    search_fields = ["PRM_ID","Retailer_Name","Cheque_No"]
    list_filter = ["Retailer_Name","Payment_Remark","Bank_Name","Distributor_Remark"]
    actions = [change_distibutor_remark]

admin.site.register(Report, ReportAdmin)


class NoticeAdmin(ImportExportModelAdmin):
    list_display = ["cr_date","Notice"]
    search_fields = ["Notice"]
    list_filter = ["cr_date","Visible"]

admin.site.register(Notice, NoticeAdmin)


class ProfiAdmin(ModelAdmin):
    list_display = ["PRM_ID","Jio_ID","Retailer_Name","Mobile_No","FOS_Assign"]
    search_fields = ["PRM_ID","Jio_ID","Retailer_Name","Mobile_No","Whatsapp_No","Email_ID","Adharcard_no","Address"]
    list_filter = ["FOS_Assign"]

admin.site.register(Profile, ProfiAdmin)

class OrderAdmin(ImportExportModelAdmin):
    list_display = ["PRM_ID","Retailer_Name","Product","Quantity","Order_Status"]
    search_fields = ["user","Product","PRM_ID","Retailer_Name"]
    list_filter = ["Product","Order_Status"]


admin.site.register(Order, OrderAdmin)