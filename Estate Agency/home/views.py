
from django.contrib import messages
from django.shortcuts import redirect, render

from home.models import Property, Slider, Inquary
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
# Create your views here.



def home(request):
    slider = Slider.objects.all()
    porperty = Property.objects.all()
    context = {
        'slider':slider,
        'porperty':porperty,
    }
    return render(request, 'home/index.html',context)

def all_property(request):
    property_list = Property.objects.filter(is_publish=True)
    paginator = Paginator(property_list,3)
    page_number = request.GET.get('page')
    property = paginator.get_page(page_number)
    
    context = {
        'property':property,
    }
    return render(request,'home/all_property.html',context)

def single_property(request,id):
    property = Property.objects.get(id=id)
    context = {
        'property':property
    }
    return render(request,'home/single_property.html',context)

@login_required
def post_property(request):
    if request.method =="POST" and request.FILES['image']:
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        location = request.POST.get('location')
        property_type = request.POST.get('property_type')
        area = request.POST.get('area')
        beds = request.POST.get('beds')
        baths = request.POST.get('baths')
        garage = request.POST.get('garage')
        video = request.POST.get('video')
        image = request.FILES['image']
        user = request.user
        
        Property.objects.create(name=name,description=description,price=price,location=location,property_type=property_type,area=area,beds=beds,baths=baths,garage=garage,video=video,image=image,user=user)
        messages.success(request,'Property Added Sucessfully')
    else:
        return render(request,'home/post_property.html')
    return render(request,'home/post_property.html')

def inquary(request):
    if request.method =="POST":
        property_owner_email= request.POST.get('property_owner_email')
        property_id = request.POST.get('property_id')
        property_name = request.POST.get('property_name')
        
        
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = name = request.POST.get('message')
        user = request.user
        Inquary.objects.create(user=user,name=name,email=email,phone=phone,message=message)
        
        email_subject= 'Property Inquary Message From EstateAgency'
        email_body = 'You Have an Enquary From '+name+'\nEmail: '+email+'\nPhone:'+phone+'\nHe/She Send You This message:\n'+message+'\n\n For Property ID: '+str(property_id)+'\nProperty Name: '+property_name+' '
        email_address = property_owner_email
        
        
        email = EmailMessage(
            email_subject,
            email_body,
            'noreply@estateagency.com',
            [email_address],
        )
        email.send(fail_silently=False)
        messages.success(request,'Your   Send Sucessfully')
        return render(request,'home/single_property.html')

    else:
        return render(request,'home/single_property.html')
    # return render(request,'home/single_property.html')