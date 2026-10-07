"""
Utilities for loading, parsing, indexing, and searching HGNC gene data
from a TSV file as oppose to using a typical Django database.

The module:
1. Defines the structure of gene records and indexes.
2. Cleans and validates individual TSV rows ( split_values() & parse_rows() ).
3. Loads records into indexes for efficient searching.
4. Finds records by approved gene symbol or HGNC ID.

Provides information that AppVeiws will need to display from search request. 
"""
import csv
import logging

from typing import TypedDict
from pathlib import Path

logger = logging.getLogger(__name__)


#Step 1. Describe expected gene dictionaries for each parsed gene dictionary.
class GeneRecord(TypedDict):
    """Describes the fields and value types of a parsed gene record."""
    symbol: str
    hgnc_id: str
    name: str 
    previous_symbols: list[str]
    previous_names: list[str]
    alias_symbols: list[str]
    alias_names: list[str]
    mane_select: list[str]
    mane_plus_clinical: list[str]

#Describes each expected search dictionaries (i.e. symbol or hgnc_id) generated post search.
class GeneIndex(TypedDict):
    """Indexes gene records by approved symbol and HGNC ID."""
    by_symbol: dict[str, GeneRecord]
    by_hgnc_id: dict[str, GeneRecord]


#Step 2. List necessary headings: creates variable for which columns are required.
REQUIRED_COLUMNS = {
    "symbol",
    "hgnc_id",
    "name",
    "prev_symbol",
    "prev_name",
    "alias_symbol",
    "alias_name",
    "mane_select",
}


#Step 3. Create function which will clean and split multi-value fields and returns a list.
def split_values(value: str | None) -> list[str]:
    """
    Converts pipe-separated fields into a list of cleaned strings.

    Args:
        value: A pipe-separated string, an empty string or None.

    Returns:
        Non-empty values with surrounding whitespace are removed.
        Returns an empty list when the input is either empty or None.
    """

    #empty values returns empty items.
    if not value:
        return []

    #Splits lines on pipes (e.g. in 'prev_symbol') and trims surrounding whitespaces.
    return [
        item.strip()
        for item in value.split("|")
        if item.strip()
    ]


#Step 4. Creates a function that parses rows so each row provides a dictionary (GeneRecord format) of required display columns.
def parse_row(row: dict[str, str | None]) -> GeneRecord:
    """
    Converts a raw TSV row into a cleaned GeneRecord dictionary.

    Scalar fields are stripped of surrounding whitespace, and
    pipe-separated fields are converted into lists.

    Args:
        row: A dictionary containing TSV column headings and cell values.

    Raises:
        ValueError: If the gene symbol or HGNC ID is missing or empty.

    Returns:
        A cleaned GeneRecord representing one gene.
    """

    #.get() avoids KeyError, and 'or ""' converts a missing, None, or empty value into an empty string.
    symbol = (row.get("symbol") or "").strip()
    hgnc_id = (row.get("hgnc_id") or "").strip()
    name = (row.get("name") or "").strip()

    #Checks if symbol present for the gene search.
    if not symbol:
        raise ValueError("Record does not contain a gene symbol.")

    #Checks if hgnc_id present for the gene search.
    if not hgnc_id:
        raise ValueError("Record does not contain an HGNC_ID.")

    #Creates a smaller dictionary in GeneRecord format per gene.
    return {
        "symbol": symbol,
        "hgnc_id": hgnc_id,
        "name": name,
        "previous_symbols": split_values(row.get("prev_symbol")),
        "previous_names": split_values(row.get("prev_name")),
        "alias_symbols": split_values(row.get("alias_symbol")),
        "alias_names": split_values(row.get("alias_name")),
        "mane_select": split_values(row.get("mane_select")),
        #Returns mane_plus_clinical despite not being a heading ()
        "mane_plus_clinical": split_values(row.get("mane_plus_clinical")),
    }


#Step 5. Main function which utilises split_value() and parse_row() to read dataset, clean, parse and return appropriate GeneRecord.
def read_file(filename: Path) -> GeneIndex:
    """
    Loads an HGNC TSV file and indexes its gene records.

    Invalid rows are skipped with a warning. All searches are converted into uppercase to 
    support case-insensitve searches.

    Args:
        filename: Path to the HGNC TSV file.

    Raises:
        OSError: If the file cannot be opened or read.
        ValueError: If required columns are missing or no valid records
            are loaded.

    Returns:
        Gene records indexed by approved symbol and HGNC ID.
    """
    
    #Creates two dictionaries (keys = by_symbol and by_hgnc) to be filled with GeneRecord fields.
    by_symbol: dict[str, GeneRecord] = {}
    by_hgnc_id: dict[str, GeneRecord] = {}

    try:
        with filename.open("r", encoding="utf-8-sig", newline="") as file:
            #Creates .tsv reader. where csv.DictReader treats first row as headers and '\t' indicates tab dilimited.
            reader = csv.DictReader(file, delimiter="\t")

            #Removes whitespaces from headings.
            reader.fieldnames = [
            field.strip()
            for field in (reader.fieldnames or [])
]
            #checks all required columns exist and raises explainatory error if missing and stops function.
            columns = set(reader.fieldnames or [])
            missing_columns = REQUIRED_COLUMNS - columns

            if missing_columns:
                missing = ", ".join(sorted(missing_columns))
                raise ValueError(
                    f"HGNC file missing required columns: {missing}"
                )

            # Read and process every gene row in the TSV file.
            for line_number, row in enumerate(reader, start=2):
                try:
                    record = parse_row(row) #creates GeneRecords per gene row columns present.

                    #Creates case-insensitve search keys for each record.
                    symbol_key = record["symbol"].upper()
                    hgnc_key = record["hgnc_id"].upper()

                    #Stores the created records in list, searchable by either symbol or HGNC ID key.
                    by_symbol[symbol_key] = record
                    by_hgnc_id[hgnc_key] = record

                except ValueError as exc:
                    logger.warning(
                        "Skipping line %d: %s",
                        line_number,
                        exc,
                    )

    except OSError: 
        logger.exception(
            "Unable to read HGNC data file.", 
            "Ensure data file is downloaded and in InfoGene/Data/"
            )
        raise

    if not by_symbol:
        raise ValueError("No valid HGNC records were loaded.")

    logger.info(
        "Successfully loaded %d HGNC records",
        len(by_symbol)
    )

    #Combines the two completed search dictionaries into a GeneIndex and returns it.
    return {
        "by_symbol": by_symbol,
        "by_hgnc_id": by_hgnc_id,
    }


#Step 7. Find the searched gene.
def find_gene(search: str, genes: GeneIndex) -> GeneRecord | None:
    """
    Finds a gene by the approved symbol or HGNC ID.

    Searching is case-insensitive. Numeric queries are treated as an
    HGNC ID, so "1100" is converted to "HGNC:1100".

    Args:
        search: An approved gene symbol, HGNC ID, or numeric HGNC ID.
        genes: Gene records indexed by symbol and HGNC ID.

    Returns:
        The matching GeneRecord, or None if no match exists.
    """

    query = search.strip().upper()

    if not query:
        return None

    if query.isdigit():
        query = f"HGNC:{query}"

    if query.startswith("HGNC:"):
        result = genes["by_hgnc_id"].get(query)
    else:
        result = genes["by_symbol"].get(query)
    

    if result is None:
        logger.info("No gene record for %s query found", query)
    else: 
        logger.info("Gene record for %s query found", query)

    return result 
