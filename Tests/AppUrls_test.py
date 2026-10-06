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


def test_home_url_view():
    """
    Tests to see if "home" uses the home view. 
    """

    actual_home_view = resolve("/").func
    expected_home_view = AppViews.home

    assert actual_home_view == expected_home_view


def test_search_url_path():
    """
    Tests to see if home url generates correctly.
    reverse() function takes a url name and returns it's path.
    """

    actual_url = reverse("search")
    expected_url = "/search/"

    assert actual_url == expected_url


def test_search_url_view():
    """
    Tests to see if "search" uses the search view. 
    """

    actual_search_view = resolve("/search/").func
    expected_search_view = AppViews.search

    assert actual_search_view == expected_search_view

