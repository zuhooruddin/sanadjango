from django.shortcuts import render
from django.contrib.auth import get_user_model

from uniapp.serializer import CustomUserSerializer, ItemsSerializer
from .models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


# Create your views here.
User = get_user_model()


@api_view(['GET', 'POST'])

def adduser(request):
    username=request.data.get('username')
    password=request.data.get('password')
    email=request.data.get('email')
    city=request.data.get('city')
    phone=request.data.get('phone')
    newpassword=make_password(password)
    image=request.data.get('image')
    
    savedata=CustomUser.objects.create(username=username,password=newpassword,email=email,city=city,phone_number=phone,image=image)

    if savedata:
        return JsonResponse("User Created Sucessfully",safe=False)
    
    else:
        return JsonResponse("Failed to Create User",safe=False)

import base64

@api_view(['GET', 'POST'])
def userLogin(request):
    email = request.data.get("email")
    password = request.data.get('password')

    try:
        user = CustomUser.objects.get(email=email)
        print("user is")
        print(user.image.url)  # Get the URL of the image
    except CustomUser.DoesNotExist:
        return JsonResponse({"Msg": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    if user.check_password(password):
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            'phone':user.phone_number,
            "image": user.image.url,
            "city":user.city
                # Include the image URL in the response
        }
        return Response({"Msg": "Successfully logged in", 'user': user_data}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"Msg": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)





@api_view(['GET','POST'])
def addAds(request):
    image_files = request.FILES.getlist('images[]')  
    print(image_files)
    category = request.data.get('category')
    title = request.data.get('title')
    quantity = request.data.get('quantity')
    price = request.data.get('price')
    description = request.data.get('description')
    user_id = request.data.get('user')

    try:
        user_instance = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"Msg": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    try:
        item = Items.objects.create(
            category=category,
            title=title,
            quantity=quantity,
            price=price,
            description=description,
            userid=user_instance,
        )

        for image_file in image_files:
            image = Image.objects.create(image=image_file)
            item.images.add(image)

        return Response({"Msg": "Data Saved Successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"Msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','POST'])
def getActiveAdds(request):
    user_id = request.data.get('userid')

    try:
        data = Items.objects.filter(userid=user_id, status='active').values()
        datalist = list(data)

        # Construct a list of dictionaries for each item with associated image URLs
        items_with_images = []
        for item in datalist:
            item_with_images = {
                'id': item['id'],
                'category': item['category'],
                'title': item['title'],
                'quantity': item['quantity'],
                'price': item['price'],
                'description': item['description'],
                # 'userid': item['userid'],  # User ID
                'status': item['status'],
                'date': item['date'],
                'location': item['location'],
                'images': [image.image.url for image in Items.objects.get(id=item['id']).images.all()]  # Retrieve image URLs
            }
            items_with_images.append(item_with_images)

        return JsonResponse({"Msg": "Data retrieved successfully", 'data': items_with_images}, status=200)

    except Items.DoesNotExist:
        return JsonResponse({"Msg": "No active items found for the specified user"}, status=status.HTTP_404_NOT_FOUND)

    
@api_view(['GET','POST'])
def getSoldAdds(request):
    user_id = request.data.get('userid')

    try:
        data = Items.objects.filter(userid=user_id, status='sold').values()
        datalist = list(data)

        # Construct a list of dictionaries for each item with associated image URLs
        items_with_images = []
        for item in datalist:
            item_with_images = {
                'id': item['id'],
                'category': item['category'],
                'title': item['title'],
                'quantity': item['quantity'],
                'price': item['price'],
                'description': item['description'],
                # 'userid': item['userid'],  # User ID
                'status': item['status'],
                'date': item['date'],
                'location': item['location'],
                'images': [image.image.url for image in Items.objects.get(id=item['id']).images.all()]  # Retrieve image URLs
            }
            items_with_images.append(item_with_images)

        return JsonResponse({"Msg": "Data retrieved successfully", 'data': items_with_images}, status=200)

    except Items.DoesNotExist:
        return JsonResponse({"Msg": "No sold items found for the specified user"}, status=status.HTTP_404_NOT_FOUND)


    except Items.DoesNotExist:
        return JsonResponse({"Msg": "Item does not exist"}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET','POST'])
def getPendingAdds(request):
    user_id = request.data.get('userid')

    try:
        data = Items.objects.filter(userid=user_id, status='pending').values()
        datalist = list(data)

        # Construct a list of dictionaries for each item with associated image URLs
        items_with_images = []
        for item in datalist:
            item_with_images = {
                'id': item['id'],
                'category': item['category'],
                'title': item['title'],
                'quantity': item['quantity'],
                'price': item['price'],
                'description': item['description'],
                # 'userid': item['userid'],  # User ID
                'status': item['status'],
                'date': item['date'],
                'location': item['location'],
                'images': [image.image.url for image in Items.objects.get(id=item['id']).images.all()]  # Retrieve image URLs
            }
            items_with_images.append(item_with_images)

        return JsonResponse({"Msg": "Data retrieved successfully", 'data': items_with_images}, status=200)

    except Items.DoesNotExist:
        return JsonResponse({"Msg": "No pending items found for the specified user"}, status=status.HTTP_404_NOT_FOUND)

    
@api_view(['GET', 'POST'])
def deleteItem(request):
    userid = request.data['userid']
    productid = request.data['productid']

    try:
        item = Items.objects.get(userid=userid, pk=productid)
        item.delete()
        return Response({'Msg': 'Item deleted successfully'}, status=status.HTTP_200_OK)
    except Items.DoesNotExist:
        return Response({'Msg': 'Item does not exist for the specified user'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def soldItem(request):
    userid = request.data['userid']
    productid = request.data['productid']

    try:
        sold=Items.objects.get(userid=userid,pk=productid)
        sold.status = 'sold'  
        sold.save() 
        return JsonResponse({"Msg":"Data Sucessfully Updated"})
    
    except Items.DoesNotExist:
        return Response({'Msg': 'Item does not exist for the specified user'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','POST'])
def getAllAdds(request):
    try:
        # Query the items, ordering by date (descending) and price (ascending).
        items = Items.objects.filter(status='active').order_by('-date', 'price')
        
        # Create a list to store item details and associated image URLs.
        item_list = []
        
        for item in items:
            item_data = {
                'id': item.id,
                'category': item.category,
                'title': item.title,
                'quantity': item.quantity,
                'price': item.price,
                'description': item.description,
                'userid': item.userid.id,  # Assuming you want to include the user ID
                'status': item.status,
                'date': item.date,
                'location': item.location,
                'image': [image.image.url for image in item.images.all()]  # Retrieve image URLs
            }
            item_list.append(item_data)
      
        return JsonResponse({'Msg': 'Data Successfully Updated', 'data': item_list}, status=200)
    
    except Items.DoesNotExist:
        return Response({'Msg': 'Item does not exist for the specified user'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework import status

@api_view(['GET','POST'])
def getSingleAdds(request):
    item_id = request.data.get('id')
    
    try:
        item = Items.objects.get(pk=item_id)
        
        # Create an instance of the serializer to include user-related fields
        serializer = ItemsSerializer(item)

        # Get the serialized data
        serialized_data = serializer.data

        # You can now access user-related fields like 'user_name', 'user_email', 'user_phone', and 'user_image' in 'serialized_data'

        # Append image URLs
        serialized_data['images'] = [image.image.url for image in item.images.all()]

        return JsonResponse({"Msg": "Data retrieved successfully", 'data': serialized_data}, status=200)

    except Items.DoesNotExist:
        return JsonResponse({'Msg': 'Item does not exist'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET', 'POST'])
def getSingleUser(request):
    id = request.data.get('id')
    try:
        user = CustomUser.objects.get(pk=id)
        serializer = CustomUserSerializer(user)  # Serialize the user object
        return Response({"Msg": "Data Successfully Retrieved", 'data': serializer.data}, status=200)
    except CustomUser.DoesNotExist:
        return Response({'Msg': 'User does not exist for the specified ID'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def updateUser(request):
    user_id = request.data.get('userid')
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"Msg": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    user.username = request.data.get('username', user.username)
    user.email = request.data.get('email', user.email)
    user.phone_number = request.data.get('phone_number', user.phone_number)
    
    image = request.data.get('image')
    if image:
        user.image = image
    
    password = request.data.get('password')
    if password:
        user.password = make_password(password)

    user.save()

    user_data = {
        "username": user.username,
        "email": user.email,
        "image": user.image.url if user.image else None
    }

    return Response({"Msg": "User updated successfully", "user": user_data}, status=status.HTTP_200_OK)
@api_view(['GET', 'POST'])
def registerDriver(request):
    name = request.data.get('name')
    phone_number = request.data.get('phone_number')
    address = request.data.get('address')
    car_number = request.data.get('car_number')
    driver_image = request.data.get('driver_image')
    car_image = request.data.get('car_image')
    vehicle_type = request.data.get('vehicle_type')
    price=request.data.get('ppk')
    city = request.data.get('city')  

    driver_registration = DriverRegistration(
        name=name,
        phone_number=phone_number,
        address=address,
        car_number=car_number,
        driver_image=driver_image,
        car_image=car_image,
        vehicle_type=vehicle_type,
        price=price,
        city=city  

    )
    driver_registration.save()

    return Response({'message': 'Driver registration successful'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getDrivers(request):
    if request.method == 'GET':
        vehicle = request.GET.get('vehicle')
        city=     request.GET.get('city')

        if vehicle:
            drivers = DriverRegistration.objects.filter(status='active', vehicle_type=vehicle,city=city)
        else:
            drivers = DriverRegistration.objects.filter(status='active')

        driver_list = []

        for driver in drivers:
            driver_data = {
                'name': driver.name,
                'phone_number': driver.phone_number,
                'address': driver.address,
                'car_number': driver.car_number,
                'driver_image': driver.driver_image.url if driver.driver_image else '',
                'car_image': driver.car_image.url if driver.car_image else '',
                'type': driver.vehicle_type,
                'price': driver.price,
                'city':driver.city
            }
            driver_list.append(driver_data)

        return Response({'drivers': driver_list}, status=200)
    else:
        return Response({'message': 'Invalid request method'}, status=405)
    
@api_view(['GET', 'POST'])
def deleteAllDrivers(request):
    try:
        # Delete all drivers with status 'active'
        deleted_count, _ = DriverRegistration.objects.filter(status='active').delete()

        return Response({"message": f"Deleted {deleted_count} drivers"}, status=200)

    except DriverRegistration.DoesNotExist:
        return Response({'message': 'No active drivers to delete'}, status=200)




@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    user = CustomUser.objects.filter(email=email).first()

    if user is not None:
        # Generate a password reset token and link
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)
        reset_link = f"http://127.0.0.1:8000/reset/{uid}/{token}/"

        # Send the reset link to the user's email
        send_mail(
            'Password Reset',
            f'Click the following link to reset your password: {reset_link}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return Response({'msg': 'Password reset link sent to your email.'}, status=200)
    else:
        return Response({'error': 'User with that email does not exist.'}, status=400)