from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import pickle
import pandas as pd


# Create your views here.


def homePageView(request):
	return render(request, 'home.html', {
		'name': 'Genevieve',
		'numbers': [1, 2, 3, 4, 5]
	})


def resultsView(request):
	with open('/Users/deannalepke/Desktop/COMP4949/4949-a2/model.pkl', 'rb') as f:
		model = pickle.load(f)
		
	data = request.session.get('data')
	
	cocoa_percent = data['cocoa_percent']
	num_ingredients = data['num_ingredients']
	ingredients = data['ingredients']
	
	print(ingredients)
	
	df = pd.DataFrame(columns=['cocoa_percent', 'num_ingredients', 'B', 'S', 'S*', 'Sa', 'V', 'L'])
	
	df = df.append({
		'cocoa_percent': int(cocoa_percent),
		'num_ingredients': int(num_ingredients),
		'B': 1 if 'Beans' in ingredients else 0,
		'S': 1 if 'Sugar' in ingredients else 0,
		'S*': 1 if 'Non-sugar sweetener' in ingredients else 0,
		'Sa': 1 if 'Salt' in ingredients else 0,
		'V': 1 if 'Vanilla' in ingredients else 0,
		'L': 1 if 'Lecithin' in ingredients else 0,
		'const': 1
	}, ignore_index=True)
	
	print(df)
	
	prediction = model.predict(df)
	print(prediction)
	
	return render(request, 'results.html', {
		'cocoa_percent': cocoa_percent,
		'num_ingredients': num_ingredients,
		'ingredients': ingredients,
		'prediction': prediction[0]
	})


def quizView(request):
	return render(request, 'quiz.html', {
		'ingredients': ['Beans', 'Sugar', 'Non-sugar sweetener', 'Salt', 'Vanilla', 'Lecithin']
	})


def quizPost(request):
	try:
		cocoa_percent = request.POST['cocoa_percent']
		num_ingredients = request.POST['num_ingredients']
		ingredients = request.POST.getlist('ingredient')
	except:
		return render(request, 'quiz.html', {
			'errorMessage': 'Choice missing, please try again',
			'numbers': [1, 2, 3, 4, 5]
		})
	else:
		request.session['data'] = {
			'cocoa_percent': cocoa_percent,
			'num_ingredients': num_ingredients,
			'ingredients': ingredients
		}
		return HttpResponseRedirect(reverse('results'))
