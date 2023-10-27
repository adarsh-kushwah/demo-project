from django import forms

from payment.models import Bill, Payment


class BillModelForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(BillModelForm, self).__init__(*args, **kwargs)
        self.fields['document'].required = False

    class Meta:
        model = Bill
        fields = "__all__"
        widgets = {
            "amount": forms.HiddenInput(),
            "booking": forms.HiddenInput(),
            "status": forms.HiddenInput(),
            "document": forms.HiddenInput(),
            "due_date": forms.widgets.DateInput(attrs={"type": "date"}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']
        