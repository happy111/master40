STORY: Story 1: Python Script Development

SUMMARY:
Develop Python Scripts for Ontology Manifest Generation and Release Artifact Packaging

DESCRIPTION:
Develop Python scripts to support the existing ontology delivery pipeline. The scripts will generate manifest.json using the approved release metadata and prepare the consolidated ontology .ttl file and manifest for deployment to AWS S3.

SUBTASKS:
1. Review the existing repository and identify required input files and metadata.
2. Develop the Python script for manifest generation.
3. Develop Python functionality to prepare the release package.
4. Validate required input files and metadata.
5. Document script execution and configuration.

ACCEPTANCE CRITERIA:
1. The Python script generates manifest.json using the approved schema.
2. The consolidated .ttl file and manifest are included in the release package.
3. Required input files and metadata are validated before packaging.
4. The output follows the agreed release directory structure.
5. The scripts can be executed locally and from Jenkins.
6. The code is committed to the designated Git branch and submitted for review.



STORY: Story 2: File Commit Integration

SUMMARY:
Implement Automated Commit of Validated Ontology Artifacts to the Git Repository

DESCRIPTION:
Implement and integrate the file commit process for the validated consolidated ontology artifact. Following successful consolidation and validation, the generated .ttl artifact should be committed to the ontology-develop branch through the existing Jenkins workflow, following the repository's Git branching and approval policies.

SUBTASKS:
1. Review the existing Jenkins Git checkout and commit process.
2. Identify how the validated .ttl artifact is generated and where it should be stored.
3. Implement or configure the automated commit process.
4. Handle Git commit and push failures.
5. Verify the committed artifact in the target branch.

ACCEPTANCE CRITERIA:
1. The validated .ttl artifact is committed to ontology-develop after successful validation.
2. The commit includes an appropriate commit message and references the source build or commit.
3. The pipeline does not commit the artifact if validation fails.
4. Git push failures are reported clearly in Jenkins.
5. The committed artifact is available in the repository.
6. The process does not overwrite unrelated changes or bypass existing branch protection rules.


STORY: Story 3: Testing and Logging

SUMMARY:
Implement Automated Testing and Logging for Ontology Release Scripts

DESCRIPTION:
Implement automated tests and logging for the Python manifest generation and artifact packaging scripts. Ensure that successful execution, invalid inputs, and processing failures are handled and reported clearly.

SUBTASKS:
1. Write unit tests for manifest generation.
2. Test missing files and invalid metadata scenarios.
3. Test release artifact packaging.
4. Implement or improve application logging.
5. Test error handling and review test results.

ACCEPTANCE CRITERIA:
1. Unit tests cover successful manifest generation and artifact packaging.
2. Tests cover missing files, invalid metadata, and other expected failure scenarios.
3. Logs provide sufficient information to identify the failed processing step.
4. Errors are reported clearly and cause the script to exit with a failure status.
5. Tests can run locally and through Jenkins.
6. Test results are documented and reviewed.
