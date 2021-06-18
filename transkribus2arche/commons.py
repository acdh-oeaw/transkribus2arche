from AcdhArcheAssets.uri_norm_rules import get_normalized_uri
from rdflib import URIRef, Literal, XSD, Namespace


REPO_SCHEMA = "https://raw.githubusercontent.com/acdh-oeaw/repo-schema/master/acdh-schema.owl"
ACDH_NS = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")
OWL_NS = Namespace("http://www.w3.org/2002/07/owl#")


def san_uri_ref(uri):
    san_uri = get_normalized_uri(uri)
    return URIRef(san_uri)


def add_triple(g, sub, triple):
    tr_type = triple[2]
    if tr_type == "uri":
        g.add(
            (
                sub,
                ACDH_NS[triple[0]],
                URIRef(triple[1])
            )
        )
    elif tr_type == "literal_no_lang":
        g.add(
            (
                sub,
                ACDH_NS[triple[0]],
                Literal(triple[1])
            )
        )
    elif tr_type == "literal":
        g.add(
            (
                sub,
                ACDH_NS[triple[0]],
                Literal(
                    triple[1],
                    lang=triple[3]
                )
            )
        )
    elif tr_type == "literal_as_uri":
        g.add(
            (
                sub,
                ACDH_NS[triple[0]],
                Literal(URIRef(triple[1]))
            )
        )
    elif tr_type == "date":
        g.add(
            (
                sub,
                ACDH_NS[triple[0]],
                Literal(
                    triple[1],
                    datatype=XSD.date
                )
            )
        )
    return g
