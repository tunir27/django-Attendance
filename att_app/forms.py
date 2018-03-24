from django import forms

class RegistrationForm(forms.Form):
    std_id = forms.CharField(label='Student ID',max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class FilterAttendance(forms.Form):
    date = forms.CharField(label='Date',max_length=100)
    s_class=forms.CharField(label='Class',max_length=100)
    sec=forms.CharField(label='sec',max_length=100)


class VerifyForm(forms.Form):
    s_id = forms.CharField(label='Student ID',max_length=100)
    date = forms.CharField(label='Date',max_length=100)
    status = forms.CharField(label='Student Status',max_length=1)
