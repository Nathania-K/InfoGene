from pathlib import Path

import pytest

from InfoGene.InfoGeneApp.AppModels import (
    split_values,
    parse_row,
    read_file,
    find_gene,
    )

# ------------------------------------------------- #
# Test Data                                         #
# ------------------------------------------------- #

TEST_FIELD = "RNF53 | BRCA1"

TEST_REQUIRED_COLUMNS = {
    "symbol",
    "hgnc_id",
    "name",
    "prev_symbol",
    "prev_name",
    "alias_symbol",
    "alias_name",
    "mane_select",
}

TEST_ROW = {
        "symbol": "BRCA1",
        "hgnc_id": "HGNC:1100",
        "name": "BRCA1 DNA repair associated",
        "previous_symbols": "RNF53 | BRCA1",
        "previous_names": "",
        "alias_symbols": "BRCAI",
        "alias_names": None,
        "mane_select": "ENST00000357654.9",
        "mane_plus_clinical": "",
}

TEST_RECORD = {
        "symbol": "BRCA1",
        "hgnc_id": "HGNC:1100",
        "name": "BRCA1 DNA repair associated",
        "previous_symbols": "RNF53 | BRCA1",
        "previous_names": "",
        "alias_symbols": "BRCAI",
        "alias_names": None,
        "mane_select": "ENST00000357654.9",
        "mane_plus_clinical": "",
}

# ------------------------------------------------- #
# Tests for split_values()                          #
# ------------------------------------------------- #
def test_split_values_empty_string():
    assert split_values("") == []


def test_split_values_removes_pipe():

    actual_pipe_split = split_values(TEST_FIELD)
    expected_pipe_split = ["RNF53", "BRCA1"]

    assert actual_pipe_split == expected_pipe_split


# ------------------------------------------------- #
# Tests for parse_rows()                            #
# ------------------------------------------------- # 

# ------------------------------------------------- #
# Tests for read_files()                            #
# ------------------------------------------------- #

# ------------------------------------------------- #
# Tests for find_genes()                            #
# ------------------------------------------------- #
def test_find_gene_returns_None():
    assert find_gene("") == None


def test_find_gene_isdigit():
    """
    Test to see if correct gene record return upon numerical hgnc entry 
    """

    genes = {
        "by_symbol": {
            "BRCA1": TEST_RECORD
        },

        "by_hgnc_id": {
            "HGNC:1100": TEST_RECORD
        },
    }

    TEST_DIGIT_QUERY = 1100

    actual_digit_query_result = find_gene(TEST_DIGIT_QUERY, genes)
    expected_digit_query_result = TEST_RECORD

    assert expected_digit_query_result == actual_digit_query_result