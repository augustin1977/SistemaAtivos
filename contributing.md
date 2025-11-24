# Contribution Guide

Thank you for your interest in contributing to the **Laboratory Asset Control System (SistemaAtivos)** project. By contributing, you agree to license your work under the MIT License.

### 1. How to Report Issues

#### 1.1. Bug Reporting
If you encounter unexpected behavior or an error:
1.  Check if the issue has already been reported in the repository's Issues section.
2.  Open a new Issue describing the error. Include:
    * Steps to reproduce the bug.
    * The expected behavior.
    * The actual (unexpected) behavior.
    * The Python/Django version used.

#### 1.2. Reporting Security Vulnerabilities
If you discover a security flaw, **DO NOT** open a public Issue.
* Follow the **Security Issue Reporting** procedure detailed in the `SECURITY.md` file.
* Send an email directly to `gestaodeativos@outlook.com.br`.

#### 1.3. Feature Suggestions
To suggest new features, open an Issue and describe:
* The need or problem the feature will solve.
* Clear details on how the feature should operate.

### 2. Code Contribution Workflow

We utilize a workflow based on Pull Requests (PR) and mandatory code reviews.

1.  **Fork** the repository to your GitHub account.
2.  **Clone** the forked repository locally.
3.  Create a new branch for your change. Use descriptive names (e.g., `feature/feature-name` or `fix/bug-in-list`).
    ```bash
    git checkout -b feature/your-feature
    ```
4.  Implement your changes to the code.
5.  **Commit** your changes with clear and concise messages.
    ```bash
    git commit -m "feat: Adds data export functionality"
    ```
6.  Push the branch to your forked repository.
    ```bash
    git push origin feature/your-feature
    ```
7.  Open a **Pull Request (PR)** from your branch to the main branch (`main`) of the original repository.

### 3. Code Standards and Quality

* **PEP 8:** Follow the Python code style standards defined in PEP 8.
* **Django:** Adhere to Django framework conventions and ensure templates and views follow best practices.
* **Testing:** It is highly recommended that significant changes include unit and/or integration tests to ensure code stability.
* **Documentation:** Update any relevant documentation (docstrings or comments) affected by your changes.

Your Pull Request will only be considered for merging after passing Continuous Integration (CI) and receiving mandatory approval from one of the project maintainers.