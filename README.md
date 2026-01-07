# DevSecOps Pipeline Documentation
This repository implements a secure software supply chain for a Python codebase managed by uv. It enforces security checks at the local commit stage and the Continuous Integration (CI) stage to prevent secrets and vulnerabilities from entering the version control history.

## Architecture Overview
The security pipeline consists of three distinct layers:

**Pre-commit (Local):** Blocks secrets from being committed to the local git history.

**Secret Scanning (CI):** Audits the entire commit history and new pushes for secrets using Gitleaks.

**SAST (CI):** Performs Static Application Security Testing using Semgrep to detect vulnerability patterns (e.g., Command Injection) and reports results via SARIF.

**SCA (Automated):** Monitors dependencies for known CVEs using Dependabot.

## 1. Local Development Setup
To contribute to this repository, the security hooks must be installed locally.

### Prerequisites
* Python 3.12+
* `uv` (Dependency Manager)
* `pre-commit`

### Installation
1. Clone the repository.
2. Install the pre-commit hook:

``` bash
pip install pre-commit
pre-commit install
```

### Troubleshooting: "Cowardly refusing to install hooks"
If `pre-commit install` fails with a `core.hooksPath` error, it indicates a conflict with a `global git` configuration (often caused by Husky or global templates).

**Resolution:**

```bash
# Clear the conflicting global setting
git config --global --unset-all core.hooksPath

# Re-run installation
pre-commit install
```

## 2. CI Pipeline Configuration
The CI pipelines are defined in .github/workflows/ and utilize SHA pinning for security resilience.

### A. Secret Scanning
Tool: [Gitleaks](https://gitleaks.io/)

Trigger: Push and Pull Request.

**Key Configuration:**

`fetch-depth: 0`: Forces a full git history download. This allows Gitleaks to scan not just the current file state, but the entire history of the branch to catch secrets hidden in previous commits.

### B. Static Analysis
Tool: [Semgrep](https://semgrep.dev/)

Trigger: Push and Pull Request.

**Execution Method:**

The job runs on `ubuntu-latest` but executes Semgrep via a direct docker run command rather than a container: job block.

**Reason:** The official Semgrep Docker image is Alpine-based and lacks Node.js. The upload-sarif action requires Node.js. Running docker run allows the scan to happen in the container while the upload step happens in the standard runner environment.

**Rule Configuration:**

`--config="p/default"`: Uses the strict default ruleset rather than auto. This ensures script files and explicit command injections are caught.

`--error`: Forces the process to exit with Code 1 if vulnerabilities are found (ensuring the build fails).

`--sarif`: Outputs findings to a standard format for GitHub integration.

**Reporting:**

Results are uploaded to the GitHub Security tab.

Pull Requests receive inline annotations on vulnerable lines.

### C. Dependency Management

**Schedule:** Weekly.

**Ecosystem:** pip.

**Behavior:** Scans **pyproject.toml/requirements.txt** against the GitHub Advisory Database and opens PRs for vulnerable versions.

## 3. Security Policies & Enforcement
**Testing the Pipeline:**
To verify the scanners are working, do not commit sensitive data. Instead, use specific "Tainted" patterns that trigger the rules engines:

**Trigger Gitleaks:**

Commit a string matching a high-entropy pattern, e.g., an AWS key format (without the "EXAMPLE" suffix).

`AKIA + 16 random characters`.

**Trigger Semgrep:**

 Passing `sys.argv` (Source) directly into `subprocess.call(..., shell=True)`.

### SHA Pinning
All GitHub Actions in this repository are pinned to specific commit hashes (SHAs) rather than mutable tags (e.g., @v4).

**Purpose:** Prevents supply chain attacks where a malicious actor compromises an Action's tag to inject code into our CI.

**Maintenance:** Updates are managed by manually verifying the SHA of new releases.
