# -*- coding: utf-8 -*-

import pytest
import os

from efs_parser.BigBed import BigBed

__author__ = "jkanche, elgaml"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions 
    come from the pyBigWig library
"""

bb = BigBed("https://obj.umiacs.umd.edu/bigwig-files/ENCFF330GHF.bigBed")

def test_correct_format():
    assert (bb.header['magic']==2273964779)

def test_header():
    assert(bb.header == {'magic': 2273964779, 'version': 4, 'zoomLevels': 10, 'chromTreeOffset': 953, 'fullDataOffset': 1275, 'fullIndexOffset': 142913985, 'fieldCount': 9, 'definedFieldCount': 9, 'autoSqlOffset': 304, 'totalSummaryOffset': 849, 'uncompressBufSize': 29537})

def test_columns():
    assert(len(bb.columns) == bb.header['fieldCount'])
    #assert(bb.columns == ['chr', 'start', 'end', 'name', 'score', 'strand', 'thickStart',7 'thickEnd', 'reserved'])

def test_range():
    start = 10000000
    end = 10020000
    res, err = bb.getRange(chr="chr1", start=start, end=end)
    assert(err == None)
    for _, row in res.iterrows():
        assert (row['start'] <= end or row['end'] >= start)

def test_get_bytes():
    res = bb.get_bytes(1, 100)
    assert (len(res) == 100)

def test_bin_rows():
    result, err = bb.getRange(chr="chr1", start=10000000, end=10010000, bins=2000, zoomlvl=-2)
    res, err = bb.bin_rows(data=result, chr="chr1", start=10000000, end=10010000, columns=['score'])
    assert (err == None)