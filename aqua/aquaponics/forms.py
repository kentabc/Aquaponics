from django import forms
from . models import plant, fish, harvest, plant_type, fish_type, schedule, tasks, testing, notes
import datetime
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
	widgets = {'plant_time': forms.TimeInput(attrs={'class':'timepicker'})}
	widgets = {'plant_date': forms.DateInput(attrs={'class':'datepicker'})}
	class Meta:
		model = plant
		fields = [
			'crop',
			'plant_type',
			'amount',
			'plant_date',
			'plant_time',
			'comment',

		]

class FishForm(forms.ModelForm):
	widgets = {'spawn_date': forms.DateInput(attrs={'class':'datepicker'})}
	class Meta:
		model = fish
		fields = [
			"crop",
			"fish_type",
			"batch",
			"spawn_amount",
			"spawn_date",
			"comment",

		]

class HarvestForm(forms.ModelForm):
	widgets = {'reap_date': forms.DateInput(attrs={'class':'datepicker'})}
	class Meta:
		model = harvest
		fields = [
			"plant",
			"fish",
			"amount_reaped",
			"reap_date",
			"harvest_complete",
			"comment",

		]

class PlanttypeForm(forms.ModelForm):
	class Meta:
		model = plant_type
		fields = [
			"plant_name",
			"comment",
			
		]

class FishtypeForm(forms.ModelForm):
	class Meta:
		model = fish_type
		fields = [
			"fish_name",
			"comment",
			
		]

class schedform(forms.ModelForm):
	class Meta:
		model = schedule
		fields = [
			"task",
			"duration",
			"completed",
			"comment",
		]

class schedform1(forms.ModelForm):
	#widgets = {'date': forms.DateInput(attrs={'class':'datepicker'})}
	class Meta:
		model = schedule
		fields = [
			"task",
			"duration",
			"comment",
		]

class taskform(forms.ModelForm):
	class Meta:
		model = tasks
		fields = [
			"name",
			"description",
		]

class watertest(forms.ModelForm):
	class Meta:
		model = testing
		fields = [
			"ph",
			"amonia",
			"nitrite",
			"nitrate",
		]

class formnotes(forms.ModelForm):
	notes = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = notes
		fields = [
			"title",
			"notes",
		]

class cropnotes(forms.ModelForm):
	class Meta:
		model = plant
		fields = [
			"crop",
			"plant_type",
			"amount",
			"plant_date",
			"plant_time",
			"comment",

		]

class fishnotes(forms.ModelForm):
	class Meta:
		model = fish
		fields = [
			"crop",
			"fish_type",
			"batch",
			"spawn_amount",
			"spawn_date",
			"comment",

		]
