from pathlib import Path
from rdflib import Graph
from pyshacl import validate


ONTOLOGY_FILE = Path("ontology/commercial-domain-model.ttl")
SHACL_FILE = Path("shapes/commercial-shapes.ttl")


def validate_ontology():
    print("=" * 60)
    print("ONTOLOGY VALIDATION")
    print("=" * 60)

    if not ONTOLOGY_FILE.exists():
        raise FileNotFoundError(f"Ontology not found: {ONTOLOGY_FILE}")

    if not SHACL_FILE.exists():
        raise FileNotFoundError(f"SHACL file not found: {SHACL_FILE}")

    ontology_graph = Graph()
    ontology_graph.parse(ONTOLOGY_FILE, format="turtle")

    print(f"Ontology: {ONTOLOGY_FILE}")
    print(f"Triples: {len(ontology_graph)}")

    shacl_graph = Graph()
    shacl_graph.parse(SHACL_FILE, format="turtle")

    print(f"SHACL: {SHACL_FILE}")
    print(f"SHACL triples: {len(shacl_graph)}")

    conforms, results_graph, results_text = validate(
        ontology_graph,
        shacl_graph=shacl_graph,
        inference="none",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
    )

    print("\nSHACL validation result:")
    print(results_text)

    if not conforms:
        raise RuntimeError("SHACL validation FAILED")

    print("SHACL validation PASSED")

    return True


if __name__ == "__main__":
    validate_ontology()
