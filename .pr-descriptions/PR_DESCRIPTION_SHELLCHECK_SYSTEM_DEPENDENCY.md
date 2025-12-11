# PR Description: Pin shellcheck as system dependency and use local hook

## Description

This PR replaces the external `shellcheck-py` pre-commit hook with a local hook that uses shellcheck as a system dependency, matching the PowerShell pattern. This ensures version consistency across environments and aligns with the project's dependency pinning best practices.

**Key Changes/Improvements:**

- Added shellcheck as a pinned system dependency in `system-dependencies-lint.toml`
- Created `shellcheck-wrapper.sh` local hook matching PowerShell pattern
- Updated installation scripts to install pinned shellcheck versions
- Updated version verification to include shellcheck
- Replaced external shellcheck-py hook with local hook for consistency

## Related Issues

None

## Type of Change

- [x] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [x] Code refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test addition/update
- [x] CI/CD or infrastructure change

## Pre-PR Checklist

### Code Quality

- [x] Removed commented-out code
- [x] No hardcoded credentials, API keys, or secrets
- [x] Ran pre-commit hooks: `pre-commit run --all-files`

### Tests

- [x] All tests pass: `pytest`
- [x] Coverage meets threshold (≥85%): `pytest --cov=audiometa --cov-report=term-missing --cov-fail-under=85`
- [x] New features have corresponding tests
- [x] Bug fixes include regression tests

### Documentation

- [x] Updated docstrings for new functions/classes (only when needed)
- [x] Updated README if adding new features or changing behavior
- [x] Updated CONTRIBUTING.md if changing development workflow
- [x] Added/updated type hints where appropriate
- [x] Updated CHANGELOG.md with changes

### Git Hygiene

- [x] Commit messages follow the [commit message convention](docs/COMMITTING.md)
- [x] No merge conflicts with target branch
- [x] Branch is up to date with target branch
- [x] No accidental commits (large files, secrets, personal configs)

## Breaking Changes

- [ ] This PR includes breaking changes
- [ ] Breaking changes are clearly documented below
- [ ] Migration path is provided (if applicable)

### Breaking Changes Description

N/A

## Testing Instructions

### How to Test

1. **Install shellcheck system dependency:**

   ```bash
   # macOS
   bash scripts/install-system-dependencies-macos.sh

   # Ubuntu
   bash scripts/install-system-dependencies-ubuntu.sh lint

   # Windows
   .\scripts\install-system-dependencies-windows.ps1
   ```

2. **Verify shellcheck is installed:**

   ```bash
   shellcheck --version
   # Should show: version: 0.11.0 (macOS/Windows) or 0.9.0 (Ubuntu)
   ```

3. **Test pre-commit hook:**

   ```bash
   pre-commit run shellcheck --all-files
   ```

4. **Test version verification:**
   ```bash
   python3 scripts/verify-system-dependency-versions.py
   # Should pass if shellcheck is installed with correct version
   ```

### Test Results

- ✅ Shellcheck installed successfully via installation scripts
- ✅ Pre-commit hook runs successfully with local hook
- ✅ Version verification includes shellcheck
- ✅ All pre-commit hooks pass

## Additional Context

This change aligns with the project's dependency pinning strategy and ensures consistency with how PowerShell is handled. The local hook pattern matches the PowerShell wrapper pattern for consistency across lint dependencies.

**Benefits:**

- Version consistency: Shellcheck versions are pinned and verified across environments
- Alignment with best practices: Follows dependency pinning rules instead of using "latest"
- Consistency: Matches PowerShell pattern for lint dependencies
- Reproducibility: Ensures same shellcheck version in CI and local development

## Checklist for Reviewers

- [ ] Code follows project conventions and style
- [ ] Logic is sound and well-structured
- [ ] Error handling is appropriate
- [ ] CI tests pass on all platforms and Python versions
- [ ] Test coverage is adequate for the changes
- [ ] Public API changes are documented
- [ ] Breaking changes are clearly marked and documented
- [ ] All review comments are addressed
- [ ] No unresolved discussions
