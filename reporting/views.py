from django.shortcuts import render
from .models import Business, LineItem

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from reporting.models import Business, LineItem, Invoice
from django.db import models
from reporting.models import *
from django.db.models import Sum, F, Q


# # Create your views here.
def index(request):
  return HttpResponse("Hello, world.")


def dashboard(request):
    businesses = Business.objects.annotate(
        total_job_amount=Sum('job__lineitem__amount'),
        total_invoice_amount=Sum('invoice__lineitem__amount'),
        remaining_invoice_amount=Sum('invoice__lineitem__amount', filter=models.Q(invoice__status='unpaid'))
    ).order_by('-remaining_invoice_amount')

    # Query the invoices and payments associated with each customer
    for business in businesses:
        invoices = Invoice.objects.filter(lineitem__job__business=business).distinct()
        print(invoices)
        payments = Payment.objects.filter(invoice__lineitem__job__business=business).values('type', 'reference').annotate(amount=Sum('amount'))

        # Attach the invoice and payment information to the business object
        business.invoices = invoices
        business.payments = payments

    return render(request, 'dashboard.html', {'businesses': businesses})



def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})


def customer_list(request):
    customers = Customer.objects.annotate(
        total_job_amount=Sum('job__lineitem__amount'),
        total_job_amount_remaining=Sum(
            F('job__lineitem__amount') - 
            F('job__lineitem__invoice__lineitem__amount')
        )
    )
    return render(request, 'customer_list.html', {'customers': customers})


def dashboard(request):
    # Query the LineItem model to get the total job line item amount and
    # the total job line item amount remaining to be invoiced for each customer
    job_amounts = LineItem.objects.filter(
        invoice__isnull=True  # Only consider LineItems without an invoice
    ).values(
        'job__business_id'  # Group by the customer's business ID
    ).annotate(
        total_amount=Sum('amount'),  # Calculate the sum of the amount field for each group
        remaining_amount=Sum('amount', filter=models.Q(invoice__isnull=True))  # Calculate the sum of the amount field for each group where invoice is null
    )

    # Query the LineItem model to get the total invoice line item amount for each customer
    invoice_amounts = LineItem.objects.filter(
        invoice__isnull=False  # Only consider LineItems with an invoice
    ).values(
        'job__business_id'  # Group by the customer's business ID
    ).annotate(
        total_amount=Sum('amount')  # Calculate the sum of the amount field for each group
    )

    # Query the Business model to get a list of all customers, sorted by the remaining amount to be invoiced
    customers = Business.objects.annotate(
        remaining_amount=Sum('job__lineitem__amount', filter=models.Q(job__lineitem__invoice__isnull=True))  # Calculate the sum of the amount field for each customer where invoice is null
    ).order_by('-remaining_amount')

    # Render the dashboard template with the retrieved data
    return render(request, 'dashboard.html', {
        'customers': customers,
        'job_amounts': job_amounts,
        'invoice_amounts': invoice_amounts,
    })



def dashboard(request):
    # Retrieve all customers and their related data
    customers = Customer.objects.annotate(
        total_job_amount=Sum('job__line_items__amount'),
        total_remaining_amount=Sum('job__line_items__amount', filter= ~models.Q(job__line_items__invoice__status=Invoice.PAID)),
        total_invoice_amount=Sum('job__line_items__invoice__lineitem__amount', filter= models.Q(job__line_items__invoice__status=Invoice.PAID))
    ).order_by('-total_remaining_amount')

    # Render the data in a template
    return render(request, 'dashboard.html', {'customers': customers})




def dashboard(request):
    if request.method == 'POST':
        min_amount = request.POST.get('min_amount')
        max_amount = request.POST.get('max_amount')
        if min_amount and max_amount:
            customers = Customer.objects.annotate(
                total_remaining=Sum('job__line_items__amount', filter=~Q(job__line_items__invoice=None)) - 
                                Sum('job__line_items__invoice__amount')
            ).filter(total_remaining__gte=min_amount, total_remaining__lte=max_amount)
        else:
            customers = Customer.objects.annotate(
                total_remaining=Sum('job__line_items__amount', filter=~Q(job__line_items__invoice=None)) - 
                                Sum('job__line_items__invoice__amount')
            )
    else:
        customers = Customer.objects.annotate(
            total_remaining=Sum('job__line_items__amount', filter=~Q(job__line_items__invoice=None)) - 
                            Sum('job__line_items__invoice__amount')
        )
    context = {'customers': customers}
    return render(request, 'dashboard.html', context)