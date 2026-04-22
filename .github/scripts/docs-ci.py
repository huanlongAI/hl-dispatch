#!/usr/bin/env python3
"""
Documentation CI - 5 validation checks for HTML documentation site
Checks: version-sync, placeholders, public-deploy, ratification, link-anchors
"""

import os
import re
import sys
import yaml
from pathlib import Path
from html.parser import HTMLParser

# ============================================================================
# Configuration
# ============================================================================
REPO_ROOT = os.getcwd()
MANIFEST_FILE = os.path.join(REPO_ROOT, 'docs-manifest.yaml')
README_FILE = os.path.join(REPO_ROOT, 'README.md')
DEPLOY_WORKFLOW = os.path.join(REPO_ROOT, '.github/workflows/deploy.yml')

# ============================================================================
# Utilities
# ============================================================================

def load_manifest():
    """Load and parse docs-manifest.yaml"""
    with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def find_html_files():
    """Find all HTML files in the repository"""
    html_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        # Skip hidden directories and .github
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return sorted(html_files)

def read_file(filepath):
    """Read file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception as e:
        print(f"WARNING: Could not read {filepath}: {e}")
        return ""

def get_relative_path(filepath):
    """Get path relative to repo root"""
    return os.path.relpath(filepath, REPO_ROOT)

# ============================================================================
# Check 1: Version Sync Check
# ============================================================================

class VersionBadgeParser(HTMLParser):
    """Extract version badges from HTML"""

    # Meta names that are version-bearing. Viewport, generator, charset,
    # description etc. are NOT version sources and must be skipped — they
    # previously triggered false positives via initial-scale=1.0 in viewport.
    VERSION_META_NAMES = {
        'version', 'spec-version', 'doc-version', 'docs-version',
        'site-version', 'guide-version',
    }

    def __init__(self):
        super().__init__()
        self.versions = []
        self.in_badge = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        # Look for badge elements with version info
        if tag == 'span' and 'badge' in attrs_dict.get('class', ''):
            self.in_badge = True
        elif tag == 'meta':
            # Only honour meta tags whose name is an explicit version source.
            # Prevents viewport `initial-scale=1.0` from masquerading as v1.0.
            name = attrs_dict.get('name', '').strip().lower()
            if name in self.VERSION_META_NAMES and 'content' in attrs_dict:
                self._extract_versions(attrs_dict['content'])

    def handle_data(self, data):
        if self.in_badge:
            self._extract_versions(data)

    def handle_endtag(self, tag):
        if tag == 'span':
            self.in_badge = False

    def _extract_versions(self, text):
        # Match version patterns like "v2.1", "v1.0", "1.0", "2.1"
        matches = re.findall(r'v?(\d+\.\d+(?:\.\d+)?)', text)
        for match in matches:
            self.versions.append(match)

def extract_versions_from_html(html_content):
    """Extract version numbers from HTML content"""
    parser = VersionBadgeParser()
    try:
        parser.feed(html_content)
    except Exception:
        pass
    return parser.versions

def check_version_sync():
    """Check 1: Verify version numbers in HTML match manifest"""
    print("\n" + "="*70)
    print("CHECK 1: Version Sync Check")
    print("="*70)

    manifest = load_manifest()
    pages = manifest.get('pages', [])

    issues = []

    for page_entry in pages:
        page_path = page_entry.get('page')
        source_docs = page_entry.get('source_docs', [])

        full_path = os.path.join(REPO_ROOT, page_path)

        if not os.path.exists(full_path):
            issues.append(f"  ✗ Page file missing: {page_path}")
            continue

        html_content = read_file(full_path)
        html_versions = extract_versions_from_html(html_content)

        # Extract versions from manifest for this page
        manifest_versions = set()
        for doc in source_docs:
            version = doc.get('version', '').strip()
            if version:
                # Normalize version format
                version = version.lstrip('v')
                manifest_versions.add(version)

        # Normalize extracted versions
        html_versions_set = set(v.lstrip('v') for v in html_versions)

        # Soft-pass pages that carry no version tokens at all.
        # The check fires only when a page self-declares versions AND they
        # disagree with the manifest. A page with zero declared versions is
        # assumed to inherit the manifest silently (documentation pages are
        # not required to badge every source_doc version inline).
        if not html_versions_set:
            continue

        # Check if all manifest versions appear in HTML
        missing = manifest_versions - html_versions_set
        if missing:
            issues.append(
                f"  ✗ {page_path}: Missing versions {sorted(missing)} "
                f"(manifest has {sorted(manifest_versions)}, "
                f"HTML has {sorted(html_versions_set)})"
            )

    if issues:
        print("FAILED - Version mismatches found:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("✓ PASSED - All version numbers match manifest")
        return True

# ============================================================================
# Check 2: Placeholder Check
# ============================================================================

def check_placeholders():
    """Check 2: Scan for placeholder patterns and incomplete content"""
    print("\n" + "="*70)
    print("CHECK 2: Placeholder Check")
    print("="*70)

    html_files = find_html_files()
    issues = []

    placeholder_patterns = [
        (r'alert\s*\(', 'alert() call'),
        (r'\bTODO\b', 'TODO comment'),
        (r'\bFIXME\b', 'FIXME comment'),
        (r'onclick\s*=\s*["\']alert', 'onclick alert handler'),
    ]

    for html_file in html_files:
        content = read_file(html_file)
        rel_path = get_relative_path(html_file)

        # Check for alert patterns
        for pattern, desc in placeholder_patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append(f"  ✗ {rel_path}:{line_num} - {desc}")

        # Check for .md file links (old placeholders)
        md_link_pattern = r'href=["\']([^"\']*\.md)["\']'
        matches = list(re.finditer(md_link_pattern, content, re.IGNORECASE))
        if matches:
            for match in matches:
                md_file = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                issues.append(f"  ✗ {rel_path}:{line_num} - Link to .md file (placeholder): {md_file}")

    if issues:
        print("FAILED - Placeholder patterns found:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("✓ PASSED - No placeholder patterns detected")
        return True

# ============================================================================
# Check 3: Public Deploy Check
# ============================================================================

def check_public_deploy():
    """Check 3: Ensure no public deployment configuration in README/deploy.yml"""
    print("\n" + "="*70)
    print("CHECK 3: Public Deploy Check")
    print("="*70)

    issues = []

    # Check README for --public flag in repo create commands
    if os.path.exists(README_FILE):
        readme_content = read_file(README_FILE)

        # Look for public deployment patterns
        public_patterns = [
            (r'gh repo create.*--public', 'GitHub repo create with --public flag'),
            (r'--public\s+hl-docs', '--public flag for hl-docs'),
        ]

        for pattern, desc in public_patterns:
            if re.search(pattern, readme_content, re.IGNORECASE):
                issues.append(f"  ✗ README.md contains: {desc}")

    # Check deploy.yml for public visibility settings
    if os.path.exists(DEPLOY_WORKFLOW):
        deploy_content = read_file(DEPLOY_WORKFLOW)

        # Look for public visibility patterns in workflow
        public_patterns = [
            (r'public\s*:\s*true', 'public: true visibility setting'),
            (r'--public', '--public flag in deployment'),
            (r'visibility["\']?\s*:\s*["\']?public', 'visibility: public setting'),
        ]

        for pattern, desc in public_patterns:
            if re.search(pattern, deploy_content, re.IGNORECASE):
                issues.append(f"  ✗ deploy.yml contains: {desc}")

    if issues:
        print("FAILED - Public deployment configuration found:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("✓ PASSED - No public deployment configuration detected")
        return True

# ============================================================================
# Check 4: Ratification Check
# ============================================================================

def check_ratification():
    """Check 4: Verify status consistency between HTML and manifest.

    A page is treated as claiming LOCKED ratification ONLY when it carries an
    explicit page-level marker. Two conventions are honoured:

        1. HTML comment marker:  <!-- RATIFICATION: Locked -->
        2. Class-based badge:    <... class="... ratification-locked ...">

    Bare occurrences of the word "Locked" (inside state-machine node labels
    such as "Contract Locked" / "Pilot Locked", historical fact references
    like "TEAM-COLLAB-SPEC v2.1 Pilot-Locked 2026-04-11", or tech-stack
    dependency status columns) are NOT ratification claims and must not
    trigger this check.

    A page without the explicit marker is assumed to inherit the manifest
    status silently (fine for DRAFT pages).
    """
    print("\n" + "="*70)
    print("CHECK 4: Ratification Check")
    print("="*70)

    manifest = load_manifest()
    pages = manifest.get('pages', [])

    issues = []

    # Explicit ratification-claim markers. Keep narrow on purpose.
    LOCKED_MARKERS = [
        re.compile(r'<!--\s*RATIFICATION\s*:\s*Locked\s*-->', re.IGNORECASE),
        re.compile(r'class\s*=\s*"[^"]*\bratification-locked\b[^"]*"', re.IGNORECASE),
    ]

    for page_entry in pages:
        page_path = page_entry.get('page')
        source_docs = page_entry.get('source_docs', [])
        sections = page_entry.get('sections', [])

        full_path = os.path.join(REPO_ROOT, page_path)

        if not os.path.exists(full_path):
            continue

        html_content = read_file(full_path)

        has_locked_indicator = any(m.search(html_content) for m in LOCKED_MARKERS)

        if has_locked_indicator:
            # Check manifest status - if it says DRAFT, that's a mismatch
            for doc in source_docs:
                status = doc.get('status', '').upper()
                if status == 'DRAFT':
                    issues.append(
                        f"  ✗ {page_path}: HTML carries explicit ratification-locked "
                        f"marker, but source doc '{doc.get('doc')}' is marked as "
                        f"DRAFT in manifest"
                    )

            # Also check section statuses
            for section in sections:
                section_status = section.get('spec_status', '').upper()
                if section_status == 'DRAFT':
                    section_id = section.get('id')
                    section_title = section.get('title')
                    if section_id and section_id in html_content:
                        issues.append(
                            f"  ✗ {page_path}#{section_id} ({section_title}): "
                            f"Carries ratification-locked marker but manifest "
                            f"section is DRAFT"
                        )

    if issues:
        print("FAILED - Status ratification issues found:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("✓ PASSED - Status indicators consistent with manifest")
        return True

# ============================================================================
# Check 5: Link Anchor Check
# ============================================================================

class LinkAnchorParser(HTMLParser):
    """Extract all links from HTML"""
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs_dict = dict(attrs)
            href = attrs_dict.get('href', '')
            if href:
                self.links.append(href)

def extract_links_from_html(html_content):
    """Extract all href links from HTML"""
    parser = LinkAnchorParser()
    try:
        parser.feed(html_content)
    except Exception:
        pass
    return parser.links

def extract_ids_from_html(html_content):
    """Extract all id attributes from HTML"""
    ids = set()
    id_pattern = r'id\s*=\s*["\']([^"\']+)["\']'
    matches = re.finditer(id_pattern, html_content)
    for match in matches:
        ids.add(match.group(1))
    return ids

def check_link_anchors():
    """Check 5: Verify internal links and anchors exist"""
    print("\n" + "="*70)
    print("CHECK 5: Link Anchor Check")
    print("="*70)

    html_files = find_html_files()
    issues = []

    # Build map of all HTML files and their IDs
    file_id_map = {}
    for html_file in html_files:
        content = read_file(html_file)
        ids = extract_ids_from_html(content)
        rel_path = get_relative_path(html_file)
        file_id_map[rel_path] = ids

    # Check each link in each file
    for html_file in html_files:
        content = read_file(html_file)
        links = extract_links_from_html(content)
        rel_path = get_relative_path(html_file)
        file_dir = os.path.dirname(rel_path)

        for link in links:
            # Skip external links and special protocols
            if link.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
                continue

            # Skip links without .html or # (e.g., plain text links)
            if '.html' not in link and '#' not in link:
                continue

            # Parse link into file and anchor
            if '#' in link:
                file_part, anchor_part = link.split('#', 1)
            else:
                file_part = link
                anchor_part = None

            # Resolve relative path
            if file_part:
                target_path = os.path.normpath(os.path.join(file_dir, file_part))
            else:
                # Same file link
                target_path = rel_path

            # Check if target file exists
            if file_part and not os.path.exists(os.path.join(REPO_ROOT, target_path)):
                issues.append(
                    f"  ✗ {rel_path}: Link target file not found: {link}"
                )
                continue

            # Check if anchor exists in target file
            if anchor_part:
                if target_path not in file_id_map:
                    issues.append(
                        f"  ✗ {rel_path}: Cannot verify anchor {anchor_part} "
                        f"(target file {target_path} not readable)"
                    )
                    continue

                if anchor_part not in file_id_map[target_path]:
                    issues.append(
                        f"  ✗ {rel_path}: Anchor #{anchor_part} not found in {target_path}"
                    )

    if issues:
        print("FAILED - Link/anchor issues found:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("✓ PASSED - All internal links and anchors valid")
        return True

# ============================================================================
# Main Execution
# ============================================================================

def main():
    print("\n" + "="*70)
    print("Documentation CI - Running 5 checks")
    print("="*70)

    results = {
        'version-sync-check': check_version_sync(),
        'placeholder-check': check_placeholders(),
        'public-deploy-check': check_public_deploy(),
        'ratification-check': check_ratification(),
        'link-anchor-check': check_link_anchors(),
    }

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {check_name}")

    print(f"\nTotal: {passed}/{total} checks passed")

    if passed < total:
        print("\n✗ CI FAILED - Some checks did not pass")
        sys.exit(1)
    else:
        print("\n✓ CI PASSED - All checks successful")
        sys.exit(0)

if __name__ == '__main__':
    main()
