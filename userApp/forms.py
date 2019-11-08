from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import User, UserProfile, Messages
from datetime import datetime

YEARS = [i for i in range(1950, datetime.now().year - 17)]


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),
                               label='Şifre',
                               max_length=64,
                               min_length=8, required=True, help_text='Şifreniz en az 8 karakter olmalıdır')
    password_validation = forms.CharField(widget=forms.PasswordInput(), label='Şifre Onayla', max_length=64,
                                          min_length=8, required=True)
    birth_day = forms.DateField(widget=forms.SelectDateWidget(years=YEARS), label='Doğum Günü')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'birth_day', 'password', 'password_validation']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control'}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'ornek@ornek.com'}
        self.fields['password'].widget.attrs = {'class': 'form-control', 'placeholder': '********'}
        self.fields['first_name'].widget.attrs = {'class': 'form-control'}
        self.fields['last_name'].widget.attrs = {'class': 'form-control'}
        self.fields['birth_day'].widget.attrs = {'class': 'form-control'}
        self.fields['password_validation'].widget.attrs = {'class': 'form-control', 'placeholder': '********'}

    def clean(self):
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('password_validation')
        if pass1 != pass2:
            return self.add_error('password_validation', 'Şifreler Eşleşmiyor!')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı mevcut!")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-posta adresi mevcut!")
        return email


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control'}
        self.fields['password'].widget.attrs = {'class': 'form-control', 'placeholder': '********'}


class EditEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(EditEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = {'class': 'form-control', 'style': 'margin-bottom:56px;'}

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Seçtiğiniz email kullanılıyor. Lütfen kullanılmayan bir email seçin.')
        return email


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']

    def __init__(self, *args, **kwargs):
        super(UploadImageForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs = {'style': 'width:100%;margin-bottom:30px;'}


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(user, *args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control', 'style': 'margin-bottom:30px;'}

    def clean_new_password1(self):
        pass1 = self.cleaned_data['new_password1']
        if len(pass1) < 8:
            raise forms.ValidationError('Yeni şifre en az 8 karakter olmak zorunda.')
        return pass1


class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['message']

    def __init__(self, *args, **kwargs):
        super(MessagesForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs = {'class': 'form-control'}