from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from stockApp.models import CURRENT_YEAR
from datetime import datetime
from datetime import date
from django.core.exceptions import ValidationError

#
def validate_file_size_10MB(value):
	filesize= value.size
	if filesize > 10485760:
		raise ValidationError("The maximum file size that can be uploaded is 10MB")
	else:
		return value

#
def validate_file_size_40MB(value):
	filesize= value.size
	if filesize > 41943040:
		raise ValidationError("The maximum file size that can be uploaded is 40MB")
	else:
		return value


todayDateTime = datetime.today()

YEAR_CHOICES = [(r,r) for r in range(date.today().year+2, 1800, -1)]

BLOOD_GROUP_CHOICES = (
	('O+','O+'),
	('O-','O-'),
	('A+','A+'),
	('A-','A-'),
	('B+','B+'),
	('B-','B-'),
	('AB+','AB+'),
	('AB-','AB-'),
)

STATUS_CHOICES = (
	('draft', 'Draft'),
	('published', 'Published'),
)

Gender_Choices = (
	('male', 'Male'),
	('female', 'Female'),
)

Marital_Status = (
	('single', 'Single'),
	('married', 'Married'),
	('seperated','Seperated'),
	('divorced','Divorced'),
	('widowed','Widowed'),
)

Qualification_Choices = (
	('high School', 'High School'),
	('diploma', 'Diploma'),
	('graduate', 'Graduate'),
	('post graduate', 'Post Graduate'),
	('others', 'Others'),
	)

Account_Status = (
	('activate', 'Activate'),
	('disable', 'Disable'),
)


Leadership_Info = (
	('yes', 'yes'),
	('no', 'no'),
	)

Admin_Info	= (
	('yes', 'yes'),
	('no', 'no'),
	)

MONTH_CHOICES = (
	('January','January'),
	('February','February'),
	('March','March'),
	('April','April'),
	('May','May'),
	('June','June'),
	('July','July'),
	('August','August'),
	('September','September'),
	('October','October'),
	('November','November'),
	('December','December'),
	)

#
def currentMonthAbbr():
	currentMonth = todayDateTime.month - 1
	monthAbbr = MONTH_CHOICES[currentMonth][0]
	return monthAbbr

#
class employeePersonalDetails(models.Model): 
	profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerEPD', null=True, blank=True)
	firstName = models.CharField(max_length=1000, null=True, blank=True)
	lastName = models.CharField(max_length=1000, null=True, blank=True)
	profileImage = models.ImageField(upload_to ='employee/employee-profile/', null=True, blank=True)
	personalEmail = models.EmailField(max_length = 254, null=True, blank=True)
	dateOfBirth = models.DateField(null=True,blank=True)
	mobileNumber = models.BigIntegerField(null=True, blank=True)
	gender = models.CharField(max_length=50,choices=Gender_Choices, null=True, blank=True)
	bloodGroup = models.CharField(max_length=50,choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
	maritalStatus = models.CharField(max_length=50,choices=Marital_Status, null=True, blank=True)
	educationDetails = models.CharField(max_length=1000, null=True, blank=True)
	highestQualification = models.CharField(max_length=50,choices=Qualification_Choices, null=True, blank=True)
	uploadDegree = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	panNumber = models.CharField(max_length=1000, null=True, blank=True)
	uploadPan = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	aadharNumber = models.CharField(max_length=1000, null=True, blank=True)
	uploadAadhar = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorEPD', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.firstName or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Personal Details'


#
class country(models.Model):
	name = models.CharField(max_length=1000, null=True, blank=True)
	countryCode = models.CharField(max_length=1000, null=True, blank=True)
	flag = models.ImageField(upload_to ='employee/employee-profile/', null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorCO', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Country'
#
class state(models.Model):
	name = models.CharField(max_length=1000, null=True, blank=True)
	stateCountry = models.ForeignKey(country, on_delete=models.SET_NULL, related_name='stateCountryS', null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorS', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'State'

#
class city(models.Model):
	name = models.CharField(max_length=1000, null=True, blank=True)
	cityState = models.ForeignKey(state, on_delete=models.SET_NULL, related_name='cityStateC', null=True, blank=True)
	cityCountry = models.ForeignKey(country, on_delete=models.SET_NULL, related_name='cityCountryC', null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorC', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'City'


#
class employeePermanentAddress(models.Model): 
	profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerEPA', null=True, blank=True)
	address = models.TextField(null=True, blank=True)
	city =  models.ForeignKey(city, on_delete=models.SET_NULL, null=True, blank=True, related_name='cityEPA')
	pinCode = models.BigIntegerField(null=True,blank=True)
	state =  models.ForeignKey(state, on_delete=models.SET_NULL, null=True, blank=True, related_name='stateEPA')
	country =  models.ForeignKey(country, on_delete=models.SET_NULL, null=True, blank=True, related_name='countryEPA')
	emergencyContactPersonName =  models.CharField(max_length=1000, null=True, blank=True)
	emergencyContactPersonNumber = models.CharField(max_length=1000, null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorEPA', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return self.emergencyContactPersonName or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Permanent Address Details'


#
class employeeLocalAddress(models.Model):
	profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerELA', null=True, blank=True)
	address = models.TextField(null=True, blank=True)
	city =  models.ForeignKey(city, on_delete=models.SET_NULL, null=True, blank=True, related_name='cityELA')
	pinCode = models.BigIntegerField(null=True,blank=True)
	state =  models.ForeignKey(state, on_delete=models.SET_NULL, null=True, blank=True, related_name='stateELA')
	country =  models.ForeignKey(country, on_delete=models.SET_NULL, null=True, blank=True, related_name='countryELA')
	localGuardianLandlord =  models.CharField(max_length=1000, null=True, blank=True)
	localGuardianLandlordDetails =  models.CharField(max_length=1000, null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorELA', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.localGuardianLandlord or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Local Address Details'

#
class financialYear(models.Model):
	name = models.CharField(max_length=1000, null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorEFY', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Financial Year'

#
class employeeCompanyDetails(models.Model):
	profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerECD', null=True, blank=True)
	companyEmail = models.EmailField(max_length=254)
	# firstPassword = models.CharField(max_length=245)
	pfNumber = models.CharField(max_length=1000, null=True, blank=True)
	joiningDate = models.DateField(null=True,blank=True)
	dateOfRelieving = models.DateField(null=True,blank=True)
	insuranceNumber = models.PositiveIntegerField(null=True,blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorECD', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.companyEmail or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Company Details'

	# def save(self):
	# 	if self.companyEmail:
	# 		if not User.objects.filter(email=companyEmail).exists():
	# 			cd = User.objects.create(email=companyEmail, password=companyEmail)
	# 			cd.save()
	# 	super(employeeCompanyDetails, self).save()

#
class companyDetailsFinancialObjs(models.Model):
	profileOwnerFK = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profileOwnerCDFO', null=True, blank=True)
	financialYear = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR, null=True, blank=True)
	annualLetter = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_40MB])
	annualVariable = models.BigIntegerField(null=True,blank=True)
	annualFixed = models.BigIntegerField(null=True,blank=True)
	joiningBonus = models.BigIntegerField(null=True,blank=True)
	annualCTC = models.BigIntegerField(null=True,blank=True)
	retentionBonus = models.BigIntegerField(null=True,blank=True)
	perksAndBenefits = models.BigIntegerField(null=True,blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorCDFO', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return 'For Profile Owner: %s , Financial Year: %s' % (self.profileOwnerFK, self.financialYear) or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Company Detail Financial Components'

	def save(self):
		if self.annualVariable:
			annualVar = self.annualVariable
		else:
			annualVar = 0
		if self.annualFixed:
			annualFix = self.annualFixed
		else:
			annualFix = 0
		if self.joiningBonus:
			joinBonus = self.joiningBonus
		else:
			joinBonus = 0
		if self.retentionBonus:
			retntionBonus = self.retentionBonus
		else:
			retntionBonus = 0
		if self.perksAndBenefits:
			perksndBenefits = self.perksAndBenefits
		else:
			perksndBenefits = 0
		
		self.annualCTC = annualVar + annualFix + joinBonus + retntionBonus + perksndBenefits
		super(companyDetailsFinancialObjs, self).save()

#
class employeeTypes(models.Model):
	name = models.CharField(max_length=250)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Type Details'

#
class employeeDepartment(models.Model):
	name = models.CharField(max_length=250)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Department Details'

#
class employeeRole(models.Model):
	name = models.CharField(max_length=250)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Role Details'

#
class employeeGrade(models.Model):
	name = models.CharField(max_length=250)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Grade Details'


WORKING_MODE = (
	('WFO', 'WFO'),
	('WFA', 'WFA'),
	('Hybrid', 'Hybrid')
)

class employeeDepartmentDetails(models.Model):
	profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerEDD', null=True, blank=True)
	designation = models.CharField(max_length=1000, null=True, blank=True)
	employeeeType = models.ForeignKey(employeeTypes,related_name='employeeeTypeEDD',null=True, blank=True,on_delete=models.SET_NULL)
	department = models.ForeignKey(employeeDepartment,related_name='employeeeTypeEDD',null=True, blank=True,on_delete=models.SET_NULL)
	role = models.ForeignKey(employeeRole,related_name='employeeeTypeEDD',null=True, blank=True,on_delete=models.SET_NULL)
	grade = models.ForeignKey(employeeGrade,related_name='employeeeTypeEDD',null=True, blank=True,on_delete=models.SET_NULL)
	account = models.CharField(max_length=10, choices=Account_Status, null=True, blank=True)
	mode_of_working = models.CharField(max_length=100, choices=WORKING_MODE, null=True, blank=True)
	leadership = models.CharField(max_length=10, choices=Leadership_Info, default='no', null=True, blank=True)
	admin = models.CharField(max_length=10, choices=Admin_Info, null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorEDD', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.designation or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Departmental Details'

	def save(self, *args, **kwargs):
		if self.account == 'disable' and self.profileOwner:
			user = User.objects.get(pk=self.profileOwner.pk)
			user.is_active = False
			user.save()
		elif self.account == 'activate' and self.profileOwner:
			user = User.objects.get(pk=self.profileOwner.pk)
			user.is_active = True
			user.save()
		super(employeeDepartmentDetails, self).save(*args, **kwargs)


#
class employeeAccountType(models.Model):
	name = models.CharField(max_length=250)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return self.name or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Account Type'

# class employeeBankDetails(models.Model):
# 	profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerEBD', null=True, blank=True)
# 	bankName = models.CharField(max_length=1000, null=True, blank=True)
# 	accountHolder = models.CharField(max_length=1000, null=True, blank=True)
# 	accountNumber = models.BigIntegerField(null=True,blank=True)
# 	accountType = models.ForeignKey(employeeAccountType,related_name='accountTypeEBD',null=True, blank=True,on_delete=models.SET_NULL)
# 	ifsc_Code = models.CharField(max_length=1000, null=True, blank=True)
# 	cancelledCheque = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf'])])
# 	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorEBD', null=True, blank=True)
# 	publish = models.DateTimeField(default=timezone.now)
# 	created = models.DateTimeField(auto_now_add=True)
# 	updated = models.DateTimeField(auto_now=True)
# 	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

# 	def __str__(self):
# 		return self.bankName or '--Name not provided--'

# 	class Meta:
# 		verbose_name_plural = 'Employee Bank Details'


#
class employeeBankDetailsObjs(models.Model):
	profileOwnerFK = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profileOwnerEBDO', null=True, blank=True)
	bankName = models.CharField(max_length=1000, null=True, blank=True)
	accountHolder = models.CharField(max_length=1000, null=True, blank=True)
	accountNumber = models.CharField(max_length=1000, null=True,blank=True)
	accountType = models.ForeignKey(employeeAccountType,related_name='accountTypeEBDO',null=True, blank=True,on_delete=models.SET_NULL)
	ifsc_Code = models.CharField(max_length=1000, null=True, blank=True)
	cancelledCheque = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	setAsDefault = models.BooleanField(default=False)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorEBDO', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return 'For Profile Owner: %s , Bank Name: %s' % (self.profileOwnerFK, self.bankName) or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Bank Detail Financial Components'


class uploadDocuments(models.Model):
	profileOwner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileOwnerUD', null=True, blank=True)
	profilePhoto = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	offerLetter = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	experienceLetter = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	recommendationLetter = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	assetDocument = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])

	appraisalLetter = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	probationConfirmation = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	relievingLetter = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	misconductLetter = models.FileField(upload_to ='employee/documents/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorUD', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return str(self.profileOwner) or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Upload Documents Details'

#
class employeeSalarySlips(models.Model):	
	profileOwnerFK = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profileOwnerESS', null=True, blank=True)
	year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=CURRENT_YEAR)
	month = models.CharField(max_length=254 ,choices=MONTH_CHOICES, default=currentMonthAbbr())
	salarySlip = models.FileField(upload_to ='employee/salarySlip/',null=True, blank=True, validators=[FileExtensionValidator(['pdf']),validate_file_size_10MB])
	dateForStatus = models.DateField(default=date.today(), null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='authorESS', null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	def __str__(self):
		return 'For Employee Username: %s , Year: %s , Month: %s' % (self.profileOwnerFK, self.year, self.month) or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Employee Salary Slips'