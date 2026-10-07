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

TEST_ROW = {
    "symbol": "BRCA1",
    "hgnc_id": "HGNC:1100",
    "name": "BRCA1 DNA repair associated",
    "prev_symbol": "RNF53 | BRCA1",
    "prev_name": "",
    "alias_symbol": "BRCAI",
    "alias_name": None,
    "mane_select": "ENST00000357654.9",
    "mane_plus_clinical": "",
}

TEST_RECORD = {
    "symbol": "BRCA1",
    "hgnc_id": "HGNC:1100",
    "name": "BRCA1 DNA repair associated",
    "previous_symbols": ["RNF53", "BRCA1"],
    "previous_names": [],
    "alias_symbols": ["BRCAI"],
    "alias_names": [],
    "mane_select": ["ENST00000357654.9"],
    "mane_plus_clinical": [],
}

TEST_WHITESPACE = " BRCA1 "

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

TEST_GENES = {
    "by_symbol": {
        "BRCA1": TEST_RECORD
    },

    "by_hgnc_id": {
        "HGNC:1100": TEST_RECORD
    },
}

TEST_DIGIT_QUERY = "1100"


# ------------------------------------------------- #
# Tests for split_values()                          #
# ------------------------------------------------- #
def test_split_values_empty_string():
    """
    Tests if empty string returns an empty list.
    """

    actual_value = split_values("")
    expected_value = []

    assert actual_value == expected_value


def test_split_values_none():
    """
    Test if None produces an empty list.
    """

    actual_value = split_values(None)
    expected_value = []

    assert actual_value == expected_value


def test_split_values_removes_pipe():

    actual_pipe_split = split_values(TEST_FIELD)
    expected_pipe_split = ["RNF53", "BRCA1"]

    assert actual_pipe_split == expected_pipe_split


# ------------------------------------------------- #
# Tests for parse_rows()                            #
# ------------------------------------------------- # 
def test_parse_row_returns_GeneRecord():
    """
    Tests if a TSV row gets converted into a GeneRecord
    """

    #Check logic of this..
    actual_record = parse_row(TEST_ROW)
    expected_record = TEST_RECORD

    assert actual_record == expected_record


def test_parse_row_removes_whitespace():
    """
    Tests to see if whitespace is removed from gene field.
    """

    row = TEST_ROW.copy()
    row["symbol"] = " BRCA1 "

    record = parse_row(row)

    actual_symbol = record["symbol"]
    expected_symbol = "BRCA1"

    assert actual_symbol == expected_symbol


def test_parse_row_empty_symbol_error():
    """
    Tests if errors raised upon empty HGNC symbol/ID.
    """

    row = TEST_ROW.copy()
    row["symbol"] = ""

    with pytest.raises(
        ValueError,
    ):
        parse_row(row)

def test_parse_row_empty_id_error():
    """
    Tests if errors raised upon empty HGNC symbol/ID.
    """

    row = TEST_ROW.copy()
    row["hgnc_id"] = ""

    with pytest.raises(
        ValueError,
    ):
        parse_row(row)


# ------------------------------------------------- #
# Tests for read_files()                            #
# ------------------------------------------------- #
def test_read_file_creates_GeneRecord(tmp_path):
    """
    Tests if TSV file is correctly indexed by HGNC symbol/ID.
    """

    TEST_FILE = tmp_path / "genes.tsv"

    TEST_FILE.write_text(
        "symbol\thgnc_id\tname\tprev_symbol\tprev_name\t"
        "alias_symbol\talias_name\tmane_select\tmane_plus_clinical\n"
        "BRCA1\tHGNC:1100\tBRCA1 DNA repair associated\t"
        "RNF53\t\tBRCAI\t\tENST00000357654.9\t\n",
        encoding="utf-8"
    )

    gene_index = read_file(TEST_FILE)

    actual_symbol = gene_index["by_symbol"]["BRCA1"]["symbol"]
    expected_symbol = "BRCA1"

    actual_hgnc_id = gene_index["by_hgnc_id"]["HGNC:1100"]["hgnc_id"]
    expected_hgnc_id = "HGNC:1100"

    assert actual_symbol == expected_symbol
    assert actual_hgnc_id == expected_hgnc_id


def test_parse_row_rejects_invalid_records(tmp_path):
    """
    Tests if .tsv with missing column is rejected
    """

    TEST_FILE = tmp_path / "genes.tsv"

    TEST_FILE.write_text(
        "symbol\thgnc_id\tname\tprev_symbol\tprev_name\t"
        "alias_symbol\talias_name\tmane_select\tmane_plus_clinical\n"
        "\tHGNC:1100\tInvalid record\t\t\t\t\t\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError
    ):
        read_file(TEST_FILE)


def test_parse_row_missing_columns(tmp_path):
    """
    Tests if .tsv with missing column is rejected
    """

    TEST_FILE = tmp_path / "genes.tsv"

    TEST_FILE.write_text(
        "symbol\thgnc_id\n"
        "BRCA1\tHGNC:1100\n",
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError
    ):
        read_file(TEST_FILE)


# ------------------------------------------------- #
# Tests for find_genes()                            #
# ------------------------------------------------- #
def test_find_gene_by_symbol():
    """
    Tests to see if gene found using HGNC symbol.
    """

    actual_gene = find_gene("BRCA1", TEST_GENES)
    expected_gene = TEST_RECORD

    assert actual_gene == expected_gene

def test_find_gene_by_hgnc_id():
    """
    Tests if gene found using HGNC symbol.
    """

    actual_gene = find_gene("HGNC:1100", TEST_GENES)
    expected_gene = TEST_RECORD

    assert actual_gene == expected_gene

def test_find_gene_isdigit():
    """
    Tests if correct gene record return upon numerical hgnc entry.
    """

    actual_digit_query_result = find_gene(TEST_DIGIT_QUERY, TEST_GENES)
    expected_digit_query_result = TEST_RECORD

    assert expected_digit_query_result == actual_digit_query_result

def test_find_gene_unknown_gene():
    """
    Tests if None is returned upon unknown gene search.
    """

    actual_gene = find_gene("UNKNOWN", TEST_GENES)
    expected_gene = None

    assert actual_gene == expected_gene

def test_find_gene_empty_search():
    """
    Tests to see if empty search returns None.
    """

    actual_gene = find_gene("", TEST_GENES)
    expected_gene = None
    
    assert actual_gene == expected_gene

def test_read_file_rejects_missing_file(tmp_path):
    """
    Tests if error raised when .tsv file not present.
    """

    missing_file = tmp_path / "missing.tsv"

    with pytest.raises(
        OSError
    ):
        read_file(missing_file)