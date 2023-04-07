from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import pickle
import pandas as pd


# Create your views here.


def homePageView(request):
	return render(request, 'quiz.html', {
		'cps': ['Typical angina', 'Atypical angina', 'Non-anginal pain', 'Asymptomatic'],
		'ecgs': ['Normal', 'ST-T wave abnormality', 'Probable or definite left ventricular hypertrophy'],
		'thalls': ['Fixed defect', 'Normal blood flow', 'Reversible defect'],
		'slps': ['Downsloping', 'Flat', 'Upsloping']
	})


def resultsView(request):
	with open('/Users/deannalepke/Desktop/COMP4949/4949-a2/model.pkl', 'rb') as f:
		model = pickle.load(f)
		
	data = request.session.get('data')
	
	print(data)
	
	age = data['age']
	sex = data['sex']
	fbs = data['fbs']
	chol = data['chol']
	cp = data['cp']
	trtbps = data['trtbps']
	restecg = data['restecg']
	thall = data['thall']
	slp = data['slp']
	
	cps = ['Typical angina', 'Atypical angina', 'Non-anginal pain', 'Asymptomatic'],
	ecgs = ['Normal', 'ST-T wave abnormality', 'Probable or definite left ventricular hypertrophy'],
	thalls = ['Fixed defect', 'Normal blood flow', 'Reversible defect'],
	slps = ['Downsloping', 'Flat', 'Upsloping']

	df = pd.DataFrame(columns=[
		'age', 'sex', 'trtbps', 'chol', 'fbs', 'thall_fixed', "thall_normal", "thall_reversible", 'cp_asymptomatic',
		'cp_atypical_angina', 'cp_non-anginal_pain',
		'cp_typical_angina', 'restecg_hypertrophy', 'restecg_normal', 'restecg_stt_abnormal',
		'slp_down', 'slp_flat', 'slp_up'
	])

	df = df.append({
		'age': age,
		'sex': 0 if sex == 'M' else 1,
		'trtbps': trtbps,
		'chol': chol,
		'fbs': fbs,
		'thall_fixed': 1 if thall == 'Fixed defect' else 0,
		'thall_normal': 1 if thall == 'Normal blood flow' else 0,
		'thall_reversible': 1 if thall == 'Reversible defect' else 0,
		'cp_asymptomatic': 1 if cp == 'Asymptomatic' else 0,
		'cp_atypical_angina': 1 if cp == 'Atypical angina' else 0,
		'cp_non-anginal_pain': 1 if cp == 'Non-anginal pain' else 0,
		'cp_typical_angina': 1 if cp == 'Typical angina' else 0,
		'restecg_hypertrophy': 1 if restecg == 'Probable or definite left ventricular hypertrophy' else 0,
		'restecg_normal': 1 if restecg == 'Normal' else 0,
		'restecg_stt_abnormal': 1 if restecg == 'ST-T wave abnormality' else 0,
		'slp_down': 1 if slp == 'Downsloping' else 0,
		'slp_flat': 1 if slp == 'Flat' else 0,
		'slp_up': 1 if slp == 'Upsloping' else 0
	}, ignore_index=True)
	
	print(df)

	prediction = model.predict(df)
	print(prediction)
	
	return render(request, 'results.html', {
		'age': age,
		'sex': sex,
		'fbs': fbs,
		'chol': chol,
		'cp': cp,
		'trtbps': trtbps,
		'restecg': restecg,
		'thal': thall,
		'slp': slp,
		'prediction': 'Heart disease likely' if prediction[0] == 0 else "No heart disease"
	})


def quizPost(request):
	try:
		age = request.POST['age']
		sex = request.POST['sex']
		fbs = request.POST['fbs']
		chol = request.POST['chol']
		cp = request.POST['cp']
		trtbps = request.POST['trtbps']
		restecg = request.POST['ecg']
		thall = request.POST['thall']
		slp = request.POST['slp']
	except:
		return render(request, 'home.html', {
			'errorMessage': 'Please fill out all fields.',
			'cps': ['Typical angina', 'Atypical angina', 'Non-anginal pain', 'Asymptomatic'],
			'ecgs': ['Normal', 'ST-T wave abnormality', 'Probable or definite left ventricular hypertrophy'],
			'thalls': ['Fixed defect', 'Normal blood flow', 'Reversible defect'],
			'slps': ['Downsloping', 'Flat', 'Upsloping']
		})
	else:
		request.session['data'] = {
			'age': age,
			'sex': sex,
			'fbs': fbs,
			'chol': chol,
			'cp': cp,
			'trtbps': trtbps,
			'restecg': restecg,
			'thall': thall,
			'slp': slp
		}
		return HttpResponseRedirect(reverse('results'))
