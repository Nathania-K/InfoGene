import pytest

from django.urls import reverse
from InfoGene.InfoGeneApp import AppViews

# ------------------------------------------------- #
# Tests for Homepage                                #
# ------------------------------------------------- #

def test_successful_home_reponse(client):
    """
    Tests if hojmepage returns HTTP status: 200
    """

    response = client.get(reverse("home"))

    actual_status = response.status_code
    expected_status = 200

    assert actual_status == expected_status


def test_home_index_template(client):
    """
    Tests to see if homepage uses the index template
    """

    response = client.get(reverse("home"))

    template_names = [
        template.name
        for template in response.templates
    ]

    assert "InfoGene/index.html" in template_names

# ------------------------------------------------- #
# Tests for Searches                                #
# ------------------------------------------------- #

def test_successful_search_reponse(client):
    """
    Tests if searchpage returns HTTP status: 200
    """

    response = client.get(reverse("search"))

    actual_status = response.status_code
    expected_status = 200

    assert actual_status == expected_status


def test_search_results_template(client):
    """
    Tests to see if searchpage uses the results template during results.
    """

    response = client.post(
        reverse("search"),
        {"gene": "BRCA1"},
        )

    template_names = [
        template.name
        for template in response.templates
    ]

    assert "InfoGene/results.html" in template_names


def test_search_get_returns_homepage(client):
    """
    Tests if a GET request returns to the homepage.
    """

    response = client.get(reverse("search"))

    actual_status = response.status_code
    expected_status = 200

    template_names = [
        template.name
        for template in response.templates
    ]

    assert actual_status == expected_status
    assert "InfoGene/index.html" in template_names


def test_search_rejects_empty(client):
    """
    Tests an empty gene search returns an error message.
    """

    response = client.post(
        reverse("search"),
        {"gene": ""},
    )

    actual_message = response.context["error_message"]
    expected_message = "Please enter a valid HGNC symbol/ID."

    assert actual_message == expected_message


def test_search_gene_result(client):
    """
    Tests a matching gene is displayed on the results page.
    """

    response = client.post(
        reverse("search"),
        {"gene": "BRCA1"},
    )

    actual_gene = response.context["gene"]["symbol"]
    expected_gene = "BRCA1"

    assert actual_gene == expected_gene
