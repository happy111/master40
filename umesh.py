import sys
import yaml
from pathlib import Path


CONFIG_FILE = Path("config/approvers.yaml")


def identify_approver(ontology_type: str) -> str:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Approver configuration not found: {CONFIG_FILE}"
        )

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    approvers = config.get("approvers", {})

    reviewers = approvers.get(ontology_type)

    if not reviewers:
        raise ValueError(
            f"No approver configured for ontology type: {ontology_type}"
        )

    return reviewers[0]


if __name__ == "__main__":
    ontology_type = sys.argv[1] if len(sys.argv) > 1 else "commercial"

    reviewer = identify_approver(ontology_type)

    print("=" * 60)
    print("APPROVER IDENTIFICATION")
    print("=" * 60)
    print(f"Ontology type : {ontology_type}")
    print(f"Approver      : {reviewer}")
