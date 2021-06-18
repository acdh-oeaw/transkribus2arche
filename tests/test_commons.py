import unittest
from datetime import datetime
from rdflib import Graph, URIRef, RDF

from transkribus2arche.commons import ACDH_NS, san_uri_ref, add_triple, fix_date

g = Graph()
subj = URIRef("https://123.com")
g.add(
    (subj, RDF.type, ACDH_NS.Resource)
)

DATES = [
    ["1212-12-12", "1212-12-12 00:00:00"],
    [-1604451600000, "1919-02-28 00:00:00"],
    ["None", None],
    [None, None],
    [False, None],
    [datetime.fromtimestamp(-1604451600000 / 1000), "1919-02-28 00:00:00"]
]

TRIPLES = [
    ["hasFormat", "image/jpeg", "literal_no_lang"],
    ["hasCategory", "https://vocabs.acdh.oeaw.ac.at/archecategory/image", "uri"],
    ["hasTitle", "Hansi4ever", "literal", "und"],
    ["hasCoverageStartDate", "1900-01-01", "date"],
    ["hasNone", None, "date"],
    ["hasFalse", False, "date"],
    ["hasCoverageEndDate", -1604451600000, "date"],
    ["hasPid", "http://hdl.handle.net/whtever/com", "literal_as_uri"]
]
DATA = [
    {
        "bad": "http://sws.geonames.org/1232324343/linz.html",
        "good": "https://www.geonames.org/1232324343"
    },
    {
        "bad": "http://d-nb.info/gnd/4074255-6/",
        "good": "https://d-nb.info/gnd/4074255-6"
    },
    {
        "bad": "https://d-nb.info/gnd/4074255-6",
        "good": "https://d-nb.info/gnd/4074255-6"
    }
]


class TestCommons(unittest.TestCase):

    def test_001_san_uri_ref_return_type(self):
        for x in DATA:
            uri = san_uri_ref(x['bad'])
            self.assertIsInstance(
                uri, URIRef
            )

    def test_002_san_uri_rer_return_value(self):
        for x in DATA:
            uri = san_uri_ref(x['bad'])
            self.assertEqual(
                f"{uri}", x['good']
            )

    def test_003_add_triple_type(self):
        add_triple(g, subj, TRIPLES[0])
        self.assertTrue(len(g) == 2)
        for x in TRIPLES:
            add_triple(g, subj, x)
        self.assertFalse('http://hdl.handle' in f"{g.serialize()}")
        self.assertFalse('hasFalse' in f"{g.serialize()}")
        self.assertFalse('hasNone' in f"{g.serialize()}")
        new_g = add_triple(g, subj, TRIPLES[0])
        self.assertIsInstance(new_g, Graph)

    def test_004_fix_date(self):
        for x in DATES:
            fixed = fix_date(x[0])
            self.assertEqual(fixed, x[1])
