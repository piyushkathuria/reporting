from django.shortcuts import render
from .models import Business, LineItem
from .tables import CustomerTable

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from reporting.models import Business, LineItem, Invoice
from django.db import models
from reporting.models import *
from django.db.models import Sum, F, Q
from django_tables2 import RequestConfig


# # Create your views here.
def index(request):
  return HttpResponse("Hello, world.")





def customer_list(request):
    customers = Customer.objects.annotate(
        total_job_amount=Sum('jobs__line_items__amount'),
        total_job_amount_remaining=Sum(
            F('jobs__line_items__amount') - 
            F('jobs__line_items__invoice__line_items__amount')
        ),
        invoice_amount = Sum('jobs__line_items__invoice__line_items__amount')
    )
    table = CustomerTable(customers,order_by = '-invoice_amount')
    RequestConfig(request).configure(table)
    return render(request, 'customer_list.html', {'table': table})


def customer_detail(request,customer_id):
    customer = Customer.objects.get(pk = customer_id)
    invoices = Invoice.objects.filter(
        line_items__job__customer = customer
    )
    payments = Payment.objects.filter(
        line_items__job__customer = customer
    ).values('payment_type').annotate(
        payment_amount = Sum('amount')
    )
    return render(request, 'customer_detail.html', {'customer': customer,'invoices': invoices,'payments':payments})


def dashboard(request):
    if request.method == 'POST':
        min_amount = request.POST.get('min_amount')
        max_amount = request.POST.get('max_amount')
        
        if min_amount and max_amount and min_amount < max_amount:
            jobs = Job.objects.annotate(
                total_job_amount_remaining=Sum(
                    F('line_items__amount') - 
                    F('line_items__invoice__line_items__amount')
                ),
            ).filter(total_job_amount_remaining__gte=min_amount, total_job_amount_remaining__lte=max_amount)
            context = {'jobs': jobs}
            return render(request, 'dashboard.html', context)

    jobs = Job.objects.annotate(
        total_job_amount_remaining=Sum(
            F('line_items__amount') - 
            F('line_items__invoice__line_items__amount')
        ),
    )
        
    context = {'jobs': jobs}
    return render(request, 'dashboard.html', context)