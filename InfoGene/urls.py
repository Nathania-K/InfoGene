#Provides root URL config and ultimately manages which application to handle a request

from django.urls import include, path

urlpatterns = [
    path("", include("InfoGene.InfoGeneApp.AppUrls"))
]