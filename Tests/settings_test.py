from pathlib import Path

from django.conf import settings

def test_root_url_config():
    """
    Tests to see if the correct root url configuration settings are used.
    """

    actual_url_config = settings.ROOT_URLCONF
    expected_urls_config = "InfoGene.urls"

    assert actual_url_config == expected_urls_config


def test_installation():
    """
    Tests to see if application is registered with Django
    """

    assert "InfoGene.InfoGeneApp" in settings.INSTALLED_APPS

def test_static_url():
    """
    Tests to see if static files use the correct url prefix.
    """

    actual_static_url = settings.STATIC_URL
    expected_static_url = "/static/"

    assert actual_static_url == expected_static_url


def test_data_file_name():
    """
    Tests to see if the correct datafile is used for function.
    """

    actual_filename = Path(settings.DATA_FILE).name
    expected_filename = "hgnc_complete_set.txt"
    
    assert actual_filename == expected_filename


