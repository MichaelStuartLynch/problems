from cs50 import SQL

import check50
import sqlparse


@check50.check()
def exists():
    """SQL files exist"""
    for i in range(5):
        check50.exists(f"{i + 1}.sql")
    check50.include("snap.db")


@check50.check(exists)
def test1():
    """1.sql produces correct result"""
    check_single_col(
        run_query("1.sql"),
        ['youthfulrespect224',
        'gracefulgift356',
        'exceptionalwisdom843',
        'incrediblewisdom960',
        'incrediblecompassion765',
        'awesomeenthusiasm921',
        'delightfulelegance193',
        'creativeparadise883',
        'impressiveopportunity267',
        'stunningelegance517',
        'sensationaljoy778',
        'thrivingcommitment546',
        'vibranthero601',
        'positiveparadise998',
        'happyrespect524',
        'lovelycommitment914',
        'peacefultrust147',
        'admirablesuccess620',
        'radiantcreativity958',
        'wonderfulfriendship325',
        'impressivecommitment918',
        'elegantcomfort516',
        'marvelousinspiration875'],
        ordered=False,
    )


@check50.check(exists)
def test2():
    """2.sql produces correct result"""
    check_single_cell(run_query("2.sql"), '2021-10-04 13:20:12')


@check50.check(exists)
def test3():
    """3.sql produces correct result"""
    check_single_col(
        run_query("3.sql"),
        ['29', '30', '48'],
        ordered=True,
    )


@check50.check(exists)
def test4():
    """4.sql produces correct result"""
    check_single_cell(run_query("4.sql"), 'impressivecommitment918')


@check50.check(exists)
def test5():
    """5.sql produces correct result"""
    check_single_col(
        run_query("5.sql"),
        ['8', '31', '32', '36', '43'],
        ordered=False,
    )


def run_query(filename):
    """
    Runs the SQL query contained in 'filename' and returns its output.

    positional arguments:
        filename (str)      file containing SQL query

    returns:
        list[dict]
    """

    try:
        with open(filename) as f:
            query = f.read().strip()
            query = sqlparse.format(query, strip_comments=True).strip()
        db = SQL("sqlite:///snap.db")
        result = db.execute(query)
        return result
    except Exception as e:
        raise check50.Failure(f"Error when executing query: {str(e)}")


def check_single_col(actual, expected, ordered=False):
    """
    Checks that the single column in 'actual' matches 'expected'.

    positional arguments:
        actual (list[dict])       result returned by run_query
        expected (list)           expected result to match against

    options:
        ordered (bool)            whether to check whether actual's order matches expected's

    returns:
        None

    raises:
        check50.Mismatch if actual does not match expected
        check50.Failure if error occurs
    """

    # convert list to list of frozen sets or set of frozen sets
    try:
        if ordered:
            expected = [frozenset([elt]) for elt in expected]
        else:
            expected = {frozenset([elt]) for elt in expected}
    except Exception as e:
        raise check50.Failure(f"Error when reading expected result: {str(e)}")
    return _check(actual, expected, ordered)


def check_single_cell(actual, expected):
    """
    Checks that the single cell in 'actual' matches 'expected'.

    positional arguments:
        actual (list[dict])       result returned by run_query
        expected (single element) expected result to match against

    returns:
        None

    raises:
        check50.Mismatch if actual does not match expected
        check50.Failure if error occurs
    """

    # convert element to list of frozen set; ordered doesn't matter
    try:
        expected = [frozenset([expected])]
    except Exception as e:
        raise check50.Failure(f"Error when reading expected result: {str(e)}")
    return _check(actual, expected, ordered=True)


def check_multi_col(actual, expected, ordered=False):
    """
    Checks that the columns in 'actual' matches 'expected'.

    positional arguments:
        actual (list[dict])       result returned by run_query
        expected (list[set])      expected result to match against

    options:
        ordered (bool)            whether to check whether actual's order matches expected's

    returns:
        None

    raises:
        check50.Mismatch if actual does not match expected
        check50.Failure if error occurs
    """

    # convert list of sets to list of frozen sets or set of frozen sets
    try:
        if ordered:
            expected = [frozenset(unfrozen_set) for unfrozen_set in expected]
        else:
            expected = {frozenset(unfrozen_set) for unfrozen_set in expected}
    except Exception as e:
        raise check50.Failure(f"Error when reading expected result: {str(e)}")
    return _check(actual, expected, ordered)


def _check(actual, expected, ordered=False):
    """
    Checks that the SQL output in 'actual' matches 'expected'.

    positional arguments:
        actual (list[dict])       result returned by run_query
        expected                  expected result to match against
            if ordered, should be list[frozenset];
            otherwise, set[frozenset]  (frozenset is needed for nested sets)

    options:
        ordered (bool)            whether to check whether actual's order matches expected's

    returns:
        None

    raises:
        check50.Mismatch if actual does not match expected
        check50.Failure if error occurs
    """

    # make sure query returned results
    if actual is None or actual == []:
        raise check50.Failure("Query did not return results")

    # convert list of dictionaries to list of frozen sets or set of frozen sets,
    # depending on whether 'ordered' is True
    try:
        result = []
        for row_dict in actual:
            values = [str(elt) for elt in list(row_dict.values())]
            result.append(frozenset(values))
        result = result if ordered else set(result)
    except Exception as e:
        raise check50.Failure(f"Error with format of query: {str(e)}")

    # check result of query against expected values
    if result != expected:
        raise check50.Mismatch(
            "\n".join(", ".join(list(sorted(entry))) for entry in list(expected)),
            "\n".join(", ".join(list(sorted(entry))) for entry in list(result)),
        )
    return None