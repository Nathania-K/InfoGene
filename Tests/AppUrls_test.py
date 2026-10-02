import pytest

from django.urls import resolve, reverse
from InfoGene.InfoGeneApp import AppViews

def test_home_url_path():
    """
    Tests to see if home url generates correctly.
    reverse() function takes a url name and returns it's path.
    """

    actual_url = reverse("home")
    expected_url = "/"

    assert actual_url == expected_url

def test_home_url_veiw():
    """
    Tests to see if "home" uses the home view. 
    """

    actual_home_veiw = resolve("/").func
    expected_home_veiw = AppViews.home

    assert actual_home_veiw == expected_home_veiw


def test_search_url_path():
    """
    Tests to see if home url generates correctly.
    reverse() function takes a url name and returns it's path.
    """

    actual_url = reverse("search")
    expected_url = "/search/"

    assert actual_url == expected_url

def test_search_url_veiw():
    """
    Tests to see if "search" uses the search view. 
    """

    actual_search_veiw = resolve("/search/").func
    expected_search_veiw = AppsViews.search

    assert actual_search_veiw == expected_search_veiw

