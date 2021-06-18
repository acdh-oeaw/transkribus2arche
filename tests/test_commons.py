import unittest
from rdflib import Graph, URIRef, RDF

from transkribus2arche.commons import ACDH_NS, san_uri_ref, add_triple

g = Graph()
subj = URIRef("https://123.com")
g.add(
    (subj, RDF.type, ACDH_NS.Resource)
)

TRIPLES = [
    ["hasFormat", "image/jpeg", "literal_no_lang"],
    ["hasCategory", "https://vocabs.acdh.oeaw.ac.at/archecategory/image", "uri"],
    ["hasTitle", "Hansi4ever", "literal", "und"]
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
        self.assertTrue(len(g) == 4)
