"""
#Urls that will be needed by to determine the  which display view to handle request.
#Checks URL patterns in order (first matching used).
"""
from django import path
from InfoGene.InfoGeneApp import AppViews

urlpatterns = [

    #Homepage: 
    #Url: /
    # Displays the search form. 
    path("", views.home, name="home"),

    #Gene search endpoint: 
    #Url: /search/
    #Processes POST requests from the home form. 
    path("search/", views.search, name="search"),

]