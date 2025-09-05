# Branch Protection Rules

This document outlines the recommended branch protection rules for the DocForge-ai repository to ensure code quality and prevent unauthorized merges.

## Main Branch Protection

### Required Settings for `main` branch:

1. **Require a pull request before merging**
   - ✅ Require approvals: 1 (minimum)
   - ✅ Dismiss stale PR approvals when new commits are pushed
   - ✅ Require review from code owners

2. **Restrict pushes that create files**
   - ✅ Restrict pushes to matching branches

3. **Require status checks to pass before merging**
   - ✅ Require branches to be up to date before merging
   - ✅ Required status checks:
     - `Test Suite` (all platforms)
     - `Security Scan`
     - `Package Test`
     - `Docker Build Test`

4. **Require conversation resolution before merging**
   - ✅ Require conversation resolution before merging

5. **Require signed commits**
   - ✅ Require signed commits (optional but recommended)

6. **Require linear history**
   - ✅ Require linear history (optional but recommended)

7. **Include administrators**
   - ✅ Include administrators (so you can override if needed)

## Develop Branch Protection

### Required Settings for `develop` branch:

1. **Require a pull request before merging**
   - ✅ Require approvals: 1 (minimum)
   - ✅ Dismiss stale PR approvals when new commits are pushed

2. **Restrict pushes that create files**
   - ✅ Restrict pushes to matching branches

3. **Require status checks to pass before merging**
   - ✅ Require branches to be up to date before merging
   - ✅ Required status checks:
     - `Quick Check`
     - `Test Suite` (at least one platform)

4. **Require conversation resolution before merging**
   - ✅ Require conversation resolution before merging

## Code Owners

Create a `.github/CODEOWNERS` file with:

```
# Global code owners
* @Venkatesh188

# Specific file patterns
/.github/ @Venkatesh188
/pyproject.toml @Venkatesh188
/setup.py @Venkatesh188
/README.md @Venkatesh188
```

## Manual Approval Workflow

### For All Pull Requests:

1. **Automated Checks Must Pass**
   - All CI/CD pipeline checks must be green
   - No security vulnerabilities detected
   - Code coverage above 80%

2. **Manual Review Required**
   - At least one approval from @Venkatesh188
   - All review comments must be addressed
   - All conversations must be resolved

3. **Merge Restrictions**
   - No automatic merging enabled
   - Only @Venkatesh188 can merge PRs
   - Squash and merge recommended for clean history

### For Dependabot PRs:

1. **Review Process**
   - Dependabot creates PR with detailed information
   - Manual review required for all dependency updates
   - Test locally if needed before approval

2. **Approval Criteria**
   - No breaking changes detected
   - All tests pass
   - Security scan shows no new vulnerabilities
   - Changelog reviewed

## Security Considerations

### API Token Protection:
- `PYPI_API_TOKEN` - Only accessible by @Venkatesh188
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

### Branch Protection Benefits:
- Prevents direct pushes to main/develop
- Ensures code quality through required checks
- Maintains project integrity
- Prevents accidental merges

## Setup Instructions

1. Go to repository Settings → Branches
2. Add rule for `main` branch with above settings
3. Add rule for `develop` branch with above settings
4. Create `.github/CODEOWNERS` file
5. Test by creating a test PR

## Override Process

If you need to override branch protection:

1. Go to the PR page
2. Click "Merge" button
3. Select "Override branch protection"
4. Confirm the override
5. Add a comment explaining why override was needed

---

**Note**: These settings ensure that only you (@Venkatesh188) can approve and merge changes, maintaining full control over the codebase while still benefiting from automated testing and quality checks.
