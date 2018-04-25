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


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2


class ContactUsForm(forms.Form):
    name = forms.CharField(label=("Name"),widget=forms.TextInput(attrs={'style': 'color: black;'}), max_length=50)
    subject = forms.CharField(label=("Subject"), max_length=2000,widget=forms.Textarea(attrs={'style': 'color: black;'}),help_text='Write here your message!')

    def clean(self):
        cleaned_data = super(ContactUsForm, self).clean()
        name = cleaned_data.get('name')
        message = cleaned_data.get('subject')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')
