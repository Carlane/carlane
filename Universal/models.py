from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.core.validators import RegexValidator
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

class User_Type(models.Model):
	id =  models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	is_active = models.BooleanField(default = True)
	def __str__(self):
		return self.name


class UserStatus(models.Model):
	id= models.AutoField(primary_key = True)
	user_status = models.CharField(max_length = 50, blank = False , null = False)

class User(models.Model):
	userid = models.AutoField(primary_key =  True)
	userTypeId = models.ForeignKey(User_Type , blank = False , null = True)
	first_name =  models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	email = models.EmailField(max_length = 50)
	#insert the Regex in other file as constants . Figure out how to do it
	#http://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
	#http://stackoverflow.com/questions/22378736/regex-for-mobile-number-validation
	#phone_regex  = RegexValidator(regex=r'^\+?1?\d{9,15}$' , message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed ")
	mobile_regex = RegexValidator(regex=r'^(\+?\d{1,4}[\s-])?(?!0+\s+,?$)\d{10}\s*,?$', message=" Enter a Valid Mobile Number")
	joint_mobile = models.CharField(validators=[mobile_regex] , blank = True , max_length = 20)
	access_token = models.CharField(blank = False , max_length = 400,default = "")
	firebase_token = models.CharField(blank = False , max_length = 400,default = "")
	is_active = models.BooleanField(default = True)
	status = models.CharField(blank = True , max_length = 50)
	user_status = models.ForeignKey(UserStatus,blank = False, null = True)
	def __str__(self):
		return self.first_name



class User_Address(models.Model):
	id = models.AutoField(primary_key = True)
	user_id = models.ForeignKey(User)
	line1 = models.CharField(max_length = 100 , blank = False , default = "")
	line2 = models.CharField(max_length = 100 , blank = False , default = "")
	#alok - i think this data should be mapped to some tables of cities , state and countries
	city = models.CharField(max_length = 100 , blank = False , default = "")
	state = models.CharField(max_length = 100 , blank = False , default = "")
	country = models.CharField(max_length = 100 , blank = False , default = "")
	latt = models.DecimalField(max_digits = 100 , decimal_places = 50 , blank = True , null = True)
	longg = models.DecimalField(max_digits = 100 , decimal_places = 50 , blank = True , null = True)

class Car_Type(models.Model):
	id = models.AutoField(primary_key = True)
	cartype = models.CharField(max_length = 30 , blank = False , null = True)

class CarBrands(models.Model):
    carbrandid = models.AutoField(primary_key = True)
    car_brand = models.CharField(max_length = 50 , blank = True, null = True)

    def __str__(self):
    	return self.car_brand



class CarModels(models.Model):
	modelid = models.AutoField(primary_key = True)
	carmodel_brand = models.ForeignKey(CarBrands)
	car_model = models.CharField(max_length = 50 , blank = True, null = True)
	typeofcar = models.ForeignKey(Car_Type)

	def __str__(self):
		return self.car_model



class UserCar(models.Model):
	carownerid = models.ForeignKey(User)
	carbrand = models.ForeignKey(CarBrands , blank = True , null = True)
	carmodel = models.ForeignKey(CarModels , blank = True , null = True)
	registration_number = models.CharField(max_length = 20 , blank = True , null = True)

	def __str__(self):
		return self.registration_number

class WashType(models.Model):
	carwashtype = models.CharField(max_length = 100)

class NewWashRequest(models.Model):
	request_number = models.AutoField(primary_key = True)
	requesterid = models.ForeignKey(User)
	#location
	carmodel_id = models.ForeignKey(CarModels)
	washtype = models.ForeignKey(WashType)

#
class Contact_Type(models.Model):
	id =  models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	is_active = models.BooleanField(default = True)
	def __str__(self):
		return self.name




class Geography(models.Model):
	id =  models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	is_active = models.BooleanField(default = True)
	def __str__(self):
		return self.name




class TimeSlot(models.Model):
	id =  models.AutoField(primary_key = True)
	geo_id = models.ForeignKey(Geography)
	display_name = models.CharField(max_length = 30)
	time_from = models.TimeField(auto_now = False , auto_now_add = False , blank = False , null = True)
	time_to = models.TimeField(auto_now = False , auto_now_add = False , blank = False , null = True)
	is_active = models.BooleanField(default = True)
	def __str__(self):
		return "Name "+self.display_name


class Service_Type(models.Model):
	id =  models.AutoField(primary_key = True)
	geo_id = models.ForeignKey(Geography)
	name = models.CharField(max_length = 50)
	is_active = models.BooleanField(default = True)
	def __str__(self):
		return "Name "+self.name+" Geo "+self.geo_id.name+" Cost "+ "\n"

class ServiceVersion(models.Model):
	id = models.AutoField(primary_key = True)
	geo_id = models.ForeignKey(Geography)
	verion = models.DecimalField(max_digits = 10 , decimal_places = 5)


class Service_Attributes(models.Model):
	id = models.AutoField(primary_key = True)
	typeofservice = models.ForeignKey(Service_Type)
	description = models.CharField(max_length = 1000 , null = True , blank = True)
	motto = models.CharField(max_length = 200 , null = True, blank = True)
	attribute_1 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_2 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_3 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_4 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_5 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_6 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_7 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_8 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_9 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_10 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_11 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_12 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_13 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_14 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_15 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_16 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_17 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_18 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_19 = models.CharField(max_length = 200 , null =True , blank = True)
	attribute_20 = models.CharField(max_length = 200 , null =True , blank = True)





class Cost(models.Model):
	id = models.AutoField(primary_key = True)
	typeofservice = models.ForeignKey(Service_Type)
	typeofcar = models.ForeignKey(Car_Type)
	costtouser = models.DecimalField(max_digits = 10 , decimal_places = 2)
	def __str__(self):
		return str(self.costtouser)

class Car_Joint(models.Model):
	id =  models.AutoField(primary_key = True)
	geo_id = models.ForeignKey(Geography)
	reg_no = models.CharField(max_length = 50 , blank = False)
	shop_no = models.CharField(max_length = 50 , blank = False)
	name = models.CharField(max_length = 50 , blank = False)
	opening_time = models.TimeField(auto_now = False , auto_now_add = False , blank = False , null = True)
	closing_time = models.TimeField(auto_now = False , auto_now_add = False , blank = False , null = True)
	closed_day = models.CharField(max_length = 15)
	latt = models.DecimalField(max_digits = 100 , decimal_places = 50 , blank = False , null = True)
	longg = models.DecimalField(max_digits = 100 , decimal_places = 50 , blank = False , null = True)
	is_active = models.BooleanField(default = True)
	def __str__(self):
		return self.name


class Car_Joint_Contact(models.Model):
	id =  models.AutoField(primary_key = True)
	car_joint_id = models.ForeignKey(Car_Joint)
	contact_type = models.ForeignKey(Contact_Type)
	contact_no = models.CharField(max_length = 100)
	is_active = models.BooleanField(default = True)



class Joint_Service_Mapping(models.Model):
	id =  models.AutoField(primary_key = True)
	car_joint_id = models.ForeignKey(Car_Joint)
	service_type_id = models.ForeignKey(Service_Type)
	service_slot_count = models.IntegerField()
	cost = models.IntegerField()
	is_active = models.BooleanField(default = True)


class Joint_Driver_Mapping(models.Model):
	id =  models.AutoField(primary_key = True)
	car_joint_id = models.ForeignKey(Car_Joint)
	driver_user_id = models.ForeignKey(User)
	s_active = models.BooleanField(default = True)

class Request_Status(models.Model):
	id = models.AutoField(primary_key = True)
	current_status = models.CharField(max_length = 50)


#we need date in request or request allocation , we need service id in this , this object should contain all info that is sent by the user
#Need to discuss with wardu if we should save Service Type in the Request object instead of request allocation
class Request(models.Model):
	id =  models.AutoField(primary_key = True)
	user_id = models.ForeignKey(User)
	time_slot_id = models.ForeignKey(TimeSlot)
	user_car_id = models.ForeignKey(UserCar)
	date = models.DateField(auto_now = False , auto_now_add = False , blank = False , null = True)
	latt = models.DecimalField(max_digits = 30 , decimal_places = 20)
	longg = models.DecimalField(max_digits = 30 , decimal_places = 20)
	current_status = models.ForeignKey(Request_Status , default = None , null = True)

class Request_Feedback(models.Model):
	id =  models.AutoField(primary_key = True)
	washrating = models.DecimalField(max_digits= 3,decimal_places =1)
	driverrating = models.DecimalField(max_digits= 3,decimal_places =1)
	overallrating = models.DecimalField(max_digits= 3,decimal_places =1)
	feedback_text = models.CharField(max_length=550)
	request_id = models.ForeignKey(Request , default = None , null = True)

#this should contain the information that is allocated by the system for a given request
class Request_Allocation(models.Model):
	id =  models.AutoField(primary_key = True)
	request_id = models.ForeignKey(Request)
	car_joint_id = models.ForeignKey(Car_Joint)
	service_type_id = models.ForeignKey(Service_Type)
	driver_id = models.ForeignKey(User , default = None , null = True)#added new

class Joint_Allocation_Status(models.Model):
	id =  models.AutoField(primary_key = True)
	date = models.DateField(auto_now = False , auto_now_add = False , blank = False , null = True)
	car_joint_id = models.ForeignKey(Car_Joint)
	service_type_id = models.ForeignKey(Service_Type)
	current_count = models.IntegerField()
	def __str__(self):
		return self.id


class Driver_Allocation_Status(models.Model):
	id =  models.AutoField(primary_key = True)
	date = models.DateField(auto_now = False , auto_now_add = False , blank = False , null = True)
	driver_user_id = models.ForeignKey(User)
	time_slot_id = models.ForeignKey(TimeSlot)
	current_count = models.IntegerField()
