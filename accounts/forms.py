from django import forms
from .models import *


class UserForms(forms.ModelForm):
            password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'enter your password','class':'form-control'}))
            confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm-password','class':'form-control'}))

            class Meta:
                model=account
                fields=['first_name','last_name','email','phone','password']

           
            def __init__(self,*args,**kwargs):
                    super(UserForms,self).__init__(*args,**kwargs)



                    for field in self.fields:
                            self.fields[field].widget.attrs['class']='form-control'
                           

                    for field in self.fields.values():
                            field.widget.attrs['placeholder']= field.label
                            
                    self.fields['password'].widget.attrs['placeholder']='Enter password'
                    self.fields['confirm_password'].widget.attrs['placeholder']='Enter confirm password'

                


            def clean(self):
                cleaned_data=super(UserForms,self).clean()
                password=cleaned_data.get('password')
                confirm_password=cleaned_data.get('confirm_password')
                if password!=confirm_password:
                        raise forms.ValidationError("password does not match")
                

class UserForms(forms.ModelForm):
       class Meta:
              model=account
              fields=['first_name','last_name','phone']
        
       def __init__(self,*args,**kwargs):
              super(UserForms,self).__init__(*args,**kwargs)
              for field in self.fields:
                     self.fields[field].widget.attrs['class']='form-control'

class UserProfileForms(forms.ModelForm):
       profile_picture=forms.ImageField(required=False,error_messages={'invalid':('Image Files only')},widget=forms.FileInput)
       class Meta:
              model=UserProfile
              fields=['address_line_1','address_line_2','state','city','country','profile_picture']
       def __init__(self,*args,**kwargs):
              super(UserProfileForms,self).__init__(*args,**kwargs)
              for field in self.fields:
                     self.fields[field].widget.attrs['class']='form-control'