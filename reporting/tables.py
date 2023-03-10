import django_tables2 as tables
from django_tables2.utils import A
from .models import Customer

class CustomerTable(tables.Table):
    name = tables.LinkColumn('customerdetail', args=[A('pk')])
    email = tables.Column()
    total_job_amount = tables.Column()
    total_job_amount_remaining = tables.Column()
    invoice_amount = tables.Column()

    class Meta:
        model = Customer
        template_name = 'django_tables2/bootstrap.html'
        fields = ('name', 'email')