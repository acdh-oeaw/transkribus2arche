import glob
import json
import os
from datetime import datetime
from rdflib import Graph, URIRef, Literal, XSD, RDF

from .config import ACDH_NS


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


def read_json(path_to_file):
    with open(path_to_file) as f:
        data = json.load(f)
        return data


def list_docs(path_to_config):
    config = read_json(path_to_config)
    docs_glob_pattern = glob.glob(f"{config['col_dir']}/col/*/*.json")
    return docs_glob_pattern


def get_md_dict(trans_doc, path_to_config):
    config = read_json(path_to_config)
    item = {}
    data = read_json(trans_doc)
    md = data['md']
    mapping = config['mapping']
    for key, value in mapping.items():
        obj = md.get(value)
        if 'Date' in key and obj is not None:
            try:
                obj = datetime.fromtimestamp(obj)
            except ValueError:
                obj = datetime.fromtimestamp(obj / 1000)
        if 'hasExtend' in key:
            obj = config['arche_extend_pattern'].format(obj)
        item[key] = f"{obj}"
        item['hasIdentifier'] = f"{config['arche_base_url']}/{config['col_id']}/{md['docId']}"
        item['docId'] = md['docId']
    return item


def make_rdf(path_to_config, out_dir):
    try:
        os.makedirs(out_dir)
        print(f"Directory '{out_dir}' created")
    except FileExistsError:
        print(f"Directory '{out_dir}' alredy exists")
    config = read_json(path_to_config)
    global_constants = config['global_constants']
    img_constants = config['img_constants']
    xml_constants = config['xml_constants']
    base_lang = config['arche_base_lang']
    base_url = config['arche_base_url']
    replace_pattern = config['img_xml_pattern']
    for x in list_docs(path_to_config):
        g = Graph()
        g.parse(config['additional_md'], format="ttl")
        top_col_sub = URIRef(config['arche_base_url'])
        for triple in global_constants:
            add_triple(g, top_col_sub, triple)
        item = get_md_dict(x, path_to_config)
        sub = URIRef(item['hasIdentifier'])
        col_g = Graph()
        col_g.add(
            (sub, RDF.type, ACDH_NS.Collection)
        )
        for triple in global_constants:
            add_triple(col_g, sub, triple)
        col_g.add(
            (sub, ACDH_NS.isPartOf, URIRef(
                f"{base_url}"
            ))
        )
        col_g.add(
            (sub, ACDH_NS.hasTitle, Literal(
                item['hasTitle'], lang=base_lang
            ))
        )
        for key, value in item.items():
            if "Date" in key:
                col_g.add(
                    (sub, ACDH_NS[key], Literal(value, datatype=XSD.date))
                )
        g = g + col_g
        trp = read_json(x)['pageList']['pages']
        for p in trp:
            img_title = p['imgFileName']
            xml_title = img_title.replace(replace_pattern[0], replace_pattern[1])
            img_id = f"{item['hasIdentifier']}/{img_title}"
            xml_id = f"{item['hasIdentifier']}/{xml_title}"
            xml_subj = URIRef(xml_id)
            xml_g = Graph()
            xml_g.add(
                (xml_subj, RDF.type, ACDH_NS.Resource)
            )
            xml_g.add(
                (xml_subj, ACDH_NS.isPartOf, sub)
            )
            xml_g.add(
                (xml_subj, ACDH_NS.hasTitle, Literal(xml_title, lang="und"))
            )
            for triple in xml_constants:
                add_triple(xml_g, xml_subj, triple)
            for triple in global_constants:
                add_triple(xml_g, xml_subj, triple)

            p_subj = URIRef(img_id)
            p_g = Graph()
            for triple in img_constants:
                add_triple(p_g, p_subj, triple)
            for triple in global_constants:
                add_triple(p_g, p_subj, triple)
            p_g.add(
                (p_subj, RDF.type, ACDH_NS.Resource)
            )
            p_g.add(
                (p_subj, ACDH_NS.isPartOf, sub)
            )
            p_g.add(
                (p_subj, ACDH_NS.hasTitle, Literal(p['imgFileName'], lang="und"))
            )
            p_g.add(
                (p_subj, ACDH_NS.isSourceOf, xml_subj)
            )
            p_g.add(
                (
                    p_subj,
                    ACDH_NS.hasExtent,
                    Literal(
                        f"height: {p['height']}; width: {p['width']}",
                        lang="en"
                    )
                )
            )
            for d in ['key', 'pageId', 'pageNr', 'docId']:
                p_g.add(
                    (
                        p_subj,
                        ACDH_NS.hasNonLinkedIdentifier,
                        Literal(
                            f"{d}: {p[d]}", lang="und")
                    )
                )
            g = g + p_g
            g = g + xml_g
        save_path = os.path.join(out_dir, f"{item['docId']}.ttl")
        with open(save_path, 'w') as f:
            print(g.serialize(format='turtle').decode('UTF-8'), file=f)
    return g
