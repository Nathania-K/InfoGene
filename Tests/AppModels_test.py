from pathlib import Path

import pytest

from InfoGene.InfoGeneApp.AppModels import (
    split_values,
    parse_row,
    read_file,
    find_gene,
    )

TEST_ROW = {

}

TEST_RECORD = {
        "symbol": "BRCA1"
        "hgnc_id": "HGNC:1100",
        "name": "BRCA1 DNA repair associated",
        "previous_symbols": "RNF53 | BRCA1",
        "previous_names": "",
        "alias_symbols": "BRCAI",
        "alias_names": None,
        "mane_select": "ENST00000357654.9",
        "mane_plus_clinical": "",
}

def test_split_values_empty_string():
    assert split_values("") == None
    