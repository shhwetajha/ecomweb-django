from django.shortcuts import render
from store.models import *
from kart.models import *
import pandas as pd
def view_home(request):
    products=Products.objects.all().filter(is_available=True)
    context={'products':products}
    return render(request,'home.html',context)

def view_chart(request):
    student=Student.objects.all().values()
    df=pd.DataFrame(student)
    df1=df.name.tolist()
    df=df['rank'].tolist()
    mydict={'df':df,
    'df1':df1}
    return render(request,'chart.html',context=mydict)