from django.shortcuts import render
from django.views import View 

from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.http import HttpResponse
# Create your views here.
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from django.db.models import Q, F, Sum

from django.utils import timezone

from payment.models import Bill, Payment
from payment.forms import BillModelForm, PaymentForm
from payment.utility import generate_pdf
from property.models import  Booking, PropertyRequestResponse

from user.models import UserProfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q, Subquery

import stripe
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class AllBookingBillView(View):

    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        bookings = Booking.objects.filter(
            property_request_response__request_token__in=
                Subquery(PropertyRequestResponse. objects.filter(
                    user__id = user_id,
                    status='approved'
                ).values('request_token')),
            ).order_by('created_at')
        
        return render(request, "payment/bills.html", {'bookings':bookings})


class BookingBillView(View):
    template_name = "payment/booking_bills.html"
    form_class = BillModelForm
    bill_status = Bill.BILL_STATUS_CHOICES
    month_choice = Bill.MONTH_CHOICES
    current_time = timezone.now()

    def calculate_bill(self, request, booking_id, bill_data_dict):
        past_due_amount = self.past_due_bill(booking_id)
        context_data = {'past_due_amount':past_due_amount}
        context_data.update(bill_data_dict)
        bill_pdf = generate_pdf(request, 'payment/generate_bill.html', context_data)
        return bill_pdf
    
    def past_due_bill(self, booking_id):
        due_bills = Bill.objects.filter( ~Q(status = self.bill_status[0][0]), booking_id=booking_id ).annotate(due_amount = F('amount') - Sum('payment__amount',filter = Q(payment__status='success')))
        total_due_amount = due_bills.aggregate(Sum('due_amount'))
        return total_due_amount['due_amount__sum']

    def get(self, request, *args, **kwargs):
        booking_id = kwargs['booking_id']
        booking = get_object_or_404(Booking, pk=booking_id)
        bills = Bill.objects.filter(booking_id=booking_id)
        current_bill_amount = PropertyRequestResponse.objects.get(booking__id=booking_id, user__user_type='owner').rent_amount
        
        current_month = self.current_time.strftime('%B').lower()[:3]
        current_year = self.current_time.year
        initail_data = {'booking':booking, 'status':self.bill_status[2][0], 'month':current_month, 'year' : current_year,'amount':current_bill_amount}
        context = {'bill_form': self.form_class(initial=initail_data), 'bills':bills, 'booking':booking }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        bill_form = self.form_class(request.POST)
        booking_id = kwargs['booking_id']
        booking = get_object_or_404(Booking, pk=booking_id)

        if bill_form.is_valid():
            due_date = bill_form.cleaned_data['due_date']
            month = bill_form.cleaned_data['month']
            year = bill_form.cleaned_data['year']
            current_bill_amount = bill_form.cleaned_data['amount']
            bill_data_dict = {
                'due_date':due_date,
                'month':month,
                'year':year,
                'current_bill_amount':current_bill_amount,
                'current_time':self.current_time,
                'booking':booking,
            }
            bill_pdf = self.calculate_bill(request, booking_id, bill_data_dict)
            file_name = f"{str(year)}-{ str(month) }-{ booking.renter.get_full_name() }.pdf"
            bill_form.instance.document = SimpleUploadedFile(file_name, bill_pdf, content_type='application/pdf')
            bill_form.save()
            return redirect(reverse("booking_bills", args=[booking_id]))
        else:
            print('---------->',bill_form.errors)
        
        bills = Bill.objects.filter(booking_id=booking_id)
        context = {'bill_form': bill_form, 'bills':bills, 'booking':booking }
        return render(request, self.template_name, context)



from django.conf import settings
class TestPayment(View):

    def get(self, request, *args, **kwargs):
        context= {'stripe_publishable_key' : settings.STRIPE_PUBLISHABLE_KEY}
        return render(request,'payment/test.html',context)



class PayBillView(View):
    template_name = "payment/pay_bill.html"
    form_class = PaymentForm

    def get(self, request, *args, **kwargs):
        
        bill_id = kwargs['bill_id']
        bill = Bill.objects.get(id=bill_id)
        payable_amount = bill.amount - bill.paid_amount
        initail_data = {'amount':payable_amount}
        payment_form = self.form_class(initial=initail_data)
        context = {'payment_form':payment_form, 'stripe_publishable_key' : settings.STRIPE_PUBLISHABLE_KEY, 'bill_id':bill_id}
        return render(request, self.template_name, context)


@csrf_exempt
def create_checkout_session(request, bill_id):

    request_data = json.loads(request.body)
    paying_amount = int(request_data['paying_amount'])
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
       
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'INR',
                    'product_data': {
                    'name': 'test',
                    },
                    'unit_amount': int(paying_amount * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment_success', args=[bill_id])
        ) + "?session_id={CHECKOUT_SESSION_ID}&paying_amount="+str(paying_amount),
        cancel_url=request.build_absolute_uri(reverse('test')),
    )
    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(View):
    template_name = "payment/payment_success.html"

    def get(self, request, *args, **kwargs):
        bill_id = kwargs['bill_id']
        paying_amount = int(request.GET.get('paying_amount'))

        bill = Bill.objects.get(id=bill_id)
        user_id = request.user.id
        user = UserProfile.objects.get(id=user_id)
        payable_amount = bill.amount - bill.paid_amount
        if paying_amount >= payable_amount:
            status = 'paid'
        else:
            status = 'partial_paid'
        Payment.objects.create(user=user, bill= bill, amount=paying_amount, source='stripe', status=status)
        context = {'paying_amount':paying_amount}
        return render(request, self.template_name, context)
