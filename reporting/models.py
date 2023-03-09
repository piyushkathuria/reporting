from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_invoice_and_payment_details(self):
        invoice_ids = []
        payment_details = {}

        for job in self.job_set.all():
            for line_item in job.lineitem_set.all():
                if line_item.invoice:
                    invoice_ids.append(line_item.invoice.number)
                    if line_item.payment:
                        payment_key = f"{line_item.payment.payment_type}_{line_item.payment.reference}"
                        if payment_key in payment_details:
                            payment_details[payment_key]['amount'] += line_item.amount
                        else:
                            payment_details[payment_key] = {
                                'payment_type': line_item.payment.payment_type,
                                'reference': line_item.payment.reference,
                                'amount': line_item.amount
                            }

        return {
            'invoice_ids': invoice_ids,
            'payment_details': list(payment_details.values())
        }


class Business(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Invoice(models.Model):
    PAID = 'paid'
    UNPAID = 'unpaid'
    DRAFT = 'draft'

    STATUS_CHOICES = [
        (PAID, 'Paid'),
        (UNPAID, 'Unpaid'),
        (DRAFT, 'Draft'),
    ]

    business = models.ForeignKey('Business', on_delete=models.CASCADE)
    number = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default=DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LineItem(models.Model):
    job = models.ForeignKey('Job', on_delete=models.RESTRICT, null=True, related_name='line_items')
    invoice = models.ForeignKey('Invoice', on_delete=models.RESTRICT, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.RESTRICT, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class Job(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, null=True)
    business = models.ForeignKey(Business, on_delete=models.RESTRICT, blank=True,null=True)
    lineitems = models.ForeignKey(LineItem, on_delete=models.RESTRICT, blank=True,null=True, related_name='jobs')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Payment(models.Model):
    CHECK = 'check'
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'

    TYPES = [
        (CHECK, 'Check'),
        (CREDIT_CARD, 'Credit Card'),
        (DEBIT_CARD, 'Debit Card'),
    ]

    payer = models.ForeignKey(
        'Business', related_name='payments_sent', on_delete=models.RESTRICT)
    payee = models.ForeignKey(
        'Business', related_name='payments_received', on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    reference = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255)
    initiated_at = models.DateTimeField()
    completed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


