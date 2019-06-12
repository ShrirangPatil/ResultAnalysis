from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib import messages
import time
import os

# forms
from analysis.forms import homeForm
from analysis.forms import selectForm

# backend file
from analysis.result_analysis import analysis_fun

# Create your views here.

# creates a result.csv file
def handle_uploaded_file(f, fname):
	try:
	    with open('analysis/static/media/'+fname+'.csv', 'wb+') as writeFile:
	    	#writer = csv.writer( writeFile , delimiter=',' )
	    	for chunk in f.chunks():
	    		writeFile.write(chunk)
	    	print('File Created')
	except Exception as e:
		pass

# Home
def home(request):
	if request.method == "POST":
		form = homeForm(request.POST, request.FILES)
		if form.is_valid():
			request.session['fileName'] = str(time.time())
			print(request.session['fileName'])
			handle_uploaded_file(request.FILES['file'], request.session['fileName'])
			#return HttpResponse("hi")
			return redirect('/analysis/select')
		else:
			messages.error(request, 'Failed to validate')
	else:
		return render(request, "home.html", {"homeForm":homeForm})

# Select
def getSubjectCode(fname):
	print(fname)
	try:
		with open('analysis/static/media/'+fname+'.csv', 'r') as csvfile:
			results = csv.reader(csvfile, delimiter=',')
			subjectCode = next(results, None)
		retSubCode = []
		for s in subjectCode:
			retSubCode.append((s, s))
		return tuple(retSubCode)
	except Exception as e:
		print('File not found')
	return ''

def select(request):
	if request.method == "POST":
		form = selectForm(request.POST)
		#form = selectForm()
		form.fields['subjectCode'].choices = getSubjectCode(request.session['fileName'])
		if form.is_valid():
			picked = form.cleaned_data.get('subjectCode')
			#print(picked)
			analysis_fun(request.session['fileName'], picked)
			messages.success(request, 'File Analysis Successful')
		else:
			messages.error(request, 'Failed to validate')
			return redirect('/analysis/home')
		return redirect('/analysis/result')
	else:
		print(getSubjectCode(request.session['fileName']))
		form = selectForm()
		form.fields['subjectCode'].choices = getSubjectCode(request.session['fileName'])
		try:
			fileContent = []
			with open('analysis/static/media/'+request.session['fileName']+'.csv', 'r') as readFile:
				reader = csv.reader(readFile)
				for row in reader:
					fileContent.append(row)
		except Exception as e:
			pass
		return render(request, "select.html", {"selectForm":form, "fileContent":fileContent})

# Result
def result(request):
	if request.method == "POST":
		try:
			with open('analysis/static/media/analysis'+request.session['fileName']+'.csv', 'rb') as fh:
				response = HttpResponse(fh.read(), content_type="text/csv")
				response['Content-Disposition'] = 'inline; filename=' + 'analysis.csv'

			os.remove('analysis/static/media/'+request.session['fileName']+'.csv')
			os.remove('analysis/static/media/analysis'+request.session['fileName']+'.csv')
			return response
			#return redirect('/analysis/home')
		except Exception as e:
			messages.error(request, 'Failed to Download')
			return redirect('/analysis/home')
	else:
		try:
			fileContent = []
			with open('analysis/static/media/analysis'+request.session['fileName']+'.csv', 'r') as readFile:
				reader = csv.reader(readFile)
				for row in reader:
					fileContent.append(row)
		except Exception as e:
			pass
		return render(request, "result.html", {"fileContent":fileContent})
