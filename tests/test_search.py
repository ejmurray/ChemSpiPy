# -*- coding: utf-8 -*-
"""
test_search
~~~~~~~~~~~

Test the search wrapper.

:copyright: Copyright 2014 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
import logging
import os

import nose
from nose.tools import eq_, ok_, raises

from chemspipy import ChemSpider, ASCENDING, DESCENDING, CSID, REFERENCE_COUNT, MOLECULAR_WEIGHT
from chemspipy.errors import ChemSpiPyServerError


logging.basicConfig(level=logging.WARN, format='%(levelname)s:%(name)s:(%(threadName)-10s):%(message)s')
logging.getLogger('chemspipy').setLevel(logging.DEBUG)

# Security token is retrieved from environment variables
CHEMSPIDER_SECURITY_TOKEN = os.environ['CHEMSPIDER_SECURITY_TOKEN']
cs = ChemSpider(security_token=CHEMSPIDER_SECURITY_TOKEN)


def test_search_smiles():
    """Test SMILES input to search."""
    results = cs.search('O=C(OCC)C')
    eq_(results.ready(), False)
    results.wait()
    eq_(results.ready(), True)
    eq_(results.success(), True)
    eq_(results.message, 'Found by conversion query string to chemical structure (full match)')
    eq_(results[0].csid, 8525)
    ok_(results.duration.total_seconds() > 0)


def test_search_csid():
    """Test ChemSpider ID input to search."""
    results = cs.search(8525)
    eq_(results.message, 'Found by CSID')
    eq_(len(results), 1)
    eq_(repr(results), 'Results([Compound(8525)])')
    eq_(results[0].csid, 8525)


def test_search_name():
    """Test name input to search."""
    results = cs.search('propanol')
    eq_(results.message, 'Found by approved synonym')
    eq_(results[0].csid, 1004)


def test_search_iter():
    """Test iteration of search results."""
    for result in cs.search('glucose'):
        ok_(result.csid in [5589, 58238, 71358, 96749, 9312824, 9484839])


def test_search_ordered_csid():
    """Test search results ordered by CSID."""
    results = cs.search('glucose', order=CSID)
    eq_([result.csid for result in results], [5589, 58238, 71358, 96749, 9312824, 9484839])


def test_search_ordered_csid_descending():
    """Test search results ordered by CSID and direction descending."""
    results = cs.search('glucose', order=CSID, direction=DESCENDING)
    eq_([result.csid for result in results], [9484839, 9312824, 96749, 71358, 58238, 5589])


def test_search_ordered_ref_descending():
    """Test search results ordered by CSID and direction descending."""
    results = cs.search('glucose', order=REFERENCE_COUNT, direction=DESCENDING)
    eq_([result.csid for result in results], [96749, 5589, 58238, 9484839, 71358, 9312824])


def test_search_ordered_weight_ascending():
    """Test search results ordered by CSID and direction descending."""
    results = cs.search('P', order=MOLECULAR_WEIGHT, direction=ASCENDING)
    eq_([result.csid for result in results], [4574144, 1010, 128566, 21111774, 14319])


def test_search_no_results():
    """Test name input to search."""
    results = cs.search('aergherguyaelrgiaubrfawyef')
    eq_(results.message, 'No results found')
    eq_(results.ready(), True)
    eq_(results.success(), True)
    eq_(len(results), 0)


@raises(IndexError)
def test_too_high_index():
    """Test IndexError is raised for a too high index."""
    result = cs.search('glucose')[7843]


def test_search_failed():
    """Test ChemSpiPyServerError is raised for an invalid SMILES."""
    results = cs.search('O=C(OCC)C*')
    results.wait()
    ok_(isinstance(results.exception, ChemSpiPyServerError))
    eq_(results.status, 'Failed')
    eq_(repr(results), 'Results(Failed)')
    eq_(results.ready(), True)
    eq_(results.success(), False)
    eq_(results.count, 0)
    ok_(results.duration.total_seconds() > 0)


@raises(ChemSpiPyServerError)
def test_search_exception():
    """Test ChemSpiPyServerError is raised for an invalid SMILES."""
    results = cs.search('O=C(OCC)C*', raise_errors=True)
    results.wait()



# ordered search - ascending/descending, different sort orders


if __name__ == '__main__':
    nose.main()
