| ID    | Description                                                                                                                                                                                   |
| ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| LLM01 | `Prompt Injection`: Attackers manipulate the LLM's input directly or indirectly to cause malicious or illegal behaviour.                                                                      |
| LLM02 | `Sensitive Information Disclosure`: Attackers trick the LLM into revealing sensitive information in the response.                                                                             |
| LLM03 | `Supply Chain`: Attackers exploit vulnerabilities in any part of the LLM supply chain.                                                                                                        |
| LLM04 | `Data and Model Poisoning`: Attackers inject malicious or misleading data into the LLM's training data, compromising performance or creating backdoors.                                       |
| LLM05 | `Improper Output Handling`: LLM Output is handled insecurely, resulting in injection vulnerabilities such as Cross-Site Scripting (XSS), SQL Injection, or Command Injection.                 |
| LLM06 | `Excessive Agency`: Attackers exploit insufficiently restricted LLM access.                                                                                                                   |
| LLM07 | `System Prompt Leakage`: Attackers trick the LLM into revealing system instructions, potentially enabling more advanced attack vectors.                                                       |
| LLM08 | `Vector and Embedding Weaknesses`: Attackers exploit vulnerabilities related to the handling or storage of vectors and embeddings in `Retrieval-Augmented Generation (RAG)` LLM applications. |
| LLM09 | `Misinformation`: LLM-generated responses contain misinformation, potentially resulting in security issues.                                                                                   |
| LLM10 | `Unbounded Consumption`: Attackers feed inputs to the LLM that result in high resource consumption, potentially causing disruptions to the LLM service or high costs.                         |

---

Prompt Injection > Leak System Prompt > https://itsbroken.ai/cheatsheet/