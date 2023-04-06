from django.urls import path
from .views import homePageView, resultsView, quizView, quizPost

urlpatterns = [
	path('', homePageView, name='home'),
	path('quiz/', quizView, name='quiz'),
	path('quizPost/', quizPost, name='quizPost'),
	path('results/', resultsView, name='results')
]
