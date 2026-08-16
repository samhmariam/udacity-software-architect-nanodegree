# Smart Home Security System — System Requirements, Design, and Validation

| Document control | Value |
|---|---|
| System | Sentinel Smart Home Security System (SSHSS) |
| Document | System Requirements Specification (SysRS) |
| Standard | ISO/IEC/IEEE 29148:2018, section 9.4 |
| Version | 1.0 |
| Status | Design baseline |
| Verification baseline | All requirements in this document |

## 1. Introduction

### 1.1 Purpose

This SysRS defines a verifiable baseline for a residential security system composed of motion and entry sensors, cameras, an audible alarm, a central control unit (CCU), a mobile application, and an optional cloud notification service. It supports architecture evaluation, implementation, acceptance, and regression testing. “Shall” statements are binding requirements; explanatory text is non-normative.

### 1.2 Scope

SSHSS addresses the need for occupants to detect intrusion, assess an incident, deter an intruder, and receive timely alerts whether at home or away. The system shall monitor configured zones, correlate sensor events, record relevant video, operate an alarm, and permit authorized users to arm, disarm, inspect status, and acknowledge incidents.

The system boundary includes the CCU, enrolled sensors and cameras, siren, local user interface, mobile application, and their security protocols. Internet, household mains, user-owned routers and phones, emergency responders, and third-party notification infrastructure are external.

The baseline supports a single residence. It does not guarantee police response, identify a person using biometrics, extinguish fires, unlock doors automatically, or continuously record unrelated household activity. Its objectives are rapid detection, useful evidence, safe operation during Internet or mains failure, privacy, and simple household operation.

## 2. Overview

### 2.1 System context

[Open the editable SysML system-context model](models/01-context.puml).

The homeowner and household members operate SSHSS locally or through the mobile application. Installers enroll and diagnose devices without receiving routine access to household recordings. Sensors send events to the CCU; cameras send authenticated video; the CCU commands the siren and communicates with the cloud when Internet access exists. The cloud relays alerts to push/SMS providers. Emergency services are contacted by a human; they are not directly controlled by SSHSS.

Trust boundaries exist between field devices and the CCU, the home network and the Internet, and the cloud and user devices. Safety-critical local detection and alarming do not depend on the cloud.

### 2.2 System functions

The major capabilities are device enrollment and supervision, arming and disarming, intrusion detection, entry/exit delay handling, alarm actuation, event-correlated video capture, remote notification and status, local audit logging, health monitoring, and backup-power operation. The functional decomposition appears in [the block model](models/02-block-definition.puml).

### 2.3 User characteristics

| User class | Typical count/site | Location/device | Use and expected skill |
|---|---:|---|---|
| Owner/administrator | 1–2 | Home panel and mobile phone | Configures users/zones; routine consumer skill |
| Resident/household member | 1–8 | Home panel and mobile phone | Arms/disarms and responds to alarms; minimal training |
| Guest | 0–10 | Home panel | Temporary disarm only; no configuration access |
| Installer/maintainer | 1–2 per visit | On-site service interface | Enrollment and diagnostics; technically trained |
| Remote notification provider | 1 service | Cloud API | Machine actor relaying messages |

## 3. Functional requirements

The required functional areas are explicitly covered as follows:

| Functional area | Requirement coverage |
|---|---|
| Motion and other sensor detection | FR-01, FR-04, FR-05, FR-10 |
| Video surveillance and incident recording | FR-08, FR-11, FR-12, FR-16 |
| Alarm system, siren, and notifications | FR-06–FR-09, FR-14 |
| Central Control Unit processing and management | FR-02, FR-04–FR-08, FR-10, FR-13–FR-15 |
| User authentication and authorized operation | FR-03, FR-09, FR-12, FR-16 |

| ID | Requirement | Verification |
|---|---|---|
| FR-01 | The system shall allow an administrator to enroll, name, assign to a zone, test, and remove each supported sensor, camera, and siren. | Test |
| FR-02 | The system shall provide Disarmed, Armed-Stay, and Armed-Away modes and shall permit a configured exit delay of 0–120 s in 5 s increments. | Test |
| FR-03 | The system shall accept disarm commands only after authenticating an authorized user by PIN or mobile credential. | Test/analysis |
| FR-04 | In Armed-Away, the CCU shall treat an authenticated event from any enabled perimeter or interior intrusion sensor as an intrusion candidate. | Test |
| FR-05 | In Armed-Stay, the CCU shall treat enabled perimeter events as intrusion candidates and shall ignore interior zones configured as Stay-bypassed. | Test |
| FR-06 | For an instant zone intrusion candidate, the CCU shall enter Alarm and command the siren without an entry delay. | Test |
| FR-07 | For a delayed-entry zone intrusion candidate, the CCU shall start the configured 0–120 s entry delay and enter Alarm if not disarmed before expiry. | Test |
| FR-08 | On entering Alarm, the CCU shall command the siren, create a timestamped incident record, request clips from associated cameras, and queue alerts for all configured recipients. | Test |
| FR-09 | The system shall allow an authenticated owner to silence and acknowledge an alarm while retaining its incident record. | Demonstration/test |
| FR-10 | The CCU shall supervise enrolled devices and report loss of heartbeat, low battery, tamper, storage fault, mains loss, and communication failure. | Fault-injection test |
| FR-11 | A camera associated with an intrusion zone shall preserve video from at least 10 s before through at least 30 s after the triggering event when configured for event recording. | Test |
| FR-12 | The mobile application shall display mode, active alarms, device health, and the timestamp of the most recent successful CCU synchronization. | Demonstration/test |
| FR-13 | The CCU shall continue local sensing, entry/exit timing, alarming, and audit logging when Internet connectivity is unavailable. | Fault-injection test |
| FR-14 | When connectivity returns, the CCU shall transmit queued alarm notifications and metadata in chronological order, marking them as delayed. | Test |
| FR-15 | The system shall record arming, disarming, alarm, acknowledgement, configuration, authentication-failure, device-health, and administrative-access events in an append-evident audit log. | Inspection/test |
| FR-16 | The system shall allow an owner to export or delete recordings and account data subject to the retention and audit constraints in IM-01–IM-04. | Test |

## 4. Usability requirements

| ID | Requirement | Verification |
|---|---|---|
| UR-01 | At least 90% of first-time adult participants shall arm Away and subsequently disarm the system without assistance within 60 s after a five-minute orientation (n ≥ 20). | Usability test |
| UR-02 | The local interface shall display the current mode and any blocking fault from 1 m under 100–500 lux lighting, correctly identified by at least 95% of participants (n ≥ 20). | Usability test |
| UR-03 | An alarm notification shall identify the residence, affected zone, event time, and available response actions on one mobile screen. | Inspection/test |
| UR-04 | A user shall be able to silence an alarm in no more than three interactions after successful authentication. | Demonstration |
| UR-05 | The mobile interface shall meet WCAG 2.2 AA for contrast, text resizing, screen-reader labels, keyboard navigation, and non-color status cues. | Analysis/test |

## 5. Performance requirements

| ID | Requirement | Verification |
|---|---|---|
| PR-01 | For 99% of valid local sensor events, the CCU shall register the event within 500 ms of sensor transmission under the nominal load in PR-05. | Instrumented test |
| PR-02 | The siren shall begin producing sound within 1.0 s after the CCU enters Alarm. | Instrumented test |
| PR-03 | When the Internet and provider are available, 95% of alarm alerts shall be submitted to the external notification provider within 5 s of Alarm entry. | Load test |
| PR-04 | The siren shall produce at least 85 dBA at 3 m for at least 4 min unless silenced, while respecting applicable local sound limits. | Measurement/test |
| PR-05 | The CCU shall support at least 32 sensors, 8 cameras, 2 sirens, 10 users, and 5 simultaneous mobile sessions without violating PR-01–PR-03. | Load test |
| PR-06 | On loss of mains power, the CCU and one siren shall retain the functions in FR-13 for at least 12 h at 25 °C, assuming no more than 15 min total siren activity and cameras on their specified supplies. | Endurance test |
| PR-07 | The CCU shall reach operational monitoring within 60 s of a cold start and restore its last safe persistent configuration. | Test |
| PR-08 | The product design life shall be at least 5 years, excluding replaceable batteries, under the environment in ENV-01. | Analysis/inspection |

## 6. System interfaces

| ID | Interface requirement | Verification |
|---|---|---|
| IF-01 | Field-device messages shall use authenticated encryption and include device identity, monotonically increasing counter, event type, battery state, and integrity protection. | Inspection/penetration test |
| IF-02 | CCU–cloud communication shall use TLS 1.3 or a maintained successor with server authentication and certificate validation. | Inspection/test |
| IF-03 | Mobile–service requests shall use a versioned HTTPS API, OAuth 2.1/OIDC authorization, and a documented JSON schema; incompatible requests shall fail closed with an actionable error. | Contract/security test |
| IF-04 | The local interface shall provide visual mode/fault indication, an audible entry/exit indication, and authenticated controls for arm, disarm, silence, and emergency alarm. | Demonstration |
| IF-05 | Loss, corruption, duplication, or reordering at an external interface shall not cause an unauthorized state change or suppress an existing alarm. | Robustness test |
| IF-06 | All externally visible timestamps shall use ISO 8601 with UTC offset; internal event ordering shall use UTC and a monotonic clock where elapsed time matters. | Inspection/test |

The logical connections and item flows are defined in [the internal block diagram](models/03-internal-block.puml).

## 7. System operations

### 7.1 Human-system integration

| ID | Requirement | Verification |
|---|---|---|
| HS-01 | Local disarm shall remain available during Internet outage and shall not require a personal mobile device. | Test |
| HS-02 | Configuration changes affecting zone behavior, recipients, credentials, retention, or alarm timing shall require administrator authorization and an explicit confirmation. | Test |
| HS-03 | Installer access shall be time-limited, revocable, logged, and unable to view recordings unless an owner grants explicit, temporary permission. | Security test |
| HS-04 | The interface shall distinguish intrusion alarm, device trouble, and connectivity warning by text and signal pattern to reduce dangerous operator confusion. | Usability test |

### 7.2 Maintainability

| ID | Requirement | Verification |
|---|---|---|
| MA-01 | A trained installer shall replace an enrolled sensor and restore its zone configuration in 15 min or less using no special tools beyond a screwdriver and mobile service device. | Maintenance demonstration |
| MA-02 | The CCU shall expose self-test results and diagnostic logs sufficient to isolate a failed field-replaceable unit in 10 min or less for 90% of seeded single faults. | Maintainability test |
| MA-03 | Signed software updates shall support automatic rollback after failed health checks and shall not erase configuration, audit logs, or retained incidents. | Fault-injection test |
| MA-04 | Batteries and other planned replacement items shall be accessible without exposing mains terminals or resetting device identity. | Inspection/demonstration |

### 7.3 Reliability

| ID | Requirement | Verification |
|---|---|---|
| RE-01 | Excluding planned maintenance and external utilities, the CCU shall achieve 99.9% monthly availability for local monitoring. | Reliability analysis/field data |
| RE-02 | No single loss of cloud, Internet, router, mobile phone, or individual camera shall prevent local intrusion detection and siren activation by an otherwise healthy sensor and CCU. | Fault-tree analysis/test |
| RE-03 | The system shall detect an enrolled device communication loss within 5 min and notify a local user within 1 additional min. | Test |
| RE-04 | After unexpected power interruption, persistent configuration and audit records shall be internally consistent with no acknowledged record reported as successfully stored being lost. | Recovery test |

## 8. System modes and states

SSHSS states are **Disarmed**, **Exit Delay**, **Armed Stay**, **Armed Away**, **Entry Delay**, **Alarm**, and **Fault/Degraded**. Degraded is an orthogonal health condition: the system continues available safe functions and reports unavailable ones. Alarm has priority over ordinary arm/disarm transitions; authenticated disarm terminates active alarming but does not delete evidence.

The normative transitions, guards, and actions appear in [the state machine](models/04-state-machine.puml). A representative alarm interaction appears in [the sequence model](models/05-alarm-sequence.puml).

### 8.1 Physical requirements

| ID | Requirement | Verification |
|---|---|---|
| PH-01 | The indoor CCU enclosure shall not exceed 250 × 200 × 80 mm or 2 kg including its backup battery. | Inspection/measurement |
| PH-02 | Wall-mounted components shall include secure mounting points and tamper detection when removal could disable protection. | Inspection/test |
| PH-03 | User-replaceable components shall carry durable model, electrical rating, battery polarity/type, and regulatory markings. | Inspection |

### 8.2 Adaptability requirements

| ID | Requirement | Verification |
|---|---|---|
| AD-01 | New supported device types shall be addable through versioned device profiles without changing existing profile semantics. | Architecture analysis/contract test |
| AD-02 | The software architecture shall permit capacity to increase to 64 sensors and 16 cameras without changing user or event data schemas. | Analysis/prototype test |
| AD-03 | Optional cloud unavailability or subscription termination shall not disable locally licensed capabilities or access to locally stored user data. | Test |

### 8.3 Environmental conditions

| ID | Requirement | Verification |
|---|---|---|
| ENV-01 | Indoor components shall operate at 0–40 °C, 10–90% RH non-condensing, and storage temperature of −20–60 °C. | Environmental test |
| ENV-02 | Outdoor cameras shall meet at least IP65 and operate at −20–50 °C unless explicitly sold for a narrower marked climate. | Certification/test |
| ENV-03 | The system shall meet applicable residential EMC, electrical safety, radio, battery transport, and acoustic regulations in each market where sold. | Certification/inspection |
| ENV-04 | A 10-second interruption or brownout of mains power shall not reset configuration or create an unauthorized disarm transition. | Power-disturbance test |

### 8.4 System security

| ID | Requirement | Verification |
|---|---|---|
| SEC-01 | The system shall enforce least-privilege roles for administrator, member, guest, installer, and service identities. | Access-control test |
| SEC-02 | Remote administrator authentication shall require multi-factor authentication; five failed local PIN attempts in 10 min shall impose a rate-limited lockout while preserving emergency functions. | Security test |
| SEC-03 | Recordings, credentials, configuration, and audit data shall be encrypted at rest using platform-protected keys and in transit using maintained authenticated cryptography. | Inspection/penetration test |
| SEC-04 | Each CCU and field device shall have a unique identity; default shared credentials shall not be used; enrollment shall require physical presence or an equivalent authenticated proof of possession. | Inspection/test |
| SEC-05 | The CCU shall accept only vendor-authorized, integrity-checked firmware and shall reject rollback to known-vulnerable versions unless an authenticated recovery procedure explicitly permits it. | Security test |
| SEC-06 | Security-relevant events shall be timestamped, append-evident, access-controlled, and exportable for incident review. | Inspection/test |
| SEC-07 | A factory reset shall require local physical action, visibly warn the user, revoke credentials/keys, and cryptographically erase locally stored personal data. | Test |
| SEC-08 | The system shall fail secure on malformed, replayed, expired, or unauthenticated commands and shall raise a security event after repeated attacks. | Fuzz/penetration test |
| SEC-09 | The design shall support signed security updates for at least 5 years after the model’s final sale date. | Supplier evidence/inspection |

### 8.5 Information management

| ID | Requirement | Verification |
|---|---|---|
| IM-01 | The owner shall be able to configure event-video retention from 1–30 days; the default shall be 7 days. | Test |
| IM-02 | Expired recordings shall be deleted within 24 h unless preserved by an explicit owner hold; holds shall be visible and revocable. | Test |
| IM-03 | The CCU shall retain at least 10,000 audit events and use bounded rotation that preserves the newest events and any protected incident. | Capacity test |
| IM-04 | Account deletion shall revoke access immediately and delete personal cloud data within 30 days, except documented legal or fraud-prevention records. | Process audit/test |
| IM-05 | Video shall not leave the residence except for an owner-enabled feature, incident access, or export; purpose and destination shall be disclosed before enablement. | Inspection/test |

### 8.6 Policies and regulations

| ID | Requirement | Verification |
|---|---|---|
| REG-01 | Deployment shall provide privacy notice, consent controls, data export/deletion, and data-minimization features needed to support applicable data-protection law, including UK GDPR where deployed in the UK. | Legal review/inspection |
| REG-02 | Installation guidance shall require users to position cameras and audible alarms consistently with local privacy, surveillance, tenancy, and noise rules. | Documentation inspection |
| REG-03 | Product safety and compliance evidence shall be retained for the applicable statutory period and mapped to the exact hardware/firmware release. | Compliance audit |

### 8.7 System life-cycle sustainment

| ID | Requirement | Verification |
|---|---|---|
| LC-01 | Each release shall maintain bidirectional traceability from stakeholder need to system requirement, design element, risk control, and verification result. | Audit |
| LC-02 | The supplier shall publish installation, operation, privacy, recovery, maintenance, and end-of-support documentation for each supported release. | Inspection |
| LC-03 | Vulnerability reports shall be acknowledged within 2 business days, triaged within 5 business days, and critical remediations targeted within 30 days or accompanied by a documented mitigation. | Process audit |

### 8.8 Packaging, handling, shipping, and transportation

| ID | Requirement | Verification |
|---|---|---|
| PK-01 | Packaging shall prevent functional or cosmetic damage during the applicable distribution vibration and drop profile and shall protect battery terminals against short circuit. | Packaging test |
| PK-02 | Lithium batteries shall be shipped, marked, and documented in accordance with applicable transport rules and verified test summaries. | Compliance inspection |

## 9. Architecture and tradeoff evaluation

### 9.1 Selected architecture

SSHSS uses a **local-first hub architecture**. The CCU owns the authoritative security state machine, executes detection rules, stores a bounded local event log, activates the siren directly, and queues cloud work. The cloud provides remote reachability and notification but is not in the critical path for local protection. Field devices communicate through a replaceable device-adapter boundary; domain logic consumes normalized events rather than radio-specific packets.

### 9.2 Decision matrix

Scores use 1 (poor) to 5 (excellent); weighted totals are out of 5.

| Criterion | Weight | Cloud-centric | Local-only | Local-first hybrid |
|---|---:|---:|---:|---:|
| Works during Internet outage | 0.25 | 1 | 5 | 5 |
| Detection/alarm latency | 0.20 | 2 | 5 | 5 |
| Privacy/data minimization | 0.15 | 2 | 5 | 4 |
| Remote access | 0.15 | 5 | 1 | 5 |
| Operational simplicity | 0.10 | 3 | 4 | 3 |
| Extensibility/analytics | 0.10 | 5 | 2 | 4 |
| Recurring cost | 0.05 | 2 | 5 | 3 |
| **Weighted total** | **1.00** | **2.55** | **4.15** | **4.55** |

The hybrid option is selected because it combines local resilience and low latency with remote access. Its extra synchronization and update complexity is controlled through a single CCU authority, idempotent cloud messages, bounded queues, explicit timestamps, and versioned interfaces.

Additional decisions:

| Decision | Selected option | Rejected alternative | Rationale/consequence |
|---|---|---|---|
| Event recording | Pre-buffered event clips | Continuous cloud recording | Reduces privacy/bandwidth while preserving incident context; may miss unrelated events |
| Device integration | Adapter/profile layer | Radio logic in alarm engine | Supports evolution and test doubles; requires profile conformance tests |
| Alarm evaluation | Deterministic CCU state machine | ML-only classification | Explainable, testable safety behavior; optional analytics may advise but cannot suppress a valid alarm |
| Availability | Graceful degradation | All-or-nothing shutdown | A failed camera/cloud does not remove local detection; UI must clearly expose degraded coverage |

### 9.3 Safety and security risk controls

| Risk | Initial risk | Control(s) | Residual validation |
|---|---|---|---|
| Intrusion not detected due to Internet failure | High | FR-13, RE-02, local state authority | TC-06 |
| Unauthorized disarm/replayed command | High | FR-03, SEC-02, SEC-04, SEC-08 | TC-09, penetration test |
| False alarm causes distress/noise | Medium | Entry delay, clear zone identity, authenticated silence, supervised health | TC-03/TC-04, usability test |
| Private video disclosed | High | SEC-01/03, IM-01/02/05, installer restriction | Access and retention tests |
| Update bricks CCU | High | MA-03, signed image and rollback | TC-10 |
| Battery failure creates hidden loss of protection | High | FR-10, RE-03, PR-06 | TC-07/TC-08 |

## 10. Verification and validation plan

### 10.1 Strategy and independence

Verification answers whether the system conforms to this SysRS through inspection (I), analysis (A), demonstration (D), and test (T). Validation answers whether representative occupants can protect a realistic residence safely and effectively. Test configuration, firmware, device inventory, network conditions, timestamps, actual results, anomalies, and evidence hashes shall be recorded. Security tests use an isolated environment and authorized scope.

Entry criteria: approved requirements baseline; reviewed design; traceable build; calibrated instruments; representative production hardware; safety and privacy review complete. Exit criteria: every requirement has objective evidence; all safety/security-critical tests pass; no open severity-1/2 defect; lower-severity deviations have an owner and approved disposition; validation acceptance criteria pass.

### 10.2 System verification procedures

| Test ID | Procedure summary | Requirements | Pass criterion |
|---|---|---|---|
| TC-01 | Enroll maximum supported mix; name, zone, test, remove, and re-enroll one of each device type. | FR-01, PR-05 | All operations persist; limits supported; no latency breach |
| TC-02 | Arm Stay/Away with boundary delay values; trigger bypassed interior and enabled perimeter zones. | FR-02, FR-04, FR-05 | Exact state/zone behavior matches requirements |
| TC-03 | Trigger instant zone and instrument Alarm-entry-to-siren interval over 100 trials. | FR-06, FR-08, PR-02, PR-04 | All alarms occur; ≤1.0 s; sound/endurance limit met |
| TC-04 | Trigger delayed-entry zone; disarm before expiry, then repeat without disarming. | FR-03, FR-07, FR-09 | First case no alarm; second alarms at configured expiry; record retained |
| TC-05 | Trigger associated camera with known timecode and inspect stored clip and alert fields. | FR-08, FR-11, UR-03 | ≥10 s pre-event and ≥30 s post-event; required metadata present |
| TC-06 | Disconnect WAN during Armed Away, trigger alarm, restore WAN, and inspect queue ordering. | FR-13, FR-14, HS-01, RE-02 | Local functions continue; delayed alert is ordered and labelled |
| TC-07 | Inject heartbeat loss, low battery, tamper, storage, mains, and network faults. | FR-10, RE-03 | Each detected and locally reported within specified time |
| TC-08 | Run representative load on backup supply at 25 °C including 15 min alarm activity. | PR-06, ENV-04 | Required functions operate ≥12 h; no unauthorized disarm/data loss |
| TC-09 | Attempt wrong PINs, privilege escalation, replay, malformed frames, expired tokens, and unauthorized data access. | IF-01/03/05, SEC-01–04, SEC-08 | All attempts fail securely, lockout/rate limits and logs operate |
| TC-10 | Interrupt update at each phase and supply invalid, old-vulnerable, and unsigned images. | MA-03, SEC-05, RE-04 | Rollback succeeds; invalid images rejected; retained data consistent |
| TC-11 | Fill event/audit storage, expire recordings, apply/revoke hold, export, delete account, factory-reset. | FR-15/16, SEC-06/07, IM-01–04 | Bounded/ordered retention and deletion criteria all met |
| TC-12 | Cold-start 30 times with max configuration and record readiness time. | PR-07 | Every run ≤60 s and restores last safe configuration |

### 10.3 Validation activities

| Validation ID | Representative scenario | Stakeholders | Acceptance criterion |
|---|---|---|---|
| VAL-01 | First-day setup, arm, leave, return, and disarm in a furnished test home | 20 first-time adults, including assistive-tech users | UR-01, UR-02, and UR-05 pass; no critical use error |
| VAL-02 | Simulated night intrusion while Internet is unavailable; occupant interprets, silences, and reviews incident | Owner/member cohort | ≥90% choose an appropriate action without facilitator help; local alarm/evidence succeeds |
| VAL-03 | Week-long pilot with routine arrivals, pets, guests, mains loss, and one injected device failure | ≥5 households | All real/injected events explainable; no unreported loss of coverage; satisfaction ≥4/5 |
| VAL-04 | Installer replaces a failed device and performs diagnostics without routine video permission | 5 trained installers | MA-01/02 and HS-03 pass; configuration and privacy preserved |

### 10.4 Requirements traceability

[The requirements model](models/06-requirements.puml) shows key need-to-requirement-to-test relationships. The tables above provide the complete verification mapping. Every normative requirement has a stated verification method; combined tests may provide evidence for several requirements, while certification, audit, analysis, inspection, and usability evidence are recorded as separate verification records under their requirement IDs.

Critical chain examples:

| User need | System requirements | Design allocation | Evidence |
|---|---|---|---|
| Detect and deter intrusion quickly | FR-04–08, PR-01/02/04 | Sensor adapter, alarm engine, siren | TC-02–TC-04 |
| Remain protective offline | FR-13/14, RE-02, PR-06 | Local CCU authority, durable queue, battery | TC-06, TC-08 |
| Protect household privacy | SEC-01–08, IM-01–05, HS-03 | IAM, encryption, local store, audit | TC-09, TC-11, VAL-04 |
| Be understandable and recoverable | UR-01–05, MA-01–04 | Panel/app UX, diagnostics/update manager | VAL-01–04, TC-10 |

## 11. Assumptions and dependencies

| ID | Assumption/dependency | Impact and treatment |
|---|---|---|
| AS-01 | The residence has compliant mains power and, for remote features, a user-managed IP connection. | Local security remains available without Internet; mains loss invokes backup power. |
| AS-02 | Sensors are placed and tested according to installation guidance; radio range is site-dependent. | Commissioning requires a walk test; poor placement is reported as a fault/coverage issue. |
| AS-03 | User phones and third-party push/SMS services may be delayed or unavailable. | PR-03 measures submission, not handset display; local alarm remains authoritative. |
| AS-04 | Emergency-service response is outside the system boundary. | Alerts clearly require human assessment/action; no response-time claim is made. |
| AS-05 | Applicable regulations depend on sales and installation jurisdiction. | Market release requires jurisdiction-specific compliance evidence under ENV-03 and REG-01–03. |
| DP-01 | Cryptographic libraries, mobile operating systems, cloud hosting, time synchronization, and notification providers are maintained dependencies. | Maintain SBOM, vulnerability monitoring, compatibility tests, and replacement plans. |
| DP-02 | Event pre-roll depends on powered cameras with adequate local buffer and storage. | Health supervision exposes unavailable recording; detection/siren do not depend on video. |

## Appendix A — Model index and rendering

The editable `.puml` files use SysML-style blocks, requirements, item flows, allocation, state-machine, and interaction notation supported by PlantUML. Render all diagrams with a local PlantUML installation:

```bash
plantuml models/*.puml
```

| Model | Purpose |
|---|---|
| [01-context.puml](models/01-context.puml) | System boundary, actors, and external interfaces |
| [02-block-definition.puml](models/02-block-definition.puml) | Composition and allocation of responsibilities |
| [03-internal-block.puml](models/03-internal-block.puml) | Internal connections and information flows |
| [04-state-machine.puml](models/04-state-machine.puml) | Modes, guards, and state transitions |
| [05-alarm-sequence.puml](models/05-alarm-sequence.puml) | End-to-end alarm scenario |
| [06-requirements.puml](models/06-requirements.puml) | Selected requirement derivation, satisfaction, and verification |
| [07-use-cases.puml](models/07-use-cases.puml) | Actors, system use cases, and include/extend relationships |
| [smart-home-architecture.drawio](diagrams/smart-home-architecture.drawio) | Editable deployment/component architecture for diagrams.net |
| [decision-matrices.xlsx](decision-matrices.xlsx) | Weighted tradeoff matrices for sensors, cameras, controllers, and server/manager |
| [test-cases-export_completed.xlsx](test-cases-export_completed.xlsx) | Completed verification and validation test suites with requirement traceability |

## Appendix B — Glossary

| Term | Definition |
|---|---|
| CCU | Central Control Unit; authoritative local controller |
| Incident | Correlated alarm event, metadata, audit entries, and available media |
| Intrusion candidate | Sensor event evaluated according to current mode and zone policy |
| Local-first | Critical monitoring and alarm decisions execute at the residence |
| Zone | Named logical grouping with entry/instant/interior/perimeter behavior |
