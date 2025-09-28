# Pull Request Template

## Description
Describe the changes in this pull request. Include:
- What problem does this solve?
- What new features or improvements are added?
- Any breaking changes?

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code style/formatting/lint (no functional changes)
- [ ] Security enhancement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass locally (`pytest`)
- [ ] Pre-commit hooks pass (`pre-commit run --all-files`)
- [ ] Manual testing completed

## Security Checklist
Review and address each security item before merging:

### Authentication & Authorization
- [ ] No hardcoded credentials or secrets in code
- [ ] Password requirements are enforced appropriately
- [ ] Sensitive data not logged or exposed
- [ ] Authentication tokens/session handling is secure
- [ ] Access controls implemented correctly

### Input Validation & Sanitization
- [ ] All user inputs are validated (Pydantic models used)
- [ ] SQL injection prevention (parameterized queries)
- [ ] Cross-site scripting (XSS) prevention
- [ ] Cross-site request forgery (CSRF) protection (if applicable)
- [ ] File upload security (if applicable)

### Configuration & Secrets
- [ ] Environment variables used for secrets
- [ ] No sensitive data committed to Git
- [ ] Secret detection scans pass
- [ ] Secure default configurations

### Code Security
- [ ] Bandit security linting passes
- [ ] No known vulnerabilities in dependencies
- [ ] No insecure functions/patterns used
- [ ] Error messages don't leak sensitive information

### Database & Data Handling
- [ ] No SQL injection vulnerabilities
- [ ] Database connections properly handled
- [ ] Data encryption where required
- [ ] Migration scripts safe and tested

### Logging & Monitoring
- [ ] Sensitive data not logged
- [ ] Error handling doesn't expose internal details
- [ ] Security-relevant events logged appropriately

### Dependencies
- [ ] Dependencies scanned for vulnerabilities (safety check, etc.)
- [ ] Requirements.txt up to date and pinned versions used
- [ ] No unnecessary dependencies added

### Production Readiness
- [ ] Debug mode disabled by default
- [ ] HTTPS required for production endpoints
- [ ] Rate limiting implemented if needed
- [ ] Monitoring and alerting configured

## Documentation Updates
- [ ] README updated if necessary
- [ ] API documentation updated for new endpoints
- [ ] Code comments added for complex logic
- [ ] CHANGELOG updated (if applicable)

## Deployment Notes
Any special deployment considerations or migration steps required?

## Screenshots (if applicable)
Add screenshots or logs to help demonstrate the changes.

## Checklist
- [ ] I have read the [CONTRIBUTING](CONTRIBUTING.md) guidelines
- [ ] My code follows the project's coding standards
- [ ] I have tested my changes thoroughly
- [ ] I have updated documentation as needed
- [ ] All CI checks pass
- [ ] Security checklist is completed
