from django import forms
from .models import *
class UserForms(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'enter your password'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'confirm your password'}))
    class Meta:
        model=account
        fields=['first_name','last_name','email','password','phone']

    def __init__(self,*args,**kwargs):
        super(UserForms,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        for field in self.fields.values():
            field.widget.attrs['placeholder']=field.label

            self.fields['password'].widget.attrs['placeholder']='enter your password'
            self.fields['confirm_password'].widget.attrs['placeholder']='confirm password'
    def clean(self):
        cleaned_data=super(UserForms,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match ")
            
class userForms(forms.ModelForm):
    class Meta:
        model=account
        fields=['first_name','last_name','phone']

    def __init__(self,*args,**kwargs):
        super(userForms,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False,widget=forms.FileInput,error_messages={'invalid':('image files only',)})

    class Meta:
        model=UserProfile
        fields=['address_line_1','address_line_2','state','city','country','profile_picture']

    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'

