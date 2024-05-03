from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

#
STATUS_CHOICES = (
	('draft', 'Draft'),
	('published', 'Published'),
)

#
class uploaded_files(models.Model):
	file = models.FileField(upload_to='sharebook-excels/')
	temp_code = models.CharField(max_length=12, unique=True, null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	def __str__(self):
		return f'Uploaded on: {self.created}' or '--Name not provided--'

	class Meta:
		verbose_name_plural = 'Sharebook Uploaded Files'

	def save(self, *args, **kwargs):
		import random
		import string
		N = 12
		token = ''.join(random.choices(string.ascii_letters, k=N))
		if uploaded_files.objects.filter(temp_code=token).exists():
			token = ''.join(random.choices(string.ascii_letters, k=N))
		self.temp_code = token
		super(uploaded_files, self).save(*args, **kwargs)
