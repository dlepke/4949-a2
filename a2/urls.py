from django.urls import path
from .views import homePageView, resultsView, quizPost

urlpatterns = [
	path('', homePageView, name='home'),
	path('quizPost/', quizPost, name='quizPost'),
	path('results/', resultsView, name='results')
]
