from django import forms
import csv

class homeForm(forms.Form):
	file = forms.FileField(label = "CSV File")

class selectForm(forms.Form):
	#print(retSubCode)
	#retSubCode = getSubjectCode()
	#print('retSubCode=',retSubCode)
	subjectCode = forms.MultipleChoiceField(
		label = "Subject Codes",
        widget=forms.CheckboxSelectMultiple,
        choices='',)
	def __init__(self, *args, **kwargs):
		super(selectForm, self).__init__(*args, **kwargs)
		self.fields['subjectCode'] = forms.MultipleChoiceField(
			label = "Subject Codes",
			widget=forms.CheckboxSelectMultiple,
			choices='',)
	# for i in subjectCode:
	# 	check_+str(subjectCode) = fr

