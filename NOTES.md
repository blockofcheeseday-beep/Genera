# NOTES

## Key Decisions and Verification Delta Points Informing Design

Please note that the key decisions and verification delta sections have been consolidated into this one section in order to reflect the cadence of this exercise, in which verification deltas ended up constructively and substantively contributing to pipeline design and agent behavior. 

### 1. Reference samples setting the form of an output but never its parameters

In the middle of discussing permission scope and agent inference, the skill and pipeline orchestrating agent caught that the capability ledger was informed by the Westbrook sample’s design. As noted in the case study packet, the sample is “not an exercise” and “there’s nothing to run or submit for it.” The risk here was having the agent build on a reference file that provides some general guidance on form to the pipeline but should not provide strict parameters to follow.

**Passed on:** treating the sample as a template where mid-session.

**Issue:** an owner maps to `BUSINESS_ADMIN`, generalised from the sample's one administrator. Acme names its administrators as "Priya and me" and Hypergrowth as "me and maya", the assistant existing precisely to keep account changes off the CEO's desk. Neither CEO is in either list.

**Change:** In addition to correcting for role (both became `BUSINESS_USER` and were mapped by administrative responsibility rather than job title (`29059cd`)), the same reading found two more sample-derived errors: a "(surname pending roster)" placeholder on a packet with no roster (`85d83cf`), and reimbursements enabled on three Apex programmes the packet never mentions. None was caught by tooling, so before submission I spun off a system of 3 agents to conduct a final review: one catalogued, one judged each against "would this still be here if the sample had never existed", and one applied only the contamination.

### 2. Assigning deterministic and customer-agnostic behavior to code while keeping judgement with the orchestrating agent

I was pointed from the get go in wanting scalability of process and reliability and, as a result, from the initial brainstorming I led with a key decision to build deterministic forty-three ledger rows in YAML, keyed on what customers say rather than on endpoints, plus nine scripted checks. The agent would in turn be in charge for parsing through and applying judgment to messy transcripts, conflicting documents, or what Ramp cannot do. 

**Passed on:** Handwritten helpers to extract citations from transcripts each time Claude is invoked on a packet.

**Issue:** Inconsistency in audit log output decision making across packets A and C.

**Change:** cite.py added to scripts folder to help enforce rules mechanically.

### 3. Ensuring pipeline is both affirmatively flagging discrepancies as well as never silently overlooking flags

With the original design, the pipeline and agent were putting forward key assumptions that would likely be misinterpreted by a client. Some of the key changes below demonstrate guidance informing the agent of a broader stance on what should be flagged.   

**Example:** Random use of pronouns in audit log that do not clearly reference the key user involved. 

**Change:** Pivoted agent to write users as names only. 

**Example:** The agent pulled transcript citations in packet A that did not sufficiently provide context backing configuration decisions. 

**Change:** Expanded agent to pull in more citation lines per configuration assumption.

During the first pass run, the agent also failed to surface areas of incomplete information and would take on the aggressive stance of filling in these holes with placeholders. For client configurations and audit logs, clear, simple communication is critical to avoiding misinterpretation of what they see as a source of truth. As a result, I pivoted the agent to specifically note areas where no information was provided: 

**Example**: where a packet gave no email address, the config carried a constructed one at the customer's apparent domain. 

**Change**: Mark explicitly as N/A in the field. 

**Example**: packet D's software card had been widened to Cloud computing on the inference that a subscription budget covers infrastructure, disclosed only in a `translation_notes` field (`29059cd`).

**Change:** Cloud computing removed as a possible aspect of subscription budget. 

## Ramp Doc Design Impact

The OpenAPI schema was available as a machine-readable artifact, pulled from `docs.ramp.com/openapi/developer-api.json`. This provided me operation-level structure, scopes, and the `x-ramp-plus-required` / `x-beta` / `x-read-only` flags. Additionally, note that the prose docs pages were blocked by this environment's egress proxy for `curl` and page fetches alike, so anything semantic required on search-returned titles and quoted excerpts.

Example areas of Ramp technical documentation impact on design are as follows: 

- **Data Relationships:** Many-to-one edges get existence-and-uniqueness validation on the target, one-to-many edges get orphan detection on the inverse, and `inverse_field_name` lets the graph be walked in both directions from one pass. Some tangible examples of this influencing pipeline design include: 
  - Ramp labels every reference (e.g. one department per user, many users per department) while the output format keeps the same references and strips the labels. As a result, a department is whatever string a user names rather than a record that has to exist.
  - Validation is written per edge type rather than field, thereby collapsing four field-specific rules into two structural ones.
- **Entities.** The accounting guide states positively that entities are created in the Ramp UI and scoped by `entity_id`, moving `CAP-ENTITY-CREATE` from absence-based UNSUPPORTED to evidenced UI_ONLY and validating packet B's `status: requested`.
- **Roles.** *User role deep-dive: IT Admin* supplies semantics the spec does not: `IT_ADMIN` grants People and Integrations access while denying spend controls, exactly the "manage users but not limits" split Acme and Hypergrowth both asked for.



## Go-live handoff — Apex Health Partners

The configuration implements all six requirements from the Apex security document, with four enforced by the Ramp platform and two by compensating controls. Please note the following flags for further review: 

**Purchase-order matching (REQ-3)**

- **For Apex Health Partners**: Not met as written as Ramp cannot verify a purchase order number while a card is being authorized. Note that a non-compliant transaction completes and is caught afterward. Apex to review with the Risk Committee in those terms and to revert on whether detection is accepted, or whether a lower cap is required to approximate prevention.

**High-limit card activation (REQ-2)**

- **For Apex Health Partners:** Cards above $10,000 monthly are created suspended and cannot transact until the Compliance Office confirms the notarized form. Ramp does not verify that the form exists. Apex to name an owner for the confirmation step and a backup, given that a cardholder cannot transact while that step is pending.

**Per-transaction cap**

- **For Apex Health Partners:** The security document requires a purchase order above $500 while the discovery call sets the clinic cap at $1,000, leaving a band where a purchase is card-approved and simultaneously subject to the PO rule. The $1,000 cap is configured as stated and the gap flagged rather than resolved unilaterally. Apex to consider whether reconciliation covers that band or the cap drops to $500, and revert.

**Vendor prohibition (REQ-1)**

- **For Apex Health Partners:** The block takes effect only once both trading names (Joe's Medical Supply and JMS Distribution) resolve to merchant records, and it does not carry to card programs created later. Apex to confirm both records and to add re-application to its card program creation checklist.

**User provisioning**

- **For Apex Health Partners:** The packet contains no email address for any individual and names no clinic manager, so no user can be invited and the three-week clinic timeline starts when the roster arrives. Apex to revert with the roster, contract nurse assignment end dates, and the full membership of the Compliance Office.

## **Capability and Questions**

**Capability**: On our check-in, Efren named a bottleneck that doesn't show up in this portion of the exercise: a large share of deployment lag is being able to design a process behind waiting on the customer to come back (including being able to respond to customer answers faster and set up answers better before the customer makes a request). That then points me to the `missing_information_flags` , which is the section that touches the bottleneck. Every packet has context on what is missing based on set pipeline requirements (e.g. Apex Health Partners has no email address for any of six hundred employees and no clinic manager named).

The schema already carries what a send would need — blocking versus not, the affected config section, each item phrased as the question you would ask. What it does not do is leave the file, which I think is a critical pipeline to building out agentic workflows. The same field that gates go-live could produce a message and could be re-runnable against the next version of the packet so that you're now able to version between packet sends with reduced input (i.e. creating targeted diffs). 

**Question, for Vanguard Retail Services:** Your field force roughly doubles every October and collapses on 24 December, and the reps live in a spreadsheet rebuilt each year. Should the seasonal wave become a standing annual motion, with a saved role-to-control mapping and a re-runnable onboarding flow, rather than rebuilt each season?

## What I'd do next with another day

Reconcile the ledger against a live API since this session excludes building out Ramp API calls. An additional exercise that would be interesting to add in to this pipeline would then be seeing how to layer in the expanded supported capabilities into the existing infrastructure (and knowing how to surface changes / updates to the API that are substantive enough for pipeline re-design).