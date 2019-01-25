from django import forms
import csv

class homeForm(forms.Form):
	file = forms.FileField(label = "CSV File")


def getSubjectCode():
	with open('analysis/static/media/result.csv', 'r') as csvfile:
		results = csv.reader(csvfile, delimiter=',')
		subjectCode = next(results, None)
	retSubCode = []
	for s in subjectCode:
		retSubCode.append((s, s))

	return tuple(retSubCode)

class selectForm(forms.Form):
	#print(retSubCode)
	retSubCode = getSubjectCode()
	subjectCode = forms.MultipleChoiceField(
		label = "Subject Codes",
        widget=forms.CheckboxSelectMultiple,
        choices=retSubCode,)
	def __init__(self, *args, **kwargs):
		super(selectForm, self).__init__(*args, **kwargs)
		retSubCode = getSubjectCode()
		self.fields['subjectCode'] = forms.MultipleChoiceField(
			label = "Subject Codes",
			widget=forms.CheckboxSelectMultiple,
			choices=retSubCode,)
	# for i in subjectCode:
	# 	check_+str(subjectCode) = fr

