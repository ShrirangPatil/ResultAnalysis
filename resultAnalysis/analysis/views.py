from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib import messages

# forms
from analysis.forms import homeForm
from analysis.forms import selectForm

# backend file
from analysis.result_analysis import analysis_fun

# Create your views here.

# creates a result.csv file
def handle_uploaded_file(f):
	try:
	    with open('analysis/static/media/result.csv', 'wb+') as writeFile:
	    	#writer = csv.writer( writeFile , delimiter=',' )
	    	for chunk in f.chunks():
		    	writeFile.write(chunk)
		    	#print(chunk,end="\n")
	except Exception as e:
		pass

# Home
def home(request):
	if request.method == "POST":
		form = homeForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			#return HttpResponse("hi")
			return redirect('/analysis/select')
		else:
			messages.error(request, 'Failed to validate')
	else:
		return render(request, "home.html", {"homeForm":homeForm})

# Select
def select(request):
	if request.method == "POST":
		form = selectForm(request.POST)
		if form.is_valid():
			picked = form.cleaned_data.get('subjectCode')
			#print(picked)
			analysis_fun(picked)
			messages.success(request, 'File Analysis Successful')
		else:
			messages.error(request, 'Failed to validate')
			return redirect('/analysis/home')
		return redirect('/analysis/result')
	else:
		try:
			fileContent = []
			with open('analysis/static/media/result.csv', 'r') as readFile:
				reader = csv.reader(readFile)
				for row in reader:
					fileContent.append(row)
		except Exception as e:
			pass
		return render(request, "select.html", {"selectForm":selectForm, "fileContent":fileContent})

# Result
def result(request):
	if request.method == "POST":
		try:
			with open('analysis/static/media/analysis.csv', 'rb') as fh:
				response = HttpResponse(fh.read(), content_type="text/csv")
				response['Content-Disposition'] = 'inline; filename=' + 'analysis.csv'
				return response
			#return redirect('/analysis/home')
		except Exception as e:
			messages.error(request, 'Failed to Download')
			return redirect('/analysis/home')
	else:
		try:
			fileContent = []
			with open('analysis/static/media/analysis.csv', 'r') as readFile:
				reader = csv.reader(readFile)
				for row in reader:
					fileContent.append(row)
		except Exception as e:
			pass
		return render(request, "result.html", {"fileContent":fileContent})