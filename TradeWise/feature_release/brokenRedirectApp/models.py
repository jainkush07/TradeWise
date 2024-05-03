from django.db import models

#
class redirectBucket(models.Model):
	source = models.CharField(max_length=1000, unique=True)
	destination = models.URLField(max_length=1000)

	class Meta:
		verbose_name_plural = 'Redirect Urls Buckets'

	def __str__(self):
		return f'Source: {self.source}, Destination: {self.destination}' or '--Name not provided--'

#
class redirectCount(models.Model):
	redirectInst = models.ForeignKey('redirectBucket', on_delete=models.SET_NULL, null=True, blank=True, related_name='redirectInstRC')
	clientIP = models.TextField(null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Redirect Links Count with IP'

	def __str__(self):
		return f'Source: {self.redirectInst.source}, IP: {self.clientIP}' or '--Name not provided--'