1. Purpose
The workflow provides a governed, repeatable process for moving ontology artifacts from local authoring through Git review, automated validation, S3 release-packet delivery, Semantic Layer intake, and downstream runtime availability.

It is designed to ensure that every ontology change is versioned, reviewed, traceable, technically valid, and recoverable before it is used by downstream Semantic Layer consumers.

2. Scope
In scope: ontology artifact updates, Git branching, pull request review, CI validation, release tagging, S3 packet publication.

3. Workflow at a Glance
Ontology team authoring — Ontology authors create feature/* branches from ontology-develop, commit modular ontology parts-file changes, open pull requests into ontology-develop, complete reviewer/steward review, and merge approved changes.

Jenkins consolidation and validation on ontology-develop — A merge to ontology-develop triggers Jenkins to check out the branch, consolidate modular files into a single .ttl artifact, run automated validation, notify owners if validation fails, and commit the validated consolidated artifact back to ontology-develop when successful.

Bitbucket release versioning and approval — When validated ontology changes are ready for release, the ontology team opens a release pull request from ontology-develop into develop, documents the release scope and impact, completes release review, addresses comments, and merges the approved PR into develop.

Jenkins manifest generation and deployment on develop — A merge to develop triggers Jenkins to retrieve the consolidated .ttl artifact, generate manifest.json, package the release artifacts, and deploy the immutable release packet to AWS S3.

S3 ontology release repository — The published packet is stored under the configured delivery bucket prefix, deployment completion status is updated, success notifications are emitted, and the ontology artifacts become available for downstream Semantic Layer consumers.

4. Detailed Workflow Process
Step 1 — Ontology team authoring
The ontology team authors modular ontology changes and submits them through the controlled feature-branch review process.

Create feature branch: the ontology author creates a user-specific feature branch from ontology-develop, such as feature/*.

Commit parts file: the author updates the modular ontology parts files and commits the changes to the feature branch.

Create pull request: the author opens a PR from the feature branch into ontology-develop.

Notify reviewers: configured reviewers, ontology stewards, governance representatives, and domain SMEs are notified automatically.

Review modular changes: reviewers inspect the parts-file changes for semantic intent, governance alignment, naming conventions, definitions, relationships, and business fit.

Address rejected changes: if the PR is rejected or comments are raised, the author updates the feature branch and the review cycle repeats.

Merge PR: once approved, the PR is merged into ontology-develop.



git checkout ontology-develop
git pull origin ontology-develop
git checkout -b feature/update-commercial-ontology
git status
git add ontology/ release-notes.md
git commit -m "Update commercial ontology parts"
git push origin feature/update-commercial-ontology


Step 2 — Jenkins consolidation and validation after merge to ontology-develop
After the approved feature PR is merged into ontology-develop, Jenkins automatically consolidates and validates the ontology changes.

Trigger pipeline: a Bitbucket webhook triggers Jenkins on merge to ontology-develop.

Checkout source: Jenkins checks out ontology-develop and identifies the merged commit.

Consolidate ontology: Jenkins executes the consolidation process to combine the modular ontology files into a single consolidated .ttl candidate artifact.

Run automated validation: Jenkins validates syntax, structure, semantic consistency, and release-readiness of the consolidated artifact.

Handle validation failures: if validation fails, Jenkins marks the build as failed, generates a validation report, notifies the PR author and approvers, and halts the pipeline.

Commit validated artifact: if validation succeeds, Jenkins commits the consolidated .ttl artifact back to ontology-develop.


Step 3 — Bitbucket release versioning and approval
Bitbucket provides the controlled release approval stage before the validated consolidated ontology artifact can progress to deployment.

Maintain ontology-develop: the ontology-develop branch contains the validated consolidated .ttl artifact.

Create release pull request: when a meaningful set of changes is ready for release, the ontology team opens a PR from ontology-develop into develop.

Document the release: the PR includes the change description, release scope, impact summary, release notes, and supporting documentation where applicable.

Notify release reviewers: configured ontology owners, taxonomy owners, governance representatives, and domain SMEs are notified automatically.

Review consolidated artifact: reviewers inspect the consolidated ontology artifact and associated release documentation.

Address review comments: if changes are required, the ontology team commits updates to ontology-develop and repeats the release review cycle.

Merge to develop: once required approvals are complete, the release PR is merged into develop.

Step 4 — Jenkins manifest generation and deployment after merge to develop
After the approved release PR is merged into develop, Jenkins prepares and publishes the immutable ontology release packet.

Trigger deployment pipeline: a Bitbucket webhook triggers Jenkins on merge to develop.

Checkout release source: Jenkins checks out develop, identifies the merged commit, and retrieves the consolidated .ttl file.

Generate manifest: Jenkins creates manifest.json from the release metadata required for downstream intake and traceability.

Package release artifacts: Jenkins packages the consolidated .ttl file and manifest.json into an immutable release packet.

Deploy to AWS S3: Jenkins uploads the release packet to the configured ontology delivery bucket.

Step 5 — S3 ontology release repository
The AWS S3 delivery bucket acts as the ontology release repository for immutable release packets consumed by downstream Semantic Layer processes.

The release packet lands under the required prefix pattern:



s3://sl-ontology-delivery-{env}/incoming/{producer}/{packetId}/
Recommended packet ID convention:



{producer}-{packetType}-{YYYYMMDD}T{HHmmss}Z-{seq}
Each published packet contains the validated consolidated ontology artifact, the generated manifest, and any supporting release metadata required by the Semantic Layer intake process.

Deployment completion updates the deployment status and emits success notifications. Published ontology artifacts are then available to downstream consumers such as semantic data products, knowledge graph pipelines, indexing services, semantic search, RAG systems, and related semantic applications.

5. Roles and Responsibilities
Role

Responsibilities

Ontology author

Authors modular parts files on feature/* branches, maintains clean commits, updates documentation and release notes, opens PRs into ontology-develop, addresses review comments, and helps initiate release PRs into develop when validated changes are ready.

Reviewer / steward

Reviews modular parts PRs for semantic intent, governance alignment, naming conventions, definitions, relationships, and domain fit; conducts final release reviews on consolidated artifacts before approval into develop.

Jenkins pipeline

On ontology-develop merge: consolidates modular parts files into a single .ttl artifact, executes automated syntax, structural, semantic, checksum, and compatibility validation, sends failure alerts, and commits the validated artifact back to ontology-develop.

On develop merge: generates manifest.json, packages the release artifacts, and deploys the immutable release packet to the AWS S3 delivery bucket.

6. Branching and Versioning Strategy
Branch

Purpose

Environment

Who Uses It

feature/*

Working branch for ontology authoring and modular parts-file updates

Authoring workspace

Ontologists

ontology-develop

Ontology integration branch for reviewed modular changes, automated Jenkins consolidation, validation, and validated consolidated .ttl artifact storage

Ontology integration / pre-release

Ontologists, reviewers, ontology stewards, Jenkins

develop

Release integration branch for approved consolidated ontology artifacts that are ready for manifest generation and S3 deployment

Development deployment source

Jenkins, release reviewers

Feature Branch (feature/*)

Created from ontology-develop

Used by ontologists to:

Create new TTL files

Update existing TTL files

Modify ontology definitions

Add ontology relationships

Multiple feature branches can exist simultaneously

Examples:

feature/add-oncology-domain

feature/update-drug-hierarchy

Feature/therapy-area-enhancement

Delete the feature branch once it is merged to the develop branch.

Ontology-Develop Branch (ontology-develop)

Acts as the ontology integration branch between feature authoring and the release-ready develop branch.

Receives approved pull requests from feature/* branches after modular ontology changes are reviewed.

Triggers the Jenkins consolidation and validation pipeline after each merge.

Stores the Jenkins-generated consolidated .ttl artifact once automated validation succeeds.

Serves as the source branch for release pull requests into develop when a meaningful set of validated ontology changes is ready for deployment.

If Jenkins validation fails, fixes are committed through the appropriate feature branch or directly to ontology-develop based on governance rules, and the validation cycle repeats.

Develop Branch (develop)

Represents the current Development deployment source.

Receives approved release pull requests from ontology-develop, not directly from feature branches.

Triggers the Jenkins manifest generation, release packaging, and S3 deployment pipeline.

Serves as the source for S3 deployment in the DEV environment.
