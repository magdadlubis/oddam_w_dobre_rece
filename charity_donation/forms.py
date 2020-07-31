from charity_donation.models import *
from django  import forms

class EditDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['picked_up_date']
        '''
        widgets =  {
            'picked_up_date': forms.SelectDateWidget(),
        }
        '''