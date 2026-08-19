import argparse
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


def send_approval_email(
    approver_email: str,
    ontology_name: str,
    version: str,
    commit_sha: str,
    ontology_url: str,
):
    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.environ["SMTP_USERNAME"]
    smtp_password = os.environ["SMTP_PASSWORD"]
    from_email = os.environ["FROM_EMAIL"]

    subject = (
        f"Ontology Approval Required - "
        f"{ontology_name} - {version}"
    )

    body = f"""
Hello,

An ontology has been submitted for formal review.

Ontology:
{ontology_name}

Version:
{version}

Git Commit:
{commit_sha}

Please review the submitted ontology/version:

{ontology_url}

This version must be reviewed and approved before deployment.

Regards,
Ontology CI/CD Pipeline
"""

    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = approver_email

    message.set_content(body)

    print(f"Sending email to: {approver_email}")

    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.starttls()

        smtp.login(
            smtp_username,
            smtp_password,
        )

        smtp.send_message(message)

    print("Approval email sent successfully.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--approver", required=True)
    parser.add_argument("--ontology", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--url", required=True)

    args = parser.parse_args()

    send_approval_email(
        approver_email=args.approver,
        ontology_name=args.ontology,
        version=args.version,
        commit_sha=args.commit,
        ontology_url=args.url,
    )
