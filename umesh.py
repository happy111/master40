import argparse
from pathlib import Path

import boto3


ONTOLOGY_FILE = Path("ontology/commercial-domain-model.ttl")
SHACL_FILE = Path("shapes/commercial-shapes.ttl")
MANIFEST_FILE = Path("deployment/manifest.json")


def upload_file(s3_client, bucket, local_file, s3_key):
    print(f"Uploading {local_file} -> s3://{bucket}/{s3_key}")

    s3_client.upload_file(
        str(local_file),
        bucket,
        s3_key,
    )


def deploy(bucket: str, packet_id: str):
    if not ONTOLOGY_FILE.exists():
        raise FileNotFoundError(ONTOLOGY_FILE)

    if not SHACL_FILE.exists():
        raise FileNotFoundError(SHACL_FILE)

    if not MANIFEST_FILE.exists():
        raise FileNotFoundError(
            "manifest.json must exist before deployment."
        )

    s3 = boto3.client("s3")

    prefix = f"incoming/centree/{packet_id}"

    # ---------------------------------------------------------
    # IMPORTANT:
    # Upload ontology and SHACL first.
    # ---------------------------------------------------------

    upload_file(
        s3,
        bucket,
        ONTOLOGY_FILE,
        f"{prefix}/ontology/commercial-domain-model.ttl",
    )

    upload_file(
        s3,
        bucket,
        SHACL_FILE,
        f"{prefix}/shapes/commercial-shapes.ttl",
    )

    # ---------------------------------------------------------
    # MANIFEST MUST BE LAST
    # ---------------------------------------------------------

    upload_file(
        s3,
        bucket,
        MANIFEST_FILE,
        f"{prefix}/manifest.json",
    )

    print()
    print("=" * 60)
    print("DEPLOYMENT COMPLETE")
    print("=" * 60)
    print(f"s3://{bucket}/{prefix}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--bucket",
        required=True,
        help="Target S3 bucket"
    )

    parser.add_argument(
        "--packet-id",
        required=True,
        help="Unique deployment packet ID"
    )

    args = parser.parse_args()

    deploy(
        bucket=args.bucket,
        packet_id=args.packet_id,
    )
