from django import forms


class InternForm(forms.Form):
    # choices_college = ['IITD','IITR','IITB','IITK','IITKGP']
    # choices_dep = ['Electrical Engineering']
    college = forms.CharField(max_length=100)
    area = forms.CharField(max_length=500,required=True)
    department = forms.CharField(max_length=100)
