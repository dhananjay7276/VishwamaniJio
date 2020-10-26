from django.shortcuts import render
from django.views.generic.list import ListView
from Retailer.models import Profile, Notice , Report, Order
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, CreateView
from _datetime import date, datetime
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.db.models import Sum
from Row_Data.models import FOS

# Create your views here.
@method_decorator(login_required , name = 'dispatch')
class ReportListView(ListView):
    model = Report
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si =""
        if self.request.user.is_superuser:
            return Report.objects.filter(Retailer_Name__icontains= si).order_by("-id")
        else:
            return Report.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Retailer_Name__icontains= si).order_by("-id")

@method_decorator(login_required , name = 'dispatch')
class ReportUpdateView(UpdateView):
    model = Report
    fields  = ["Payment_Remark","Payment_Date","Cheque_No","Bank_Name","Payment_collected_by"]



@method_decorator(login_required , name = 'dispatch')
class OrderCreateView(CreateView):
    model = Order
    fields  = ["Product","Quantity","Description",]
    def form_valid(self, form):
        Retailer_Name = self.request.user.profile.Retailer_Name
        PRM_ID = self.request.user.profile.PRM_ID
        print("result of print "+Retailer_Name)
        print(PRM_ID)
        self.object = form.save()
        self.object.user = self.request.user
        self.object.PRM_ID = self.request.user.profile.PRM_ID
        self.object.Retailer_Name =self.request.user.profile.Retailer_Name
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required , name = 'dispatch')
class OrderListView(ListView):
    model = Order
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si =""
        if self.request.user.is_superuser:
            return Order.objects.filter(Product__icontains= si).order_by("-id")
        else:
            return Order.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Product__icontains= si).order_by("-id")


@method_decorator(login_required , name = 'dispatch')
class NoticeListView(ListView):
    model = Notice
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si =""
        if self.request.user.is_superuser:
            return Notice.objects.filter(Notice__icontains= si).order_by("-id")
        else:
            return Notice.objects.filter(Notice__icontains= si).order_by("-id")


@method_decorator(login_required, name="dispatch")    
class HomeView(TemplateView):
    template_name = "dashboard.html"
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        if self.request.user.is_superuser:
            Pending_List = Report.objects.filter(Payment_Remark = 'Pending')
            Pending_Order = Order.objects.filter(Order_Status = 'Pending')
            Pending_payment_count = Report.objects.filter(Payment_Remark = 'Pending').count()
            Cheque_Bounce = Report.objects.filter(Distributor_Remark = 'Cheque_Bounce').count()
            Cheque_Bounce_amount = Report.objects.filter(Distributor_Remark = 'Cheque_Bounce').aggregate(Sum('Amount'))['Amount__sum']
            Pending_Amount = Report.objects.filter(Payment_Remark ='Pending').aggregate(Sum('Amount'))['Amount__sum']
            Pending_Amount_Distibutor = Report.objects.exclude(Payment_Remark ='Pending').filter(Distributor_Remark ='Pending').aggregate(Sum('Amount'))['Amount__sum']
            Pending_Order_count = Order.objects.filter(Order_Status = 'Pending').count()
            Inprocess_Order_count = Order.objects.filter(Order_Status = 'In-Process').count()
            Complete_Order_count = Order.objects.filter(Order_Status = 'Complete').count()
            cash_payment =  Report.objects.filter(Payment_Remark = 'Cash').count()
            Cheque_payment =Report.objects.filter(Payment_Remark = 'Cheque').count()
            UPI_payment = Report.objects.filter(Payment_Remark = 'UPI').count()
            NEFT_payment  = Report.objects.filter(Payment_Remark = 'NEFT').count()
            # deva = Report.objects.exclude(Payment_Remark ='Cash').filter(Payment_collected_by = FOS.objects[1])
            # print(deva)       
            if Pending_Amount == None:
                Pending_Amount = 0
            if Pending_Amount_Distibutor == None:
                Pending_Amount_Distibutor = 0
            if Cheque_Bounce_amount == None:
                Cheque_Bounce_amount = 0

            area_wise_pending = {}
            for fos in FOS.objects.all():
                fos_retailer = Profile.objects.filter(FOS_Assign=fos)
                # fos_pending = Report.objects.filter(area_pending =)
                for prmid in fos_retailer:
                    fos_total_pending_amount = Report.objects.filter(PRM_ID=prmid.PRM_ID).aggregate(Sum('Amount'))['Amount__sum']
                    fos_pending_amount = Report.objects.filter(Payment_Remark = 'Pending').filter(PRM_ID=prmid.PRM_ID).aggregate(Sum('Amount'))['Amount__sum']
                    fos_area_collections = Report.objects.exclude(Payment_Remark = 'Pending').filter(PRM_ID=prmid.PRM_ID).aggregate(Sum('Amount'))['Amount__sum']
                    if fos_pending_amount == None:
                        fos_pending_amount = 0
                    if fos_area_collections == None:
                        fos_area_collections = 0
                    if fos_total_pending_amount == None:
                        fos_total_pending_amount = 0
                    area_wise_pending[fos.Fos_name] =[fos_total_pending_amount,fos_area_collections,fos_pending_amount]
                    print(fos_pending_amount)
                    
            print(area_wise_pending)
            fos_wise_pending = {}
            for fos in FOS.objects.all():
                pending_cash = Report.objects.filter(Payment_Remark ='Cash').filter(Payment_collected_by=fos).filter(Distributor_Remark ='Pending').aggregate(Sum('Amount'))['Amount__sum']
                pending_cheque = Report.objects.filter(Payment_Remark ='Cheque').filter(Payment_collected_by=fos).filter(Distributor_Remark ='Pending').aggregate(Sum('Amount'))['Amount__sum']
                pending_upi = Report.objects.filter(Payment_Remark ='UPI').filter(Payment_collected_by=fos).filter(Distributor_Remark ='Pending').aggregate(Sum('Amount'))['Amount__sum']
                pending_neft = Report.objects.filter(Payment_Remark ='NEFT').filter(Payment_collected_by=fos).filter(Distributor_Remark ='Pending').aggregate(Sum('Amount'))['Amount__sum']
                pending_collection = Report.objects.exclude(Payment_Remark ='Pending').filter(Payment_collected_by=fos).filter(Distributor_Remark ='Pending').aggregate(Sum('Amount'))['Amount__sum']

                if pending_cash ==None:
                    pending_cash =0
                if pending_cheque == None:
                    pending_cheque = 0
                if pending_upi == None:
                    pending_upi = 0
                if pending_neft == None:
                    pending_neft =0
                if pending_collection ==None:
                    pending_collection =0

                fos_wise_pending[fos.Fos_name]=[pending_cash,pending_cheque,pending_upi,pending_neft,pending_collection]

                # name.append(fos.Fos_name)
                # pending_cash_toward_fos = Report.objects.exclude(Payment_Remark ='Cash').filter(Payment_collected_by=fos).filter(Distributor_Remark ='Pending').aggregate(Sum('Amount'))['Amount__sum']
                # # print(name)
                # fos_wise_pending.append(pending_cash_toward_fos)
                # print(fos_wise_pending)

          
            

        
        else:
            Pending_List = Report.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Payment_Remark = 'Pending')
            Pending_Order = Order.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Order_Status = 'Pending')
            Pending_payment_count = Report.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Payment_Remark = 'Pending').count()
            Pending_Amount = Report.objects.filter(Payment_Remark ='Pending').filter(PRM_ID = self.request.user.profile.PRM_ID).aggregate(Sum('Amount'))['Amount__sum']
            Pending_Amount_Distibutor = Report.objects.exclude(Payment_Remark ='Pending').filter(Distributor_Remark ='Pending').filter(PRM_ID = self.request.user.profile.PRM_ID).aggregate(Sum('Amount'))['Amount__sum']
            Pending_Order_count = Order.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Order_Status = 'Pending').count()
            Inprocess_Order_count = Order.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Order_Status = 'In-Process').count()
            Complete_Order_count = Order.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Order_Status = 'Complete').count()
            cash_payment = Complete_Order_count = Report.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Payment_Remark = 'Cash').count()
            Cheque_payment = Complete_Order_count = Report.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Payment_Remark = 'Cheque').count()
            UPI_payment = Complete_Order_count = Report.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Payment_Remark = 'UPI').count()
            NEFT_payment = Complete_Order_count = Report.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Payment_Remark = 'NEFT').count()
            Cheque_Bounce = Report.objects.filter(PRM_ID = self.request.user.profile.PRM_ID).filter(Distributor_Remark = 'Cheque_Bounce').count()
            Cheque_Bounce_amount = Report.objects.filter(Distributor_Remark = 'Cheque_Bounce').aggregate(Sum('Amount'))['Amount__sum']
            if Pending_Amount == None:
                Pending_Amount = 0
            if Pending_Amount_Distibutor == None:
                Pending_Amount_Distibutor = 0
            if Cheque_Bounce_amount == None:
                Cheque_Bounce_amount = 0
            

        
        
        # print(Pending_Order)
        # print(Pending_List)
        context = {'pending_list':Pending_List, 'pending_Order':Pending_Order, 'pending_payment_count':Pending_payment_count,'pending_Amount':Pending_Amount,'Pending_Amount_Distibutor':Pending_Amount_Distibutor,'Pending_Order_count':Pending_Order_count,'Inprocess_Order_count':Inprocess_Order_count,'Complete_Order_count':Complete_Order_count,'cash_payment':cash_payment,'Cheque_payment':Cheque_payment,'UPI_payment':UPI_payment,'NEFT_payment':NEFT_payment,'Cheque_Bounce':Cheque_Bounce,'Cheque_Bounce_amount':Cheque_Bounce_amount,'fos_wise_pending':fos_wise_pending,'area_wise_pending':area_wise_pending}
        return context