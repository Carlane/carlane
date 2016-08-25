from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
from datetime import timedelta
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from django.core.mail import EmailMultiAlternatives
import requests#to send python post request
import json
from decimal import Decimal
import codecs


from Universal.models import CarBrands , User , UserCar , User_Type , CarModels , Car_Joint, User_Address , UserStatus , Request,Request_Allocation , Request_Status , Geography
from Universal.models import Service_Type , Joint_Service_Mapping , Joint_Driver_Mapping , Driver_Allocation_Status , TimeSlot , Joint_Allocation_Status , Request_Feedback

def send_welcome_email2(request , receiver , mailsubject , name):
    # Load the image you want to send as bytes
    img_data = open('carlane.png', 'rb').read()
    print('iamge data read')
    # Create a "related" message container that will hold the HTML
    # message and the image. These are "related" (not "alternative")
    # because they are different, unique parts of the HTML message,
    # not alternative (html vs. plain text) views of the same content.
    html_part = MIMEMultipart(_subtype='related')
    print('html part okay')
    # Create the body with HTML. Note that the image, since it is inline, is
    # referenced with the URL cid:myimage... you should take care to make
    # "myimage" unique
    body = MIMEText('<p>Hello <img src="cid:myimage" /></p>', _subtype='html')
    html_part.attach(body)
    print('html part okay 2')
    # Now create the MIME container for the image
    img = MIMEImage(img_data, 'png')
    img.add_header('Content-Id', '<myimage>')  # angle brackets are important
    img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
    html_part.attach(img)
    print('notification preparing')
    print('html part okay 3')
    msg.send()


def send_welcome_email4(request , receiver , mailsubject , name):
    d = Context({ 'user': name })
    html_content = render_to_string('Universal/email/NOTIFICATIONBLUE.html', d)
    #text_content = render_to_string('foo.txt', context)
    msg = EmailMultiAlternatives(mailsubject, 'text_content',
                                 'mycarlane@mycarlane.com', [receiver])

    msg.attach_alternative(html_content, "text/html")

    msg.mixed_subtype = 'related'

    for f in ['templates/Universal/email/images/PROMO-GREEN2_01_02.jpg', 'templates/Universal/email/images/PROMO-GREEN2_01_01.jpg']:
        fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        head, tail = os.path.split(f)
        print('tail ', tail)
        msg_img.add_header('Content-ID', '<{}>'.format(tail))
        msg.attach(msg_img)

    msg.send()

def joint_request_email(request , receiver , mailsubject , name):
    try:
        context = Context({ 'user': name })
        html_content = render_to_string('Universal/joint_request_email/index.html', context)
        #text_content = render_to_string('foo.txt', context)
        msg = EmailMultiAlternatives(mailsubject, 'text_content',receiver, [receiver])
        msg.attach_alternative(html_content, "text/html")

        msg.mixed_subtype = 'related'

        for f in ['templates/Universal/joint_request_email/images/mycarlane.png', 'templates/Universal/email/images/PROMO-GREEN2_01_01.jpg']:
            fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
            msg_img = MIMEImage(fp.read())
            fp.close()
            head, tail = os.path.split(f)
            print('tail ', tail)
            msg_img.add_header('Content-ID', '<{}>'.format(tail))
            msg.attach(msg_img)

        msg.send()
    except Exception as inst:
        print('Error in Emailing Request mail to joint')
        print(type(inst))
        print(inst.args)
        print(inst)
        print('Error End Email')


def send_welcome_email3(request , receiver , mailsubject , name):
    plaintext = 'This is an important message.'
    htmly     = get_template('Universal/email/NOTIFICATIONBLUE.html')
    d = Context({ 'user': name })
    html_content = render_to_string('Universal/email/NOTIFICATIONBLUE.html', d)

    subject, from_email, to = 'hello', 'triton.core.tech@gmail.com', 'aloksingh.itbhu@gmail.com'
    #text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, plaintext, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.mixed_subtype = 'related'
    img_data = open('carlane.png', 'rb').read()
    img = MIMEImage(img_data, 'png')
    img.add_header('Content-Id', '<myimage>')  # angle brackets are important
    img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
    msg.attach(img)
    msg.send()

def send_welcome_email(request , receiver , mailsubject , name):
    print('EMAILING')
    #print(os.path.dirname(os.path.abspath(__file__)))
    #print(os.getcwd())
    try:
        subject = mailsubject
        to = [receiver]
        from_email = 'triton.core.tech@gmail.com'
        ctx = {
        'user': name
        }

        message = get_template('Universal/email/NOTIFICATIONBLUE.html').render(ctx)
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
    except Exception as inst:
        print('Error in Emailing')
        print(type(inst))
        print(inst.args)
        print(inst)
        print('Error End Email')

def sendnotification(token , title , message):
    fireurl = 'https://fcm.googleapis.com/fcm/send'
    body = 'Test Message'
    print('user token',token)
    notification = {}
    notification['message'] = message
    notification['title'] = title
    arraytosend = {'to':token,'data':notification}
    headers = {"Content-Type":"application/json","Authorization":"key=AIzaSyDyFp7dzNe5DD7Q3MvcCAk0a-xLxX4Xut0"}
    r = requests.post(fireurl , data =  json.dumps(arraytosend) , headers = headers)
    print('notification sent' , r.content)







# Create your views here.
@api_view(['GET' , 'POST'])
def cardetails(request, pk , format = None):
    #Get the details of Car for the user whose user id is sent as primary_key
    if request.method == 'GET':
        print("==================== GET USER CAR DETAILS ====================")
        user_car_data  = UserCar.objects.filter(carownerid__userid = pk)
        returndata = []
        print('----- user id  ---- ',pk)
        for row in user_car_data:
            tempDict = {}
            tempDict['brand'] = row.carbrand.car_brand
            tempDict['model'] = row.carmodel.car_model
            tempDict['regno'] = row.registration_number
            returndata.append(tempDict)
            print(">>brand" , row.carbrand.car_brand)
            print(">>model" , row.carmodel.car_model)
            print(">>reg" , row.registration_number)
        #return Response(returndata)
        return Response({'response':[{'error':False,'reason':'','success':True,'id':pk,'responsedata':returndata}]} , status= status.HTTP_201_CREATED)
    #Add a new car for this User with primary key provided in request
    if(request.method == 'POST'):
        print("==================== POST USER CAR DETAILS ====================")
        requestdata = request.data
        existUser = User.objects.get(userid = pk)
        phoneupdateresult = False
        carupdateresult = False
        if existUser is None:
            print('User Not Added in system - Cant add car for a Ghost')
            return Response({'name':'NoUser'}, status.HTTP_400_BAD_REQUEST)
        newRegNumber = requestdata['registration_number']
        usermobile = requestdata['mobile_number']
        print('usermobile obrained in request is' , usermobile)
        try:
            print('>>>>Updating Mobile for user')
            existUser.joint_mobile = usermobile
            existUser.save()
            phoneupdateresult = True
            print('----Updating mobile Success')
        except:
            print('----Updating mobile Failed')
            phoneupdateresult = False

        existCar = UserCar.objects.filter(carownerid__userid=pk).filter(registration_number=newRegNumber)
        #car with same regisrtation number is already added
        if existCar is not None and len(existCar) != 0:
            print('Same Car(registration number ) is Already Added for this User-',existUser.first_name)
            return Response({'response':[{'error':True,'reason':'Car Already Exists','success':False,'id':existUser.userid }]} , status= status.HTTP_201_CREATED)
        # car brands and models table will be mapped between user app and this back end
        try:
            print('User and Registration OK ')
            carbrand_requestdata = requestdata['carbrand']
            carmodel_requestdata = requestdata['carmodel']
            print('car brand' , (carbrand_requestdata))
            print('car model' , (carmodel_requestdata))
            try:
                carsbrand = CarBrands.objects.get(car_brand = carbrand_requestdata)
            except:
                print("Not able to get info from DB" , carsbrand)
            if carsbrand is None:
                print('Cars Brand is None')
                #print(carsbrand[0])
            #print('CarBrand' , carsbrand.car_brand)
            try :
                print("Getting car models - ", carmodel_requestdata)
                carsmodel =  CarModels.objects.get(car_model = carmodel_requestdata)
            except :
                print("Error in getting Car Modes")
            print('Second doubt')
            #print('car brand is ' , carsbrand.car_brand)
            print('carmode is' , carsmodel.car_model)
            print('carmodel brand is' , carsbrand.car_brand)
            print('carownerid' , existUser.userid)
            print('registrion number is' , newRegNumber)

            newCarEntry = UserCar(carownerid = existUser,   carbrand = carsbrand , carmodel = carsmodel , registration_number = newRegNumber)
            newCarEntry.save()
            profilestatus = UserStatus.objects.get(user_status = 'CarProfile')
            print('Car Add Existing User Sign Up',profilestatus.user_status)
            existUser.user_status = profilestatus
            existUser.save()
            sendnotification(existUser.firebase_token ,'Carlane ' , 'You added a Car')
        except:
            return Response({'response':[{'error':True,'reason':'FailedToAdd','success':False,'id':existUser.userid,'phoneresult':phoneupdateresult }]} , status = status.HTTP_201_CREATED)

        return Response({'response':[{'registration_number': newCarEntry.registration_number ,'name':existUser.first_name,'error':False,'reason':'CarAdded','success':True,'id':existUser.userid,'user_status':existUser.user_status.user_status,'mobilebkEnd':usermobile ,'phoneresult':phoneupdateresult}]} , status = status.HTTP_201_CREATED)


@api_view(['GET' ,'POST'])
def usersignup(request , format = None):
    if(request.method == 'POST'):
        userdata = request.data
        print('Alok' , userdata['firstname'])
        fname = userdata['firstname']
        lname = userdata['lastname']
        email = userdata['email']
        mobile = userdata['mobile']
        token = userdata['token']
        firebase_token = userdata['firebasetoken']
        print('firebasetoken sign in' , firebase_token)
        #validate if the same email or phone is present in the database
        existUser = User.objects.filter(email=email ,access_token = token)
        print('existUser' , existUser)
        if existUser is None or len(existUser) == 0:
            print('existUser is None')

        elif existUser is not None:
            print('existUserID' , existUser[0].userid)
            existUser[0].firebase_token = firebase_token
            print('Existing Users New firebase_token Token is ',existUser[0].firebase_token)
            existUser[0].save()
            print('firebase save OK')
            return Response({'response':[{'error':False,'reason':'UserExists','success':True,'id':existUser[0].userid ,'user_status':existUser[0].user_status.user_status}]} , status = status.HTTP_201_CREATED)
            #if i rtrn  HTTP_400_BAD_REQUEST i dont get any data returned
        try:
            # if no duplicate data entry then save the data
            usertype = User_Type.objects.filter(name='Customer')
            newuserstatus = UserStatus.objects.get(user_status = 'NewProfile')
            newUserEntry = User(userTypeId=usertype[0] , first_name = fname , last_name = lname, email = email , joint_mobile=mobile,access_token = token,firebase_token = firebase_token ,is_active = True , status = 'Normal',user_status = newuserstatus)
            newUserEntry.save()
            print('notification preparing')
            send_welcome_email4(request ,email,'Welcome to Carlane',fname)
            sendnotification(firebase_token, 'Carlane Welcome' , 'Thanks for Signing Up')
        except User.DoesNotExist:
            return Response({'response':[{'error':True,'reason':'FailedtoAdded','success':False,'id':-1, 'name':''}]}, status = status.HTTP_400_BAD_REQUEST)
        print('New User Status',newUserEntry.user_status.user_status)
        return Response({'response':[{'error':False,'reason':'Added','success':True,'id':newUserEntry.userid , 'name':newUserEntry.first_name ,'user_status':newUserEntry.user_status.user_status}]} , status = status.HTTP_201_CREATED)

    #if(request.method =='GET'):
    #    dict = {'name':'alok'}
    #    return Response(dict)

@api_view(['GET','POST'])
def address(request , pk , format = None):
    if request.method == 'GET':
        print('Get is Fine for Address')
        try :
            user = User.objects.get(userid = pk)
            q = User_Address.objects.filter(user_id = user)
        except:
            return Response([],status.HTTP_400_BAD_REQUEST)
        addressList = []
        for row in q:
            tempDict = {}
            tempDict['name'] = user.first_name
            tempDict['Line1'] =  row.line1
            tempDict['Line2'] =  row.line2
            tempDict['city'] =  row.city
            tempDict['state'] =  row.state
            tempDict['country'] =  row.country
            addressList.append(tempDict)

        return Response(addressList , status.HTTP_201_CREATED)
    elif request.method == 'POST':
        print('POSTING for address')
        user_request_data = request.data
        user = User.objects.get(userid = pk)
        address_line1= user_request_data['line1']
        address_line2= user_request_data['line2']
        address_city= user_request_data['city']
        address_state= user_request_data['state']
        address_country= user_request_data['country']
        address_lat= user_request_data['lat']
        address_long= user_request_data['long']
        newaddress = User_Address(user_id = user , line1 =address_line1 , line2 = address_line2 , city = address_city , state = address_state ,country = address_country,latt = address_lat , longg = address_long)
        newaddress.save()
        return Response({'name': str(newaddress.id)} , status.HTTP_201_CREATED)


@api_view(['POST'])
def initiate_request(request , pk , format = None):
    requestdata = request.data
    requesting_user = User.objects.get(userid = pk)
    request_service_name = requestdata['servicename']
    print('request_service_name ', request_service_name)

    requested_service_id = requestdata['servicetype']
    print('requested_service_id', requested_service_id)

    #requested_date = requestdata['date']
    requested_timeslotfrom =  datetime.datetime.strptime(requestdata['timeSlotfrom'], '%H:%M:%S').time()#09:00:00
    requested_timeslotto = datetime.datetime.strptime(requestdata['timeSlotto'], '%H:%M:%S').time()#requestdata['timeSlotto']#12:000:00
    requested_geo_id = requestdata['geo']
    print('requested_geo_id ', requested_geo_id)
    available_services = Service_Type.objects.get(name=request_service_name , geo_id = requested_geo_id)
    print('available_services are ' ,available_services)
    print(requested_timeslotfrom)
    print(requested_timeslotto)
    #find all the Joint which are catering this Service
    try :
        print('Finding Joints from Joint Service Mapping')
        q = Joint_Service_Mapping.objects.filter(service_type_id__id = requested_service_id , service_slot_count__gte =1)
    except :
        return Response({'error:','No such service exists'}, status.HTTP_400_BAD_REQUEST)
    #find out all the drivers of the Joints found in above step
    print('Finding Drivers of suitable Car Joints')
    drivermapping = []
    for each_mapping in q:
        print(each_mapping.car_joint_id.name , each_mapping.service_type_id.name)
        dmap = Joint_Driver_Mapping.objects.filter(car_joint_id = each_mapping.car_joint_id)
        print('dmap', len(dmap),dmap)
        for maps in dmap:
            drivermapping.append(maps)
            print('maps',maps.driver_user_id.first_name)
    #find out all the drivers which are available for the requested service
    print('Joint Driver MApping',len(drivermapping))
    drivers = []
    time_slot_for_user =  TimeSlot.objects.filter(time_from = requested_timeslotfrom , time_to = requested_timeslotto , geo_id = requested_geo_id)
    print('timeslotuser',len(time_slot_for_user),time_slot_for_user[0].display_name)
    for each_drivermap in drivermapping:
            print('each_rider ',each_drivermap.driver_user_id.userid ,time_slot_for_user[0].id)
            rider = Driver_Allocation_Status.objects.filter(driver_user_id = each_drivermap.driver_user_id.userid , current_count__lte = 4, time_slot_id = time_slot_for_user[0].id)
            print('rider len',len(rider))
            for each_rider in rider:
                tempdict = {'name' , each_rider.driver_user_id.first_name}
                drivers.append(tempdict)
    print('drivers -',len(drivers))
    return Response({'response':[{'error':False,'reason':'Drivers Available','success':True,'id':pk , 'name':requesting_user.first_name ,'user_status':requesting_user.user_status.user_status ,'drivers_data':drivers}]} , status = status.HTTP_201_CREATED)

@api_view(['POST'])
def findSlotsForDate(request , pk , format = None):
    print("==================Find Slot Request===================");
    user = User.objects.get(userid = pk)
    print("Request Initiated By User " , user.first_name)
    requestdata = request.data
    request_service_id = requestdata['serviceid']
    available_services = Service_Type.objects.get(id = request_service_id)
    days_ahead_of_current_date = requestdata['daysahead']
    print('request service id is ' , request_service_id)
    print('days ahead from current date' , days_ahead_of_current_date)
    request_Date = datetime.datetime.now() + timedelta(days=int(days_ahead_of_current_date))
    #print('length of available services is ' , len(available_services))
    #find all the Joint which are catering this Service
    try :
        print('Finding Joints from Joint Service Mapping')
        q = Joint_Service_Mapping.objects.filter(service_type_id__id = request_service_id , service_slot_count__gte =1)
    except :
        return Response({'error:','No such service exists'}, status.HTTP_400_BAD_REQUEST)

    print('Found %d Joints',len(q))
    print('Finding Drivers of Suitable Car Joints')
    drivermapping = []
    for each_mapping in q:
        print(each_mapping.car_joint_id.name , each_mapping.service_type_id.name)
        dmap = Joint_Driver_Mapping.objects.filter(car_joint_id = each_mapping.car_joint_id)
        print('dmap', len(dmap),dmap)
        for maps in dmap:
            drivermapping.append(maps)
            print('maps',maps.driver_user_id.first_name)

    print('Found %d Driver for %d Joints',len(drivermapping),len(q))
    #find out all the drivers which are available for the requested service.
    #We need to find information for each timeslot- if there is  a driver available in that time slot mark it as available
    #Get all the time slots
    time_slots =  TimeSlot.objects.all()
    response_time_slots=[]
    for each_drivermap in drivermapping:
        for timeslot in time_slots:
            print('each_rider ',each_drivermap.driver_user_id.userid ,timeslot.display_name)
            #Find the drivers allocation for date and time slot , If No allocation is there it means driver is available
            #If Allocation is there then check if current_count__lte = 4 then slot is available
            rider = Driver_Allocation_Status.objects.filter(driver_user_id = each_drivermap.driver_user_id.userid , date = request_Date, time_slot_id = timeslot.id)
            if len(rider) > 0:
                try:
                    if rider[0].current_count <=5:
                        print('Information available for this slot and count is also less')
                        slotAvailableDict = {timeslot.id:True}
                        #slotAvailableDict = {'timeslotid',timeslot.id}
                        response_time_slots.append(slotAvailableDict)
                        print('response slot en',len(response_time_slots))
                        if len(response_time_slots) ==  len(time_slots):
                            break
                except:
                    print('this slot id is already available' , timeslot.id)
            else :
                print('No Information means entire slot is empty')
                #No Information means entire slot is empty
                slotAvailableDict = {timeslot.id:True}
                #slotAvailableDict = {'timeslotid',timeslot.id}
                response_time_slots.append(slotAvailableDict)
                print('response slot en',len(response_time_slots))
                if len(response_time_slots) ==  len(time_slots):
                    break



        if len(response_time_slots) ==  len(time_slots):
            break
    print('return data length is ',len(response_time_slots))
    return Response({'response':[{'error':False,'reason':'Slots Available','success':True,'id':pk  ,'responsedata':response_time_slots}]} , status = status.HTTP_201_CREATED)

@api_view(['POST'])
def changedriver(request , pk , format = None):
    print('=====================Change Driver Request Received=============================')
    requestdata = request.data
    new_driver_id = requestdata['newdriverid']
    request_id = requestdata['serviceid']
    print('New Driver Id' , new_driver_id)
    print('Reques Id to change',request_id)
    request_to_change = Request.objects.get(id = request_id)
    new_driver = User.objects.get(userid= new_driver_id)
    print('New driver Name is ', new_driver.first_name)
    requestalloc_to_change = Request_Allocation.objects.get(request_id = request_id)
    print('Getting old driver Updating His allocation')
    old_driver = requestalloc_to_change.driver_id
    old_driver_allocation = Driver_Allocation_Status.objects.get(driver_user_id = old_driver , date = request_to_change.date , time_slot_id = request_to_change.time_slot_id)
    if(old_driver_allocation.current_count > 0):
        old_driver_allocation.current_count -=1
        old_driver_allocation.save()
    print('Updated Old Driver ',old_driver.first_name)
    print('Finding allocation of new driver')
    print('Getting old driver Updating His allocation on given date time slot',new_driver.first_name)
    try:
        rider = Driver_Allocation_Status.objects.filter(driver_user_id = new_driver, date = request_to_change.date , time_slot_id = request_to_change.time_slot_id)

    except Exception as inst:
        print('Error in finding new driver allocation status ')
        print(type(inst))
        print(inst.args)
        print(inst)
        rider = None
    if len(rider) > 0 and rider[0].current_count > 5:
        print('this rider is already booked so search for next one')
        return Response({'response':[{'error':True,'reason':'Driver Booked','success':False,'id':new_driver.userid }]} , status = status.HTTP_201_CREATED)
        #return response
    else:
        if rider is None or len(rider) <= 0:
            # create new driver allocation
            print("creating new driver allocation")
            driver_allocation_obj = Driver_Allocation_Status(date = request_to_change.date  ,current_count = 1 ,driver_user_id =  new_driver,time_slot_id = request_to_change.time_slot_id)
            driver_allocation_obj.save()
            print("Success driver allocation success id is " , driver_allocation_obj.id)
        else:
            print("Updating driver allocation status")
            rider[0].current_count = rider[0].current_count + 1
            rider[0].save()
            print("Succes driver alocation update - new count is ",rider[0].current_count)
        requestalloc_to_change.driver_id = new_driver
        requestalloc_to_change.save()
        print('Update Request Allocation Also , New Driver Allocated')
        return Response({'response':[{'error':False,'reason':'New Driver Changed Successfully','success':True,'id':new_driver.userid }]} , status = status.HTTP_201_CREATED)





@api_view(['POST'])
def initreq(request , pk , format = None):
    print('=====================WASH Request Received=============================')
    who_requested  = User.objects.get(userid = pk)
    print('Request Generated By ' , who_requested.first_name)
    requestdata = request.data
    request_service_id = requestdata['serviceid']
    request_slot_id= requestdata['timeslot_id']
    request_car =requestdata['carno']
    request_latt= requestdata['latt']
    request_longg = requestdata['longg']
    print('Printing data received in Request service , slot , car', request_service_id,    request_slot_id,request_car)
    print('Lattitude' , request_latt)
    print('Lattitude' , request_longg)

    days_ahead_of_current_date = requestdata['daysahead']
    print('days ahead from current date' , days_ahead_of_current_date)
    request_Date = datetime.datetime.now() + timedelta(days=int(days_ahead_of_current_date))

    time_slot = TimeSlot.objects.get(id = request_slot_id)
    #Again First find the drivers for the given time slot
    try :
        print('Finding Joints from Joint Service Mapping')
        joint_service_map = Joint_Service_Mapping.objects.filter(service_type_id__id = request_service_id , service_slot_count__gte =1)
    except :
        return Response({'error:','No such service exists'}, status.HTTP_400_BAD_REQUEST)

    print('Found %d Joints for Selected Service',len(joint_service_map))
    print('Finding Drivers of Suitable Car Joints')

    for each_joint in joint_service_map:
        print('Finding Driver for this Joint for this Service', each_joint.car_joint_id.name , each_joint.service_type_id.name)
        joint_driver_map = Joint_Driver_Mapping.objects.filter(car_joint_id = each_joint.car_joint_id)
        print('This Joint has this N umber of drivers', len(joint_driver_map))
        for driverMapObject in joint_driver_map:
            print('We will find allocation status on given date time slot for this driver name',driverMapObject.driver_user_id.first_name)
            try:
                rider = Driver_Allocation_Status.objects.filter(driver_user_id = driverMapObject.driver_user_id.userid , date = request_Date, time_slot_id = time_slot.id)
            except Exception as inst:
                print('Error in finding driver allocation status')
                print(type(inst))
                print(inst.args)
                print(inst)
                rider = None

            print('driver name allocation',driverMapObject.driver_user_id.first_name)
            print('length of rider ' ,len(rider))
            if len(rider) > 0 and rider[0].current_count > 5:
                print('this rider is already booked so search for next one')
                continue
            else:
                # no allocations for this guy yet so  allocate this guy
                print('Allocating this driver - name is ---- ', driverMapObject.driver_user_id.first_name)
                user = User.objects.get(userid =pk)
                user_car = UserCar.objects.get(registration_number = request_car)
                request_current_status = Request_Status.objects.get(current_status ='request_init')
                print("request current status" ,request_current_status.current_status)
                newRequest = Request(user_id = user , time_slot_id = time_slot ,user_car_id = user_car , date = request_Date , current_status = request_current_status , latt = request_latt , longg = request_longg)
                newRequest.save()
                print('Request Placed -- New request id ' ,newRequest.id)
                joint = Car_Joint.objects.get(id = each_joint.car_joint_id.id)
                servicetype = Service_Type.objects.get(id = request_service_id)
                newRequestAllocation = Request_Allocation(request_id = newRequest, car_joint_id = joint , service_type_id= servicetype , driver_id = driverMapObject.driver_user_id)
                newRequestAllocation.save()
                print('NewRequest Allocation id' , newRequestAllocation.id)
                #increase joint allocation status(currently does not handler dates)
                current_allocation_count = 0
                try:
                    existJointAllocationStatus = Joint_Allocation_Status.objects.get(car_joint_id =  joint , service_type_id = servicetype , date = request_Date)
                except:
                    print('Error in Finding Existing Joint Allocation')
                    existJointAllocationStatus = None

                if existJointAllocationStatus is not None:
                    current_allocation_count = existJointAllocationStatus.current_count
                    existJointAllocationStatus.current_count +=1
                    print('Count for this Joints Existing Allocation',existJointAllocationStatus.current_count)
                    existJointAllocationStatus.save()
                else:
                    print('Its a new Joint Allocation for this joint ')
                    newJointAllocationStatus = Joint_Allocation_Status(car_joint_id = joint , service_type_id = servicetype , current_count =1 , date = request_Date)
                    newJointAllocationStatus.save()

                #increase the count of driver allocation status
                if rider is None or len(rider) <= 0:
                    # create new driver allocation
                    print("creating new driver allocation")
                    driver_allocation_obj = Driver_Allocation_Status(date = request_Date ,current_count = 1 ,driver_user_id =  driverMapObject.driver_user_id ,time_slot_id = time_slot)
                    driver_allocation_obj.save()
                    print("Success driver allocation success id is " , driver_allocation_obj.id)
                else:
                    print("Updating driver allocation status")
                    rider[0].current_count = rider[0].current_count + 1
                    rider[0].save()
                    print("Succes driver alocation update - new count is ",rider[0].current_count)
                print('updating request to driver allocated')
                request_current_status = Request_Status.objects.get(current_status ='driver_allocated')
                newRequest.current_status = request_current_status
                newRequest.save()
                print('updated request')
                print('updating user status to pending request ')
                print('alok log ')
                profilestatus = UserStatus.objects.get(user_status = 'RequestPending')
                user.user_status = profilestatus
                user.save()
                print('Success Updated User Status to RequestPending')
                print('sending request email')
                joint_request_email(request,user.email,'Request Placed',user.first_name)
                print('email sent')



                return Response({'response':[{'error':False,'reason':'Booking Confirmed','success':True,'id':pk  ,'driver':driverMapObject.driver_user_id.first_name,
                'joint':each_joint.car_joint_id.name,'driverphone':driverMapObject.driver_user_id.joint_mobile,'service_id':request_service_id,'time_slot_id':time_slot.id,'request_status':newRequest.current_status.id,'request_date':newRequest.date}]} , status = status.HTTP_201_CREATED)
    return Response({'response':[{'error':True,'reason':'No Joints','success':False,'id':pk }]} , status = status.HTTP_201_CREATED)


@api_view(['GET','POST'])
def requeststatus_info(request , pk , format = None):
    if request.method == 'POST':
        print('=======================   Request Status GET Received =========================')
        requestdata = request.data
        request_data_car_reg = requestdata['car_reg']
        #find the request pending for this car_reg
        # assumption only one request for user is ongoing - rest all are completed
        try:
            who_requested  = User.objects.get(userid = pk)
            print('RequestStatus initiated by ', who_requested.first_name)
            car = UserCar.objects.get(registration_number = request_data_car_reg)
            print('obtained car data')
            print('car registration',request_data_car_reg)
            try:
                request_obj = Request.objects.get(user_car_id = car , current_status__id__lte=7)
            except:
                print('No Ongoing Request So Handling in Exception Handler')
                return Response({'response':[{'error':False,'reason':'No OnGoing Request','success':True,'id':pk,'request_status':8 }]} , status = status.HTTP_201_CREATED)
            print('obtained request data',request_obj.id)
            #NOTES currently we are savinf service typ service type in Request Allocation , we should move it to request since it received from User
            request_alloc_obj = Request_Allocation.objects.get(request_id = request_obj)
        except:
            print('error in Request Status')
            return Response({'response':[{'error':True,'reason':'Unknown','success':False,'id':pk }]} , status = status.HTTP_201_CREATED)

        return Response({'response':[{'error':False,'reason':'No Joints','success':True,'id':pk,'request_status':request_obj.current_status.id,'date':request_obj.date,'timeslot':request_obj.time_slot_id.id,'car_reg':car.registration_number,'carmodel':car.carmodel.car_model,'carbrand':car.carbrand.car_brand,'drivermobile':request_alloc_obj.driver_id.joint_mobile,'driverfirstname':request_alloc_obj.driver_id.first_name ,'driverlastname':request_alloc_obj.driver_id.last_name,'latt':request_alloc_obj.car_joint_id.latt,'longg':request_alloc_obj.car_joint_id.longg}]} , status = status.HTTP_201_CREATED)



@api_view(['GET','POST'])
def driverjobdetails(request , pk , format = None):
    if request.method == 'GET':
        try:
            print("==================GOT DRIVER REQUEST===================");
            driver = User.objects.get(userid = pk)
            print("Driver Details " ,driver.first_name , driver.userid , driver.joint_mobile)
            print(">>>>> GET ONGOING DRIVER REQUESTS FROM REQUEST ALLOCATION")
            driver_jobs=[]
            driver_req_allocation_objs = Request_Allocation.objects.filter(driver_id = driver , request_id__current_status__id__lte=7)
            for req_alloc in driver_req_allocation_objs:
                dictionary_req= {}
                #gte other drivers which can handle this request_id
                print('getting car joints')
                try:
                    carjoint = req_alloc.car_joint_id
                    print('carjoint name',carjoint.name)
                    driver_joints_map = Joint_Driver_Mapping.objects.filter(car_joint_id = carjoint)
                    print('joint driver mapping', len(driver_joints_map))
                    alternate_driver = []
                    for eachdriver_jointmapping in driver_joints_map:
                        driver_id_name_map = {}
                        if(int(pk) != int(eachdriver_jointmapping.driver_user_id.userid)):
                            print('alternate driver id' , eachdriver_jointmapping.driver_user_id.userid , pk)
                            driver_id_name_map['alternate_id'] = eachdriver_jointmapping.driver_user_id.userid
                            print('alternate driver name' , eachdriver_jointmapping.driver_user_id.first_name)
                            driver_id_name_map['alternate_name'] = eachdriver_jointmapping.driver_user_id.first_name
                            alternate_driver.append(driver_id_name_map)
                    print('size of alternate drivers', len(alternate_driver))
                    dictionary_req['alternate_drivers'] = alternate_driver
                except Exception as inst:
                    print('Error in joint driver mapping')
                    print(type(inst))
                    print(inst.args)
                    print(inst)

                req_obj = req_alloc.request_id
                print('Get Req Id')
                dictionary_req['requestid'] = req_obj.id
                print('Get Req time slot id')
                dictionary_req['timeslotid'] = req_obj.time_slot_id.id
                print('Get Req Time slot name')
                dictionary_req['timeslotdisplay'] = req_obj.time_slot_id.display_name
                print('Get Req Car Reg No')
                dictionary_req['carno'] = req_obj.user_car_id.registration_number
                print('Get User Car Brand ')
                dictionary_req['carbrand'] = req_obj.user_car_id.carbrand.car_brand
                print('Get User Car Model')
                dictionary_req['carmodel'] = req_obj.user_car_id.carmodel.car_model
                print('Get Req User')
                dictionary_req['customer_name'] = req_obj.user_id.first_name
                print('Get User Mobile')
                dictionary_req['customer_mobile'] = req_obj.user_id.joint_mobile
                print('Get Req Status')
                dictionary_req['reqstatus'] = req_obj.current_status.id
                print('Get Req Date')
                dictionary_req['date'] = req_obj.date
                print('Get Req Car Joint')
                carjoint = Car_Joint.objects.get(id = req_alloc.car_joint_id.id)
                dictionary_req['joint'] = req_alloc.car_joint_id.name;
                print('adding service id')
                dictionary_req['serviceid'] = req_alloc.service_type_id.id
                print('adding latt' , req_obj.latt)
                dictionary_req['latt'] = req_obj.latt
                print('adding longg' , req_obj.longg)
                dictionary_req['longg'] = req_obj.longg

                driver_jobs.append(dictionary_req)


            print('size of dic req',len(driver_jobs))
            return Response({'response':[{'error':False,'reason':'FetchedDetails','success':True,'id':pk,'responsedata':driver_jobs }]} , status = status.HTTP_201_CREATED)
        except:
            return Response({'response':[{'error':True,'reason':'Unknown','success':False,'id':pk }]} , status = status.HTTP_201_CREATED)
    if request.method == 'POST':
        print("==================POST DRIVER REQUEST UPDATE JOB STATUS ===================");
        try:
            driver = User.objects.get(userid = pk)
            print("Driver Details " ,driver.first_name , driver.userid , driver.joint_mobile)
            print('Another Driver detail')
            requestdata = request.data
            print('Got request Data')
            requestid_toupdate = requestdata['requestid']
            print('Get Requestid' ,requestid_toupdate)
            request_obj = Request.objects.get(id = requestid_toupdate)
            print('Get Request Obj')
            print('currentstatusid' , request_obj.current_status.id)
            print('currentstatusid plus one' , request_obj.current_status.id +1)
            print('get plus request obj')
            newid = request_obj.current_status.id +1
            print('new id is' , str(newid))

            if newid <= 8:
                print('less than 8')
                newstatus = Request_Status.objects.get(id = newid)
                print('Get Request Status')
                request_obj.current_status = newstatus
                print('Updated Status')
                request_obj.save()
                print('Save')
                sendnotification(request_obj.user_id.firebase_token,'Carlane Service Status' , 'Your Service Status is Updated.')
            else:
                if newid > 8:
                    print('status is 8 , move it to feedback pending')
                    print('all okay Request Status is Pending')


            #if status is now completed we should now do some extra process
            #1. Change User status here , and send appropriate response so that userapp will also change user status
            #2. Do we need to update anything for driver ??
            #if newid == 8:
                #print("Request is completed so change user status , Getting Uuser id from Request")
                #user_requester = request_obj.user_id
                #user_requester.user_status = UserStatus.objects.get(id = 2)
                #user_requester.save()
                #print('User Status Update to Car Profile')




            return Response({'response':[{'error':False,'reason':'UpdatedStatus','success':False,'id':pk,'newstatusid':newstatus.id}]} , status = status.HTTP_201_CREATED)
        except:
            print('Error')
            return Response({'response':[{'error':True,'reason':'Unknown','success':False,'id':pk }]} , status = status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def cancelrequest(request , pk , format = None):
    if request.method == 'POST':
        print("===================== CANCEL ORDER =====================================")
        requestdata = request.data
        try:
            who_requested  = User.objects.get(userid = pk)
            print('cancel request submitted by ',who_requested.first_name)
            print('Getting Request Object')
            request_obj = Request.objects.get(user_id = pk , current_status__id__lte = 4)
            print("Some log to check request object")
            if request_obj is None:
                print("No Request to Cancel")
                return Response({'response':[{'error':True,'reason':'No Request To Cancel','success':False,'id':pk }]} , status = status.HTTP_201_CREATED)
            else:
                print("Cancelling the Request")
                newstatus = Request_Status.objects.get(id = 11)
                request_obj.current_status = newstatus
                request_obj.save()
                #update user status back to carprofile
                user_requester = request_obj.user_id
                user_requester.user_status = UserStatus.objects.get(id = 2)
                user_requester.save()
                #todo update driver allocation status and joint alloecation status
                driver_allocation = Driver_Allocation_Status.objects.get(date = request_obj.date , time_slot_id = request_obj.time_slot_id)
                print("updating driver allocation")
                driver_allocation.current_count -=1
                driver_allocation.save()
                print("driver allocation update SUCCESS")
                print("Updating Joint Allocation Status")
                request_alloc = Request_Allocation.objects.get(request_id = request_obj.id)
                joint_allocation = Joint_Allocation_Status.objects.get(date = request_obj.date, car_joint_id = request_alloc.car_joint_id, service_type_id = request_alloc.service_type_id)
                joint_allocation.current_count -=1
                joint_allocation.save()
                print("Joint Allocation Status update SUCCESS")
        except Exception as inst:
            print('error in cancel Status')
            print(type(inst))
            print(inst.args)
            print(inst)
            return Response({'response':[{'error':True,'reason':'Exception','success':False,'id':pk }]} , status = status.HTTP_201_CREATED)

        return Response({'response':[{'error':False,'reason':'CancelSuccess','success':True,'id':pk }]} , status = status.HTTP_201_CREATED)





@api_view(['GET','POST'])
def submitfeedback(request , pk , format = None):
    if request.method == 'POST':
        print("==============================    REQUEST  FEEDBACK ======================================")
        print('Feedback Values Status GET Received')
        requestdata = request.data
        driverrating = requestdata['driverrating']
        washrating = requestdata['washrating']
        overallrating = requestdata['overallrating']
        feedback_text = requestdata['feedback']
        #find the request pending for this car_reg
        # assumption only one request for user is ongoing - rest all are completed
        try:
            who_requested  = User.objects.get(userid = pk)
            print('feedback submitted by ',who_requested.first_name)
            print('Getting Request Object')
            request_obj = Request.objects.get(user_id = pk , current_status__id = 8)
            print('obtained request object ',request_obj.id)
            print('getting feedback')
            newfeedback = Request_Feedback(driverrating = float(driverrating) , washrating = float(washrating), overallrating = float(overallrating) , feedback_text = feedback_text , request_id = request_obj)
            newfeedback.save()
            all_completed_status = 10
            newstatus = Request_Status.objects.get(id = all_completed_status)
            request_obj.current_status = newstatus
            request_obj.save()
            print('feedback saved')
            print("Request is completed so change user status , Getting Uuser id from Request")
            user_requester = request_obj.user_id
            user_requester.user_status = UserStatus.objects.get(id = 2)
            user_requester.save()
            print('User Status Update to Car Profile')
        except Exception as inst:
            print('error in Request Status')
            print(type(inst))
            print(inst.args)
            print(inst)
            return Response({'response':[{'error':True,'reason':'Unknown','success':False,'id':pk }]} , status = status.HTTP_201_CREATED)

        return Response({'response':[{'error':False,'reason':'No Joints','success':True,'id':pk,'feedbackid':newfeedback.id}]} , status = status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def getuserrequests(request , pk , format = None):
    print("================================ GET USER REQUEST ====================================")
    if request.method == 'GET':
        requestdata = request.data
        try:
            who_requested  = User.objects.get(userid = pk)
            print('submitted by ',who_requested.first_name)
            print('Getting Request Object')
            all_requests = Request.objects.filter(user_id = pk)
            request_list = []
            for each_request in all_requests:
                request_map = {}
                request_alloc_obj = Request_Allocation.objects.get(request_id = each_request)

                request_map['time_slot_id'] = each_request.time_slot_id.id
                request_map['date'] = each_request.date
                request_map['current_status_id'] = each_request.current_status_id
                usercar = each_request.user_car_id
                usercarbrand = usercar.carbrand.car_brand
                request_map['usercarbrand'] = usercarbrand
                request_map['regno'] = usercar.registration_number
                usercarmodel = usercar.carmodel.car_model
                request_map['usercarmodel'] = usercarmodel
                request_map['servicetype'] = request_alloc_obj.service_type_id.name
                request_map['drivername'] = request_alloc_obj.driver_id.first_name
                try:
                    feedback = Request_Feedback.objects.get(request_id = each_request)
                    request_map['washrating'] = feedback.washrating
                    request_map['driverrating'] = feedback.driverrating
                    request_map['overallrating'] = feedback.overallrating
                except Exception as inst:
                    request_map['washrating'] = 0
                    request_map['driverrating'] = 0
                    request_map['overallrating'] = 0
                #request_map['driver_name'] = each_request.driver_id.first_name
                request_list.append(request_map)
            return Response({'response':[{'error':False,'reason':'Requests Available','success':True,'id':pk,'responsedata':request_list}]} , status = status.HTTP_201_CREATED)
        except Exception as inst:
            print('error in Request Status')
            print(type(inst))
            print(inst.args)
            print(inst)
            return Response({'response':[{'error':True,'reason':'Unknown','success':False,'id':pk }]} , status = status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def locationbasedServices(request , pk , format = None):
    print("================================ GET LOCATIONBASED SERVICES ====================================")
    if request.method == 'POST':
        requestdata = request.data
        try:
            who_requested  = User.objects.get(userid = pk)
            print('submitted by ',who_requested.first_name)
            print("latt " , requestdata['latt'])
            print("longg " , requestdata['longg'])
            print('Getting Car Joints')
            geo= Geography.objects.get(name__iexact="Hyderabad")
            if geo is None:
                print('Error in Geo')
            print('Geo is Okay')
            carjoints = Car_Joint.objects.filter(geo_id = geo)
            destinations=""
            for each_joint in carjoints:
                print('joint name for validation with second loop below' , each_joint.name)
                destinations=destinations+str(each_joint.latt) + ","+str(each_joint.longg)+"|"
            destinations = destinations[:-1]

            final_url="https://maps.googleapis.com/maps/api/distancematrix/json?units=metrics&origins="+ requestdata['latt'] + "," + requestdata['longg'] + "&destinations="+destinations+ "&key=AIzaSyDyFp7dzNe5DD7Q3MvcCAk0a-xLxX4Xut0"
            print(final_url)
            response = findDistance(final_url)
            distance_list = []
            print('===== Distances got from Google APIs response')
            for each_item in response:
                print('print distance value')
                print(each_item['distance']['text'])
                distance_list.append(each_item['distance']['value'])

            print("===========   Iterate CAR JOINTS and find services of their and add in a dictionary - key is service id ====")
            #again iterate the car joints so that we can prepare a dictionary to send data
            response_list = []
            data_for_user = {}# one dictionary for all the services
            count = 0
            for each_joint in carjoints:
                print('joint name for validation with second loop above' , each_joint.name)
                #find each service for this joint
                services = Joint_Service_Mapping.objects.filter(car_joint_id = each_joint)
                for each_service in services:
                    print(' key : service id' , str(each_service.service_type_id.id))
                    if str(each_service.service_type_id.id) in data_for_user:
                        print('key present in dict')
                        key = str(each_service.service_type_id.id)
                        print('key value' , data_for_user[key]['min_dist'])
                        old_dist = int(data_for_user[key]['min_dist'])
                        print('old_dist' , old_dist)
                        print('new dist' , distance_list[count])
                        new_dist = distance_list[count]
                        if old_dist > new_dist:
                            print('new distance is less so save this')
                            data_for_user[key]['min_dist'] = str(new_dist)
                        data_for_user[key]['joint_count'] = data_for_user[key]['joint_count'] +1

                    else:
                        print('key not in dict')
                        inside_dict = {}
                        inside_dict['joint_count'] = 1
                        print('  google distance for this service' , distance_list[count])
                        inside_dict['min_dist'] = distance_list[count]
                        print('  inside dict prepared' , inside_dict['min_dist'] )
                        print('  key : service id' , str(each_service.service_type_id.id))
                        key = str(each_service.service_type_id.id)
                        data_for_user[key] = inside_dict
                count+=1

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
        response_list.append(data_for_user)
        return Response({'response':[{'error':False,'reason':'Requests Available','success':True,'id':pk , 'responsedata':response_list}]} , status = status.HTTP_201_CREATED)


def findDistance(url):
    print('Firing Request')
    r = requests.get(url)
    print('request sent')
    print('notification sent' , r.content)
    try :
        reader = codecs.getreader("utf-8")
        a= json.loads(r.content.decode('utf-8'))
        print('json reading success')
        print('origin_addresses ' ,a['origin_addresses'][0])
        print('rows elements', a['rows'][0]['elements'][0]['distance']['value'])
        return a['rows'][0]['elements']
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
    return []
