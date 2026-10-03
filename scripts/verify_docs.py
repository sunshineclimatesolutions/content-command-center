#!/usr/bin/env python3
"""Zero-dependency verification for Content Command Center documentation.

Stage 0 checks (no third-party imports):

1. Required Stage 0 files exist.
2. Relative Markdown links resolve to files in the repository.
3. Requirement IDs CCC-REQ-001..CCC-REQ-035 exist in docs/PRODUCT_CHARTER.md
   and are referenced by docs/ACCEPTANCE_TESTS.md.
4. No media, database, environment, or credential-like files are present in the
   repository working tree.
5. A conservative secret-pattern scan of text files (tokens/keys/passwords).

Usage:  python scripts/verify_docs.py
Exit code 0 = all checks passed; 1 = at least one error.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    ".gitignore",
    "LICENSE_DECISION.md",
    "docs/PRODUCT_CHARTER.md",
    "docs/USER_WORKFLOWS.md",
    "docs/ARCHITECTURE.md",
    "docs/DATA_MODEL.md",
    "docs/OPEN_SOURCE_EVALUATION.md",
    "docs/PLATFORM_CAPABILITIES.md",
    "docs/THREAT_MODEL.md",
    "docs/NO_COST_POLICY.md",
    "docs/ROADMAP.md",
    "docs/ACCEPTANCE_TESTS.md",
    "docs/DECISION_LOG.md",
    "docs/SOURCE_EVIDENCE.md",
    "docs/STAGE_0_REVIEW_CHECKLIST.md",
    "scripts/verify_docs.py",
]

REQ_COUNT = 35

SKIP_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

TEXT_EXTENSIONS = {
    ".md",
    ".markdown",
    ".txt",
    ".py",
    ".json",
    ".yml",
    ".yaml",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".toml",
    ".cfg",
    ".ini",
    ".ps1",
    ".sh",
}

FORBIDDEN_EXTENSIONS = {
    ".env",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".lic",
    ".key",
    ".pem",
    ".pfx",
    ".p12",
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".webm",
    ".wav",
    ".mp3",
    ".m4a",
    ".flac",
    ".srt",
    ".vtt",
    ".jpg",
    ".jpeg",
    ".png",
    ".heic",
    ".dng",
    ".tif",
    ".tiff",
    ".psd",
    ".drp",
    ".braw",
}

SECRET_PATTERNS = [
    (re.compile(r"ghp_[A-Za-z0-9]{30,}"), "GitHub personal access token"),
    (re.compile(r"gho_[A-Za-z0-9]{30,}"), "GitHub OAuth token"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "GitHub fine-grained token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key block"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"(?i)\b(password|passwd|secret|api[_-]?key)\s*[:=]\s*['\"][^'\"]{8,}['\"]"), "inline credential assignment"),
]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def warn(message: str) -> None:
    print(f"WARN:  {message}")


def iter_files() -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            files.append(Path(dirpath) / name)
    return files


def check_required_files() -> int:
    errors = 0
    for rel in REQUIRED_FILES:
        if not (REPO_ROOT / rel).is_file():
            fail(f"missing required file: {rel}")
            errors += 1
    return errors


def check_links() -> int:
    errors = 0
    for md in REPO_ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in md.parts):
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            candidate = (md.parent / target).resolve()
            try:
                candidate.relative_to(REPO_ROOT.resolve())
            except ValueError:
                fail(f"{md.relative_to(REPO_ROOT)}: link escapes repo: {target}")
                errors += 1
                continue
            if not candidate.exists():
                fail(f"{md.relative_to(REPO_ROOT)}: broken link: {target}")
                errors += 1
    return errors


def check_requirement_ids() -> int:
    errors = 0
    charter = (REPO_ROOT / "docs/PRODUCT_CHARTER.md").read_text(encoding="utf-8")
    acceptance = (REPO_ROOT / "docs/ACCEPTANCE_TESTS.md").read_text(encoding="utf-8")
    for number in range(1, REQ_COUNT + 1):
        req_id = f"CCC-REQ-{number:03d}"
        if req_id not in charter:
            fail(f"requirement {req_id} missing from docs/PRODUCT_CHARTER.md")
            errors += 1
        if req_id not in acceptance:
            fail(f"requirement {req_id} missing from docs/ACCEPTANCE_TESTS.md")
            errors += 1
    return errors


def check_forbidden_files() -> int:
    errors = 0
    for path in iter_files():
        suffix = path.suffix.lower()
        if suffix in FORBIDDEN_EXTENSIONS:
            fail(f"forbidden file type in repo: {path.relative_to(REPO_ROOT)}")
            errors += 1
        if path.name.startswith(".env") and path.name != ".env.example":
            fail(f"environment file in repo: {path.relative_to(REPO_ROOT)}")
            errors += 1
    return errors


def check_secret_patterns() -> int:
    errors = 0
    for path in iter_files():
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name != ".gitignore":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, label in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                snippet = match.group(0)[:40]
                fail(
                    f"possible {label} in {path.relative_to(REPO_ROOT)}:"
                    f" {snippet!r}"
                )
                errors += 1
    return errors


def check_status_honesty() -> int:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    if "Stage 0 documentation only" not in readme:
        warn("README does not contain the expected current-status honesty marker")
    return 0


def main() -> int:
    print("Content Command Center - documentation verification")
    print(f"Repository root: {REPO_ROOT}")
    total = 0
    print("\n[1/6] Required files")
    total += check_required_files()
    print("\n[2/6] Relative Markdown links")
    total += check_links()
    print("\n[3/6] Requirement ID mapping")
    total += check_requirement_ids()
    print("\n[4/6] Forbidden file types")
    total += check_forbidden_files()
    print("\n[5/6] Secret pattern scan")
    total += check_secret_patterns()
    print("\n[6/6] Status honesty marker")
    total += check_status_honesty()
    print()
    if total:
        print(f"FAILED: {total} problem(s) found.")
        return 1
    print("OK: all Stage 0 documentation checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
