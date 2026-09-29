"""
Views implement application logic, handle requests and determine appropriate HTML response.

As dataset will not be in database format but in tsv upon application startup, no ORM needed.


"""

import logging

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from . import AppModels as models

#Sets up logger for AppViews.py
logger = logging.getLogger(__name__)

logger.info("Initialising Django view layer")

TEMPLATE_NAME = "InfoGene/index.html"


#Initialises "database" (i.e. HGNC.tsv file for lookup) in Data.
DATA_FILE = settings.DATA_FILE

logger.info("loading data from %s", settings.DATA_FILE)


#Opens the dataset in DATA, reads, selects and creates the gene dictionaries, indexed by symobol/ID.
try: 
    DATA = models.read_file(DATA_FILE)

    #length describes number of genes loaded.
    logger.info(
        "successfully loaded %d records.",
        len(DATA["by_symbol"]),
    )

#Prevents loading if dataset fails to load.
except Exception:
    logger.exception("Failed to load application data.")
    raise


#Defines and render application homepage.
def home(request: HttpRequest) -> HttpResponse:
    """
    Renders the application homepage

    Args:
        request (HttpRequest): Incoming HTTP request for homepage.

    Returns:
        HttpResponse: Rendered homepage.
    """
    logger.debug("Rendering homepage.")

    return render(request, TEMPLATE_NAME)

#Defines and renders application searchpage.
def search(request: HttpRequest) -> HttpResponse:
    """
    Processes gene search requests 

    Args:
        request (HttpRequest): Incoming HTTP request contiainign submitted form data

    Returns:
        HttpReponse:  Rendered HTML response containing either search results or an
        explainatory error message.
    """

    #Ensures only POST requests allows searches to be performed.
    if request.method != "POST":
        logger.debug("Ignoring non-POST request.")

        return render(request, TEMPLATE_NAME)

    #prepares parameter input by cleaning whitespaces to allow for search request of gene.
    search_term = request.POST.get("gene", "").strip()

    #Handles empty output and returns to template so users can re-search.
    if not search_term:
        logger.warning("No gene search term entered. Please enter a valid HGNC symbol/ID.")

        return render(
            request,
            TEMPLATE_NAME,
            {
                "error_message": (
                    "Please enter a valid HGNC symbol/ID."
                ),
            },
        )

    logger.debug("Searching for gene: %s", search_term)

    #passes cleaned search term into find_gene() function to search within dataset.
    gene_selection = models.find_gene(search_term, DATA)

    #If not found in dataset, error message raised.
    if gene_selection is None:
        logger.info("Gene was not found: %s", search_term)

        return render(
            request,
            TEMPLATE_NAME,
            {
                "error_message": (
                    f"No gene was found for '{search_term}'."
                ),
                "search_term": search_term,
            },
        )

    logger.info("Gene found: %s", search_term)

    #returns template with searched gene and appropraite information in GeneRecord format.
    return render(
        request,
        TEMPLATE_NAME,
        {
            "gene": gene_selection,
            "search_term": search_term,
        },
    )
