#!/usr/bin/env python3
"""Zero-dependency verification for Content Command Center documentation.

Checks (no third-party imports):

1. Required project files exist.
2. Relative Markdown links resolve to files in the repository.
3. Relative anchor links resolve to real headings (GitHub-style slugs).
4. Requirement IDs are unique in the charter and the acceptance-test mapping covers
   exactly the charter's requirement set (no missing, no orphan mappings).
5. The CURRENT-STAGE status marker exists in README.md and docs/ROADMAP.md, uses an
   allowed stage token, and matches between the two files (stale status is an error).
6. Every docs/*.md file is linked from README.md (no orphan documents).
7. No media, database, environment, or credential-like files are present.
8. Conservative secret-pattern scan of text files.

Usage:  python scripts/verify_docs.py
Exit code 0 = all checks passed; 1 = at least one error.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

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
    "docs/ENVIRONMENT.md",
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

REQ_COUNT = 38
ALLOWED_STAGES = {"0", "0.5", "1A", "1B", "2", "3", "4", "5", "6"}
STATUS_MARKER_RE = re.compile(r"CURRENT-STAGE:\s*(\S+)")
REQ_RE = re.compile(r"CCC-REQ-\d{3}")

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
    (
        re.compile(
            r"(?i)\b(password|passwd|secret|api[_-]?key)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
        ),
        "inline credential assignment",
    ),
]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def iter_files() -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            files.append(Path(dirpath) / name)
    return files


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return text


def heading_slugs(md_path: Path) -> set[str]:
    counts: dict[str, int] = {}
    result: set[str] = set()
    for line in md_path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = slugify(match.group(2))
        if not base:
            continue
        count = counts.get(base, 0)
        counts[base] = count + 1
        result.add(base if count == 0 else f"{base}-{count}")
    return result


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
            if target.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            file_part, _, fragment = target.partition("#")
            fragment = unquote(fragment)
            if not file_part:
                # Pure in-page anchor: check against this document.
                if fragment and fragment not in heading_slugs(md):
                    fail(f"{md.relative_to(REPO_ROOT)}: broken anchor: #{fragment}")
                    errors += 1
                continue
            candidate = (md.parent / file_part).resolve()
            try:
                candidate.relative_to(REPO_ROOT.resolve())
            except ValueError:
                fail(f"{md.relative_to(REPO_ROOT)}: link escapes repo: {target}")
                errors += 1
                continue
            if not candidate.exists():
                fail(f"{md.relative_to(REPO_ROOT)}: broken link: {file_part}")
                errors += 1
                continue
            if fragment and candidate.suffix.lower() == ".md":
                if fragment not in heading_slugs(candidate):
                    fail(
                        f"{md.relative_to(REPO_ROOT)}: broken anchor:"
                        f" {file_part}#{fragment}"
                    )
                    errors += 1
    return errors


def check_requirement_mapping() -> int:
    errors = 0
    charter = (REPO_ROOT / "docs/PRODUCT_CHARTER.md").read_text(encoding="utf-8")
    acceptance = (REPO_ROOT / "docs/ACCEPTANCE_TESTS.md").read_text(encoding="utf-8")

    charter_ids = REQ_RE.findall(charter)
    charter_set = set(charter_ids)
    if len(charter_ids) != len(charter_set):
        fail("docs/PRODUCT_CHARTER.md contains duplicate requirement IDs")
        errors += 1
    if len(charter_set) != REQ_COUNT:
        fail(
            f"charter defines {len(charter_set)} requirement IDs;"
            f" expected {REQ_COUNT}"
        )
        errors += 1

    acceptance_set = set(REQ_RE.findall(acceptance))
    missing = charter_set - acceptance_set
    orphans = acceptance_set - charter_set
    for req_id in sorted(missing):
        fail(f"requirement {req_id} has no acceptance-test mapping")
        errors += 1
    for req_id in sorted(orphans):
        fail(f"acceptance tests reference unknown requirement {req_id}")
        errors += 1
    return errors


def check_status_marker() -> int:
    errors = 0
    values: dict[str, str] = {}
    for rel in ("README.md", "docs/ROADMAP.md"):
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        match = STATUS_MARKER_RE.search(text)
        if not match:
            fail(f"{rel} is missing a CURRENT-STAGE status marker")
            errors += 1
            continue
        value = match.group(1)
        values[rel] = value
        if value not in ALLOWED_STAGES:
            fail(f"{rel} has unknown stage token: {value}")
            errors += 1
    if len(values) == 2 and len(set(values.values())) != 1:
        fail(
            "status markers disagree between README.md and docs/ROADMAP.md:"
            f" {values}"
        )
        errors += 1
    return errors


def check_docs_inventory() -> int:
    errors = 0
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    for doc in sorted((REPO_ROOT / "docs").glob("*.md")):
        rel = f"docs/{doc.name}"
        if rel not in readme:
            fail(f"{rel} is not linked from README.md (orphan document)")
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


def main() -> int:
    print("Content Command Center - documentation verification")
    print(f"Repository root: {REPO_ROOT}")
    total = 0
    print("\n[1/8] Required files")
    total += check_required_files()
    print("\n[2/8] Relative links and anchors")
    total += check_links()
    print("\n[3/8] Requirement mapping (charter <-> acceptance tests)")
    total += check_requirement_mapping()
    print("\n[4/8] Status markers (README <-> ROADMAP)")
    total += check_status_marker()
    print("\n[5/8] Documentation inventory (no orphan docs)")
    total += check_docs_inventory()
    print("\n[6/8] Forbidden file types")
    total += check_forbidden_files()
    print("\n[7/8] Secret pattern scan")
    total += check_secret_patterns()
    print("\n[8/8] Done")
    print()
    if total:
        print(f"FAILED: {total} problem(s) found.")
        return 1
    print("OK: all documentation checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
