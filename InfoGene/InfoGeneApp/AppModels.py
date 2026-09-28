"""
#Data access and parsing utilities for .tsv file - "service layer" rather than database:
1. reads input
2. Parses individual records
3. Searching loaded dataset
#Info that the app veiws will need to function. 
#database layer will need to configure .tsv file into database. 
"""
import csv
import logging

#Mapping provides a dictionary-like inpout whilst TypedDict descirbes expected key/vlaues of dictionaries.
from typing import Mapping, TypedDict
from pathlib import Path

logger = getLogger(__name__)


#Step 1. Create class to format generic gene dictionaries required for both HDNC_ID and HGNC_Index searches.
class GeneRecord(TypedDict):
    symbol: str
    hgnc_id: str
    name: str 
    previous_symbols: list[str]
    previous_names: list[str]
    aliases: list[str]
    mane_select: list[str]

class GeneIndex(TypedDict):
    by_symbol: dict[str, GeneRecord]
    by_hgnc_id: dic[str, GeneRecord]


#Step 2. State the required columns so app can check if they exist within record.
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


#Step 3. Clean and split multi-value fields and returns a list.
def split_values(value: str | None) -> list[str]:
    """
    _summary_

    Args:
        value (str | None): _description_

    Returns:
        list[str]: _description_
    """

    #empty values returns empty items.
    if not value:
        return []

    #multi-value fields split by '|' (e.g. in 'prev_symbol') cleaned and trailing whitespace removed.
    return [
        item.strip()
        for item in value.split("|")
        if item.strip()
    ]


#Step 4. Parse the rows so that each .tsv row provides a dictionary (GeneRecord format) of required columns.
def parse_row(row: Mapping[str, str | None],) -> GeneRecord:
    """
    _summary_

    Args:
        row (Mapping[str, str  |  None]): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        GeneRecord: _description_
    """

    #uses .get to retrieve required fields and "" prevents KeyError if key missing as converted to None.
    symbol = (row.get("symbol") or "").strip()
    hgnc_id = (row.get("hgnc_id") or "").strip()
    name = (row.get("name") or "").strip()

    #Checks if symbol present for the gene search.
    if not symbol:
        raise ValueError("Record does not contain a gene symbol.")

    #Checks if hgnc_id present for the gene search.
    if not hgnc_id:
        raise ValueError("Record does not contain an HGNC_ID.")

    #Creates a smaller dictionary used by app to search through per gene.
    return {
        "symbol": symbol,
        "hgnc_id": hgnc_id,
        "name": name,
        "previous_symbols": split_values(row.get("prev_symbol")),
        "previous_names": split_values(row.get("prev_name")),
        "alias_symbols": split_values(row.get("alias_symbol")),
        "alias_names": split_values(row.get("alias_name")),
        "mane_select": split_values(row.get("mane_select")),
        #Check if this is needed (v)
        "mane_plus_clinical": split_values(row.get("mane_plus_clinical")),
    }


#Step 5. Read the .tsv file.
def read_file(filename: Path) -> GeneIndex:
    
    #Opens a list for the searches so that required fields can be filled after reading .tsv in GeneRecord format.
    by_symbol = dict[str, GeneRecord] = {}
    by_hgnc_id = dict[str, GeneRecord] = {}

#Step 6. Opens .tsv file and uses csv.DictReader to 
    try:
        with filename.open("r", encoding="utf-8-sig", newline="") as file:
            #Creates .tsv reader. csv.DictReader treats first row as headers and '/t' indicates tab dilimited.
            reader = csv.DictReader(file, delimiter="\t")

            #Finds required fieldnames and raises explainatory error if missing.
            columns = set(reader.fieldnames or [])
            missing_columns = REQUIRED_COLUMNS - columns

            if missing_columns:
                missing = ", ".join(sorted(missing_columns))
                raise ValueError(
                    f"HGNC file missing required columns: {missing}"
                )

            #Processing of each gene ('row') and normalised to uppercase. Ignores headers (row=1).
            for line_number, row in enumerate(reader, start=2):
                try:
                    record = parse_row(row)

                    symbol_key = record["symbol"].upper()
                    hgnc_key = record["hgnc_id"].upper()

                    by_symbol[symbol_key] = record
                    by_hgnc_id[hgnc_key] = record

                except ValueError as exc:
                    logger.warning(
                        "Skipping line %d: %s",
                        line_number,
                        exc,
                    )

    except OSError: 
        logger.Exception("Unable to read HGNC data file.")
        raise

    if not by_symbol:
        raise ValueError("No valid HGNC records were loaded.")

    logger.info(
        "Successfully loaded %d HGNC records",
        len(by_symbol)
    )

    return {
        "by_symbol": by_symbol,
        "by_hgnc_id": by_hgnc_id,
    }


#Step 7. Find the searched gene.
def find_gene(search: str, genes: GeneIndex) -> GeneRecord | None:

    query = search.strip().upper()

    if not query:
        return None

    if query.isdigit():
        query = f"HGNC: {query}"

    if query.startswith("HGNC:"):
        result = genes["by_hgnc_id"].get(query)
    else:
        result = genes["by_symbol"].get(query)
    

    if result is None:
        logger.info("No gene record for %s query found", query)
    else: 
        logger.info("Gene record for %s query found", query)

    return result 
