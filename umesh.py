import hashlib
import json
import os
from pathlib import Path

from rdflib import Graph


ONTOLOGY_FILE = Path("ontology/commercial-domain-model.ttl")
SHACL_FILE = Path("shapes/commercial-shapes.ttl")
APPROVAL_FILE = Path("deployment/approval.json")

MANIFEST_FILE = Path("deployment/manifest.json")


def calculate_sha256(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def count_triples(file_path: Path) -> int:
    graph = Graph()
    graph.parse(file_path, format="turtle")
    return len(graph)


def load_approval():
    if not APPROVAL_FILE.exists():
        raise FileNotFoundError(
            "Approval file does not exist. Deployment is not allowed."
        )

    with APPROVAL_FILE.open("r", encoding="utf-8") as file:
        approval = json.load(file)

    if approval.get("status") != "approved":
        raise RuntimeError(
            "Ontology is not approved. Manifest cannot be generated."
        )

    return approval


def generate_manifest():
    if not ONTOLOGY_FILE.exists():
        raise FileNotFoundError(ONTOLOGY_FILE)

    if not SHACL_FILE.exists():
        raise FileNotFoundError(SHACL_FILE)

    approval = load_approval()

    ontology_sha256 = calculate_sha256(ONTOLOGY_FILE)
    shacl_sha256 = calculate_sha256(SHACL_FILE)

    triple_count = count_triples(ONTOLOGY_FILE)

    version = os.getenv("ONTOLOGY_VERSION", "0.1.0")
    commit_sha = approval["commitSha"]

    manifest = {
        "manifestSchemaVersion": "1.0.0",
        "artifacts": [
            {
                "artifactId": "commercial-domain-model",
                "version": version,
                "file": (
                    "ontology/"
                    "commercial-domain-model.ttl"
                ),
                "format": "turtle",
                "sha256": ontology_sha256,
                "tripleCount": triple_count,
                "approvalStatus": "approved",
                "approvedBy": approval["approvedBy"],
                "sourceRef": f"git:{commit_sha}",
            },
            {
                "artifactId": "commercial-shapes",
                "version": version,
                "file": "shapes/commercial-shapes.ttl",
                "format": "turtle",
                "sha256": shacl_sha256,
                "approvalStatus": "approved",
                "approvedBy": approval["approvedBy"],
                "sourceRef": f"git:{commit_sha}",
            },
        ],
    }

    MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)

    with MANIFEST_FILE.open("w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=2)

    print("=" * 60)
    print("MANIFEST GENERATED")
    print("=" * 60)
    print(json.dumps(manifest, indent=2))

    return MANIFEST_FILE


if __name__ == "__main__":
    generate_manifest()
