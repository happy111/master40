Hi @Samal, Umesh (Ext)

As discussed, can you please explore and implement the highlighted tasks?

Regards,
Nagarjuna Itte

________________________________________
From: Samant, Ajay <ajay.samant@novartis.com>
Sent: Wednesday, August 19, 2026 3:40 AM
To: Felder, Diana (Ext) <diana.felder_ext@novartis.com>; Bishop, Leah (Ext) <leah.bishop_ext@novartis.com>; Itte, Nagarjuna <nagarjuna.itte@novartis.com>; Majumder, Urmi (Ext) <urmi.majumder_ext@novartis.com>; Aguilar Islas, Fernando (Ext) <fernando.aguilar_islas_ext@novartis.com>
Cc: Fung, Heidon <heidon.fung@novartis.com>
Subject: Re: Protege install status and next steps. 

Additional Context
•	Given the current limitations and constraints, the approval and review process should be kept as simple and lightweight as possible.
•	The intent is to avoid building a full-scale custom portal solely to support ontology approval and review workflows unless there is a clear enterprise requirement to do so.
•	The proposed Protégé + Git + CI/CD approach should therefore be viewed as a tactical solution designed to unblock the NovaOS implementation in the near term.
•	At the same time, the tactical approach should not compromise key requirements such as:
o	Version control and traceability
o	Formal review and approval
o	Controlled promotion of approved ontology artifacts
o	Validation through SHACL
o	Auditability of what was approved and deployed
•	This is not intended to define the long-term enterprise ontology management and governance model.
•	As the enterprise approach matures, we will need to revisit ontology authoring, governance, approval workflows, collaboration, and lifecycle management from a broader enterprise perspective.
•	For now, the objective is to implement a practical temporary solution that removes the immediate blocker while preserving the critical governance and deployment controls we need.
Looking forward to hearing from you on Protege experience 🙂 Let us know.




________________________________________
From: Felder, Diana (Ext) <diana.felder_ext@novartis.com>
Sent: Tuesday, August 18, 2026 3:08 PM
To: Samant, Ajay <ajay.samant@novartis.com>; Bishop, Leah (Ext) <leah.bishop_ext@novartis.com>; Itte, Nagarjuna <nagarjuna.itte@novartis.com>; Majumder, Urmi (Ext) <urmi.majumder_ext@novartis.com>; Aguilar Islas, Fernando (Ext) <fernando.aguilar_islas_ext@novartis.com>
Cc: Fung, Heidon <heidon.fung@novartis.com>
Subject: RE: Protege install status and next steps.
 
Thanks, Ajay! Forwarding this to Urmi and Fernando to look over the proposed approval and deployment workflow.
 
From: Samant, Ajay <ajay.samant@novartis.com>
Sent: Tuesday, August 18, 2026 10:06 AM
To: Bishop, Leah (Ext) <leah.bishop_ext@novartis.com>; Itte, Nagarjuna <nagarjuna.itte@novartis.com>; Felder, Diana (Ext) <diana.felder_ext@novartis.com>
Cc: Fung, Heidon <heidon.fung@novartis.com>
Subject: Re: Protege install status and next steps.
 
 
Great, thanks!!
 
Now do the magic in Protege and let us know if you could author it as you wanted so we can showcase this to others later.
 
Review the integration flow and let us know. We are making sure there is zero impact to AWS layer as long as they get the files as expected on S3. Does not matter if it comes from Protege or CENTree. 
 
Sooner you and Diana validate Protege if it meets your requirements then we can start our work on the proposed soln explained below.  Even if we go back to CENTRee the impact is minimum - nothing on AWS side - our integration code will change.
 
Proposed Custom Approval & Deployment Workflow for Protégé Ontology Files
1	Ontology authoring
	o	Ontology authors create and maintain the ontology locally using Protégé.
	o	Associated SHACL validation files are maintained alongside the ontology where applicable.
2	Source control submission
	o	Once the ontology is ready for formal review, the author commits/pushes the ontology file and associated artifacts from the local environment to the designated Novartis Git repository.
	o	Git becomes the controlled source for versioning, review history, and traceability.
3	Automated approval initiation
	o	The Git check-in triggers an automated pipeline.
	o	The pipeline invokes custom workflow code that identifies the designated approver and sends an email notification containing a link to the submitted ontology/version.
4	Reviewer validation and approval
	o	The approver accesses the submitted ontology using the provided link and performs the required review/validation.
	o	Once approved, the reviewer applies an "Approved" tag/status to the corresponding Git version and checks in the approval change.
	o	This provides an auditable record of exactly which ontology version was approved.
5	Automated deployment trigger
	o	The approved tag/status triggers the downstream CI/CD pipeline.
	o	The pipeline executes custom deployment logic only for approved ontology versions.
6	Generate required deployment artifacts
	o	The deployment process packages the approved:
		Ontology file
		SHACL file
	o	In addition, the pipeline dynamically generates the required MANIFEST file based on the approved ontology package and deployment requirements.
7	Publish to AWS
	o	The CI/CD pipeline copies the ontology file, SHACL file, and MANIFEST file to the appropriate controlled Amazon S3 locations expected by the downstream AWS components.
	o	This provides a clear separation between authoring, approval, and runtime consumption.
8	Overall control model
	o	Protégé → ontology authoring
	o	Git → version control and approval traceability
	o	Custom workflow → reviewer notification and approval process
	o	CI/CD → controlled promotion of approved artifacts
	o	S3 → approved ontology package consumed by the AWS implementation
________________________________________
From: Bishop, Leah (Ext) <leah.bishop_ext@novartis.com>
Sent: Tuesday, August 18, 2026 10:07 AM
To: Samant, Ajay <ajay.samant@novartis.com>; Itte, Nagarjuna <nagarjuna.itte@novartis.com>; Felder, Diana (Ext) <diana.felder_ext@novartis.com>
Cc: Fung, Heidon <heidon.fung@novartis.com>
Subject: RE: Protege install status
 
It is installed from your link and working.
 
Thanks Ajay!
 
Leah
 
From: Samant, Ajay <ajay.samant@novartis.com>
Sent: Tuesday, August 18, 2026 7:39 AM
To: Itte, Nagarjuna <nagarjuna.itte@novartis.com>; Bishop, Leah (Ext) <leah.bishop_ext@novartis.com>; Felder, Diana (Ext) <diana.felder_ext@novartis.com>
Cc: Fung, Heidon <heidon.fung@novartis.com>
Subject: Protege install status
 
Let us know asap today if you could install Protege successfully.
 
If you just install it with this option "install for local user only" then I think you can do it on your own.
 
Regards
Ajay
