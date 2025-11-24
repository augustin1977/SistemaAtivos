# Security Policy for the Sistema de Ativos Project

## Objective
Protect the project's source code, data, and infrastructure against vulnerabilities, unauthorized access, and attacks, ensuring the integrity, confidentiality, and availability of assets.

## Security and Development Practices

### Access and Authentication
* **Principle of Least Privilege:** Access to the GitHub repository and other project resources must be restricted to the principle of least privilege. Access granting is the responsibility of the repository maintainer (owner).
* **Mandatory Authentication:** The use of Two-Factor Authentication (2FA) is mandatory for all collaborators on GitHub and any related infrastructure services.
* **Secure Credentials:** Strong passwords must be used and managed, preferably via a password manager. No credentials should be stored in plain text within the source code or configuration files.

### Code Management (GitHub Flow)
* **Branch Protection:** The main branch (e.g., main) must be protected (Branch Protection Rules), requiring at least:
    * Code review (minimum 1 approval).
    * Successful Continuous Integration (CI) tests.
* **Code Review:** All code changes must be submitted via Pull Request (PR) and reviewed by at least one other collaborator before merging.
* **Vulnerability Analysis:** Static Application Security Testing (SAST) and/or Software Composition Analysis (SCA) tools must be integrated into the CI process to verify vulnerabilities before merging.

### Data and Infrastructure
* **Data Encryption:** Sensitive data and personally identifiable information (PII) must be encrypted at rest (storage) and in transit (SSL/TLS connections).
* **Production Environment:** The production environment must be segregated, monitored, and accessible only through secure channels (VPN, SSH with keys, etc.).
* **Dependencies:** All external dependencies and libraries must be kept up-to-date. Known vulnerabilities in dependencies must be remediated within 7 days of disclosure.

## Reporting Security Issues

* **Responsible Communication:** Any discovered vulnerabilities or security flaws must be reported immediately and discreetly to the repository maintainer.
* **Contact Point:** Reports should be sent via email to: `gestaodeativos@outlook.com.br`.
* **Response:** The maintainer must acknowledge receipt of the report within 24 hours and begin the remediation process as quickly as possible.

## Policy Review
This policy will be reviewed annually, or after significant security events, to ensure its continued relevance and effectiveness against current threats.