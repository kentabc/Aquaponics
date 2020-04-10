from django.db import models
#from __future__ import unicode_literals
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
#from django.urls import reverse
from ckeditor.fields import RichTextField


class plant_type(models.Model):
	plant_name = models.CharField(max_length = 100)
	comment = models.TextField(null=True, blank=True)
	def __str__(self):
		return self.plant_name
	# def get_absolute_url(self):
	# 	return reverse("planttypefrm", args=[str(self.id)])

class fish_type(models.Model):
	fish_name = models.CharField(max_length = 100)
	comment = models.TextField(null=True, blank=True)
	def __str__(self):
		return self.fish_name
	# def get_absolute_url(self):
	# 	return reverse("fishtypefrm", args=[str(self.id)])

class plant(models.Model):
	crop = models.CharField(max_length=15)
	plant_type = models.ForeignKey(plant_type, on_delete=models.CASCADE)
	amount = models.IntegerField()
	plant_date = models.DateField('Date Planted')
	plant_time = models.TimeField('Time Planted')
	comment = models.TextField(null=True, blank=True)
	def __str__(self):
		return self.crop

	def get_absolute_url(self):
		return reverse("forms_detail", kwargs={"id": self.id})

class fish(models.Model):
	crop = models.CharField(max_length=15)
	fish_type = models.ForeignKey(fish_type, on_delete=models.CASCADE)
	batch = models.IntegerField()
	spawn_amount = models.IntegerField()
	spawn_date = models.DateField()
	comment = models.TextField(null=True, blank=True)
	def __str__(self):
		return self.crop


class harvest(models.Model):
	plant = models.ForeignKey(plant, on_delete=models.CASCADE, null=True, blank=True)
	fish = models.ForeignKey(fish, on_delete=models.CASCADE, null=True, blank=True)
	amount_reaped = models.IntegerField()
	reap_date = models.DateField(null=True, blank=True)
	harvest_complete = models.DateField(null=True, blank=True)
	comment = models.TextField(null=True, blank=True)
	def __str__(self):
		return str(self.amount_reaped)+(" Reaped")


class tasks(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=200)
	def __str__(self):
		return self.name

class schedule(models.Model):
	task = models.ForeignKey(tasks, on_delete=models.CASCADE)
	date = models.DateField(auto_now_add=True)
	task_date = models.DateField(editable=False)
	duration = models.IntegerField()
	completed = models.BooleanField(default=False)
	comment = models.TextField(max_length=200, null=True, blank=True)
	def save(self):
		dur = timedelta(days=self.duration)
		if not self.id:
			self.task_date = datetime.now() + dur
			super(schedule,self).save()
		if self.completed == True:
			self.date = datetime.now()
			self.task_date = datetime.now() + dur
			self.completed = False
			super(schedule,self).save()
		if self.completed == False:
			super(schedule,self).save()

	def get_absolute_url(self):
		return reverse("schedulefrm", kwargs={"id": self.id})


class testing(models.Model):
	test_date = models.DateField(auto_now_add=True)
	ph = models.DecimalField(max_digits=5, decimal_places=1,  null=True, blank=True, default=0.0)
	amonia = models.DecimalField(max_digits=5, decimal_places=2,  null=True, blank=True, default=0.0)
	nitrite = models.DecimalField(max_digits=5, decimal_places=2,  null=True, blank=True, default=0.0)
	nitrate = models.DecimalField(max_digits=5, decimal_places=1,  null=True, blank=True, default=0.0)
	

class notes(models.Model):
	date = models.DateField(auto_now_add=True)
	title = models.CharField(max_length=100)
	# notes = models.TextField()
	notes = RichTextField()
	def __str__(self):
		return self.title
