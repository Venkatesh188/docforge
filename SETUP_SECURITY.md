# 🔒 Security Setup Guide

This guide will help you set up the security measures for your DocForge-ai repository to ensure only you can approve and merge changes.

## 🚀 Quick Setup

### 1. Enable Branch Protection Rules

1. Go to your repository on GitHub
2. Click **Settings** → **Branches**
3. Click **Add rule** for the `main` branch
4. Configure the following settings:

#### Main Branch Protection:
```
✅ Require a pull request before merging
  ✅ Require approvals: 1
  ✅ Dismiss stale PR approvals when new commits are pushed
  ✅ Require review from code owners

✅ Restrict pushes that create files
  ✅ Restrict pushes to matching branches

✅ Require status checks to pass before merging
  ✅ Require branches to be up to date before merging
  ✅ Required status checks:
    - Test Suite
    - Security Scan
    - Package Test
    - Docker Build Test

✅ Require conversation resolution before merging

✅ Include administrators
```

5. Click **Create** to save the rule

#### Develop Branch Protection:
Repeat the same process for the `develop` branch with these settings:
```
✅ Require a pull request before merging
  ✅ Require approvals: 1
  ✅ Dismiss stale PR approvals when new commits are pushed

✅ Restrict pushes that create files
  ✅ Restrict pushes to matching branches

✅ Require status checks to pass before merging
  ✅ Require branches to be up to date before merging
  ✅ Required status checks:
    - Quick Check
    - Test Suite

✅ Require conversation resolution before merging

✅ Include administrators
```

### 2. Set Up Code Owners

The `.github/CODEOWNERS` file is already created and configured to require your approval for all changes.

### 3. Configure Repository Settings

1. Go to **Settings** → **General**
2. Scroll down to **Danger Zone**
3. Ensure these settings are configured:

```
✅ Allow merge commits
✅ Allow squash merging
✅ Allow rebase merging
❌ Allow auto-merge (DISABLED)
```

### 4. Set Up Secrets

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:

#### Required Secrets:
- `PYPI_API_TOKEN` - Your PyPI API token for publishing
- `GITHUB_TOKEN` - Automatically provided by GitHub

#### Optional Secrets:
- `OPENAI_API_KEY` - For testing (if you want to test with real API)

### 5. Enable Security Features

1. Go to **Settings** → **Security**
2. Enable these features:

```
✅ Dependency graph
✅ Dependabot alerts
✅ Dependabot security updates
✅ Code scanning alerts
✅ Secret scanning
```

### 6. Configure Dependabot

1. Go to **Settings** → **Security** → **Code security and analysis**
2. Enable **Dependabot alerts**
3. Enable **Dependabot security updates**

## 🔍 Verification

### Test Branch Protection

1. Create a test branch:
   ```bash
   git checkout -b test-branch-protection
   ```

2. Make a small change and commit:
   ```bash
   echo "# Test" >> TEST.md
   git add TEST.md
   git commit -m "test: add test file"
   git push origin test-branch-protection
   ```

3. Create a Pull Request to `main`
4. Verify that:
   - ✅ You cannot merge without approval
   - ✅ Status checks are required
   - ✅ You need to approve the PR yourself

### Test Dependabot

1. The Dependabot configuration will automatically create PRs for dependency updates
2. Verify that these PRs:
   - ✅ Require manual approval
   - ✅ Have "needs-review" label
   - ✅ Cannot be auto-merged

### Test Security Scanning

1. Push a commit to trigger the CI pipeline
2. Verify that security scans run:
   - ✅ Safety check
   - ✅ Bandit security check
   - ✅ Semgrep scan
   - ✅ CodeQL analysis

## 🛠️ Manual Override Process

If you need to override branch protection:

### For Emergency Situations:
1. Go to the PR page
2. Click **Merge** button
3. Select **Override branch protection**
4. Add a comment explaining why override was needed
5. Confirm the override

### For Dependabot PRs:
1. Use the manual approval workflow
2. Go to **Actions** → **Manual Approval Required**
3. Run the workflow with appropriate parameters

## 📋 Security Checklist

### Initial Setup:
- [ ] Branch protection rules enabled for `main` and `develop`
- [ ] Code owners file configured
- [ ] Repository settings configured
- [ ] Secrets configured
- [ ] Security features enabled
- [ ] Dependabot configured

### Regular Maintenance:
- [ ] Review security alerts weekly
- [ ] Update dependencies monthly
- [ ] Review access permissions quarterly
- [ ] Test security measures annually

## 🚨 Troubleshooting

### Common Issues:

**Issue**: Cannot merge PR even after approval
**Solution**: Check that all required status checks are passing

**Issue**: Dependabot PRs not being created
**Solution**: Verify Dependabot is enabled in repository settings

**Issue**: Security scans failing
**Solution**: Check that all required secrets are configured

**Issue**: Cannot override branch protection
**Solution**: Ensure you have admin access to the repository

### Getting Help:

1. Check GitHub documentation on branch protection
2. Review the security policy in `SECURITY.md`
3. Create an issue with "security" label
4. Contact @Venkatesh188 for assistance

## 🔄 Maintenance

### Weekly Tasks:
- Review security alerts
- Check for failed CI runs
- Monitor dependency updates

### Monthly Tasks:
- Review access permissions
- Update security tools
- Audit security logs

### Quarterly Tasks:
- Review security policy
- Update documentation
- Conduct security assessment

## 📚 Additional Resources

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [GitHub Code Owners Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---

**Important**: After completing this setup, only you (@Venkatesh188) will be able to approve and merge changes to the repository. All automated processes will create PRs that require your manual approval.
