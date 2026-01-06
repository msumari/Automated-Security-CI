import os
import subprocess


def connect_to_database():
    # 1. TRIGGER FOR GITLEAKS (Hardcoded Secret)
    # Gitleaks detects patterns like "AKIA..." which are AWS Access Keys.
    aws_access_key = "XXXX1234567890EXAMPLE"
    aws_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

    print(f"Connecting with {aws_access_key}...")


def ping_website(hostname):
    # 2. TRIGGER FOR SEMGREP (Command Injection)
    # Passing user input directly to a shell command is dangerous.
    # A hacker could send hostname = "google.com; rm -rf /"
    os.system("ping -c 1 " + hostname)


if __name__ == "__main__":
    connect_to_database()
    ping_website("google.com")
