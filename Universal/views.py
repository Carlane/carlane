from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime

from Universal.models import CarBrands , User , UserCar , User_Type , CarModels , User_Address , UserStatus , Request,Request_Allocation , Car_Joint
from Universal.models import Service_Type , Joint_Service_Mapping , Joint_Driver_Mapping , Driver_Allocation_Status , TimeSlot , Joint_Allocation_Status
# Create your views here.
@api_view(['GET' , 'POST'])
def cardetails(request, pk , format = None):
    #Get the details of Car for the user whose user id is sent as primary_key
    if request.method == 'GET':
        user_car_data  = UserCar.objects.filter(carownerid__userid = pk)
        returndata = []
        for row in user_car_data:
            tempDict = {}
            tempDict['name'] = row.carbrand.car_brand
            tempDict['model'] = row.carmodel.car_model
            tempDict['regno'] = row.registration_number
            returndata.append(tempDict)
        #return Response(returndata)
        return Response({'response':[{'error':False,'reason':'','success':True,'id':pk,'responsedata':returndata}]} , status= status.HTTP_201_CREATED)
    #Add a new car for this User with primary key provided in request
    if(request.method == 'POST'):
        requestdata = request.data
        existUser = User.objects.get(userid = pk)
        if existUser is None:
            print('User Not Added in system - Cant add car for a Ghost')
            return Response({'name':'NoUser'}, status.HTTP_400_BAD_REQUEST)
        newRegNumber = requestdata['registration_number']
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
            carsbrand = CarBrands.objects.get(car_brand = carbrand_requestdata)
            if carsbrand is None:
                print('Cars Brand is None')
                #print(carsbrand[0])
            #print('CarBrand' , carsbrand.car_brand)
            try :
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
        except:
            return Response({'response':[{'error':True,'reason':'FailedToAdd','success':False,'id':existUser.userid }]} , status = status.HTTP_201_CREATED)

        return Response({'response':[{'registration_number': newCarEntry.registration_number ,'name':existUser.first_name,'error':False,'reason':'CarAdded','success':True,'id':existUser.userid,'userstatus':existUser.user_status.user_status}]} , status = status.HTTP_201_CREATED)


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
        #validate if the same email or phone is present in the database
        existUser = User.objects.filter(email=email , joint_mobile=mobile ,access_token = token)
        print('existUser' , existUser)
        if existUser is None or len(existUser) == 0:
            print('existUser is None')

        elif existUser is not None:
            print('existUserID' , existUser[0].userid)
            return Response({'response':[{'error':False,'reason':'UserExists','success':True,'id':existUser[0].userid ,'userstatus':existUser[0].user_status.user_status}]} , status = status.HTTP_201_CREATED)
            #if i rtrn  HTTP_400_BAD_REQUEST i dont get any data returned
        try:
            # if no duplicate data entry then save the data
            usertype = User_Type.objects.filter(name='Customer')
            newuserstatus = UserStatus.objects.get(user_status = 'NewProfile')
            newUserEntry = User(userTypeId=usertype[0] , first_name = fname , last_name = lname, email = email , joint_mobile=mobile,access_token = token,is_active = True , status = 'Normal',user_status = newuserstatus)
            newUserEntry.save()
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
    requestdata = request.data
    request_service_id = requestdata['serviceid']
    available_services = Service_Type.objects.get(id = request_service_id)
    print('request service id is ' , request_service_id)
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
            rider = Driver_Allocation_Status.objects.filter(driver_user_id = each_drivermap.driver_user_id.userid , current_count__lte = 4, time_slot_id = timeslot.id)
            if len(rider) > 0:
                try:
                    slotAvailableDict = {timeslot.id:True}
                    #slotAvailableDict = {'timeslotid',timeslot.id}
                    response_time_slots.append(slotAvailableDict)
                    print('response slot en',len(response_time_slots))
                    if len(response_time_slots) ==  len(time_slots):
                        break
                except:
                    print('this slot id is already available' , timeslot.id)


        if len(response_time_slots) ==  len(time_slots):
            break
    print('return data length is ',len(response_time_slots))
    return Response({'response':[{'error':False,'reason':'Slots Available','success':True,'id':pk  ,'responsedata':response_time_slots}]} , status = status.HTTP_201_CREATED)


@api_view(['POST'])
def initreq(request , pk , format = None):
    print('Request Received')
    requestdata = request.data
    request_service_id = requestdata['serviceid']
    request_slot_id= requestdata['timeslot_id']
    request_car =requestdata['carno']
    print('Printing data received in Request ', request_service_id,    request_slot_id,request_car)

    time_slot = TimeSlot.objects.get(id = request_slot_id)
    #Again First find the drivers for the given time slot
    try :
        print('Finding Joints from Joint Service Mapping')
        joint_service_map = Joint_Service_Mapping.objects.filter(service_type_id__id = request_service_id , service_slot_count__gte =1)
    except :
        return Response({'error:','No such service exists'}, status.HTTP_400_BAD_REQUEST)

    print('Found %d Joints for',len(joint_service_map))
    print('Finding Drivers of Suitable Car Joints')

    for each_joint in joint_service_map:
        print(each_joint.car_joint_id.name , each_joint.service_type_id.name)
        joint_driver_map = Joint_Driver_Mapping.objects.filter(car_joint_id = each_joint.car_joint_id)
        print('number of drivers', len(joint_driver_map))
        for driverMapObject in joint_driver_map:
            print('driver name',driverMapObject.driver_user_id.first_name)
            rider = Driver_Allocation_Status.objects.get(driver_user_id = driverMapObject.driver_user_id.userid , current_count__lte = 4, time_slot_id = time_slot.id)
            print('driver name allocation',driverMapObject.driver_user_id.first_name)
            if rider is not None:
                #allocate this guy
                print('allocating this driver', driverMapObject.driver_user_id.first_name)
                user = User.objects.get(userid =pk)
                user_car = UserCar.objects.get(registration_number = request_car)
                newRequest = Request(user_id = user , time_slot_id = time_slot ,user_car_id = user_car)
                newRequest.save()
                print('new request id ' ,newRequest.id)


                joint = Car_Joint.objects.get(id = each_joint.car_joint_id.id)
                servicetype = Service_Type.objects.get(id = request_service_id)

                newRequestAllocation = Request_Allocation(request_id = newRequest, car_joint_id = joint , service_type_id= servicetype)
                newRequestAllocation.save()
                print('newRequest Allocation id' , newRequestAllocation.id)
                #increase joint allocation status(currently does not handler dates)
                current_allocation_count = 0
                try:
                    existJointAllocationStatus = Joint_Allocation_Status.objects.get(car_joint_id =  joint , service_type_id = servicetype)
                except:
                    existJointAllocationStatus = None

                if existJointAllocationStatus is not None:
                    current_allocation_count = existJointAllocationStatus.current_count
                    existJointAllocationStatus.current_count +=1
                    print('Count for this Joints Existing Allocation',existJointAllocationStatus.current_count)
                    existJointAllocationStatus.save()
                else:
                    print('Its a new Allocation for this joint ')
                    newJointAllocationStatus = Joint_Allocation_Status(car_joint_id = joint , service_type_id = servicetype , current_count =1)


                #increase the count of driver allocation status
                rider.current_count = rider.current_count +1

                return Response({'response':[{'error':False,'reason':'Booking Confirmed','success':True,'id':pk  ,'driver':driverMapObject.driver_user_id.first_name,
                'joint':each_joint.car_joint_id.name}]} , status = status.HTTP_201_CREATED)
    return Response({'response':[{'error':True,'reason':'No Joints','success':False,'id':pk }]} , status = status.HTTP_201_CREATED)
