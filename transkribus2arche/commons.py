from AcdhArcheAssets.uri_norm_rules import get_normalized_uri
from dateutil.parser import parse, ParserError
from datetime import datetime
from rdflib import URIRef, Literal, XSD, Namespace


REPO_SCHEMA = "https://raw.githubusercontent.com/acdh-oeaw/repo-schema/master/acdh-schema.owl"
ACDH_NS = Namespace("https://vocabs.acdh.oeaw.ac.at/schema#")
OWL_NS = Namespace("http://www.w3.org/2002/07/owl#")


def fix_date(potential_date):
    if not potential_date:
        return None
    elif isinstance(potential_date, str):
        try:
            date = parse(potential_date)
        except ParserError:
            return None
    elif isinstance(potential_date, int):
        try:
            date_obj = datetime.fromtimestamp(potential_date)
        except ValueError:
            date_obj = datetime.fromtimestamp(potential_date / 1000)
        date = parse(f"{date_obj}")
    elif isinstance(potential_date, datetime):
        date = f"{potential_date}"
    else:
        return None
    return f"{date}"


def san_uri_ref(uri):
    san_uri = get_normalized_uri(uri)
    return URIRef(san_uri)


def add_triple(g, sub, triple):
    if triple[1] is None:
        return g
    elif triple[1] is False:
        return g
    else:
        tr_type = triple[2]
        if tr_type == "uri":
            g.add(
                (
                    sub,
                    ACDH_NS[triple[0]],
                    san_uri_ref(triple[1])
                )
            )
        elif tr_type == "date":
            fixed_date = fix_date(triple[1])
            if fix_date is not None:
                g.add(
                    (
                        sub,
                        ACDH_NS[triple[0]],
                        Literal(
                            fixed_date,
                            datatype=XSD.date
                        )
                    )
                )
            else:
                return g
        elif tr_type == "literal_no_lang":
            g.add(
                (
                    sub,
                    ACDH_NS[triple[0]],
                    Literal(triple[1])
                )
            )
        elif tr_type == "literal_as_uri":
            g.add(
                (
                    sub,
                    ACDH_NS[triple[0]],
                    Literal(san_uri_ref(triple[1]))
                )
            )
        else:
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
    return g
