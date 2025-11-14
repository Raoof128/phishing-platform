# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The Phishing Awareness Training Platform team takes security vulnerabilities seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report a Security Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:

- **Email**: security@company.com
- **Subject**: [SECURITY] Brief description of the vulnerability

### What to Include

To help us better understand the nature and scope of the issue, please include as much of the following information as possible:

1. **Type of vulnerability** (e.g., SQL injection, XSS, authentication bypass, etc.)
2. **Full paths of source file(s)** related to the vulnerability
3. **Location of the affected source code** (tag/branch/commit or direct URL)
4. **Step-by-step instructions** to reproduce the issue
5. **Proof-of-concept or exploit code** (if possible)
6. **Impact of the issue**, including how an attacker might exploit it
7. **Any potential mitigations** you've identified

### Response Timeline

- **Initial Response**: Within 48 hours
- **Assessment**: Within 5 business days
- **Status Update**: Weekly updates until resolved
- **Fix Timeline**: Depends on severity (see below)

### Severity Levels

| Severity | Description | Response Time |
|----------|-------------|---------------|
| **Critical** | Immediate risk to users, data breach potential | 24-48 hours |
| **High** | Significant impact, exploitable remotely | 1 week |
| **Medium** | Moderate impact, requires specific conditions | 2 weeks |
| **Low** | Limited impact, difficult to exploit | 1 month |

## Security Best Practices

### For Users

When deploying this platform, please ensure:

1. **Use HTTPS** in production environments
2. **Enable SSL certificate verification** (set `verify_ssl: true` in config)
3. **Change default API keys** before deployment
4. **Use strong passwords** for GoPhish and SMTP
5. **Restrict CORS origins** to trusted domains
6. **Enable rate limiting** (already configured)
7. **Keep dependencies updated** regularly
8. **Use environment variables** for sensitive data
9. **Regular security audits** of your deployment
10. **Monitor health endpoints** for anomalies

### For Developers

When contributing to this project:

1. **Never commit secrets** (API keys, passwords, tokens)
2. **Validate all input** before processing
3. **Use parameterized queries** to prevent SQL injection
4. **Implement proper authentication** for all sensitive endpoints
5. **Follow OWASP Top 10** security guidelines
6. **Run security scanners** (Bandit, Safety) on your code
7. **Keep dependencies updated** and review security advisories
8. **Use type hints** to catch potential issues early
9. **Write security tests** for authentication and authorization
10. **Review code** for security implications before submitting PRs

## Security Features

### Current Security Implementations

✅ **Rate Limiting** - Prevents DoS attacks (60 req/min, 1000 req/hour)
✅ **CORS Protection** - Restricts cross-origin requests
✅ **Input Validation** - Email validation and string sanitization
✅ **SQL Injection Protection** - Parameterized queries
✅ **Error Handling** - Prevents information disclosure
✅ **Health Monitoring** - `/health` endpoint for service checks
✅ **Dependency Scanning** - Regular vulnerability checks
✅ **Secure Defaults** - Production-ready configurations

### Planned Security Enhancements

- [ ] Authentication and authorization system
- [ ] API key rotation mechanism
- [ ] Request signing and verification
- [ ] Audit logging for sensitive operations
- [ ] Two-factor authentication support
- [ ] Session management improvements
- [ ] Advanced threat detection
- [ ] Automated security scanning in CI/CD

## Known Security Considerations

### GoPhish Integration

This platform integrates with GoPhish, which handles actual phishing campaign management. Please ensure:

- GoPhish is properly secured and updated
- GoPhish API keys are kept confidential
- GoPhish runs on a secure network
- SSL/TLS is enabled for GoPhish communication

### Self-Signed Certificates

The platform supports self-signed certificates (`verify_ssl: false`). **Do not use this in production**. Always use properly signed certificates in production environments.

### Database Security

- The platform uses SQLite by default, which stores data in a local file
- Ensure proper file permissions on the database file
- Consider encrypting the database file in production
- For enterprise deployments, consider PostgreSQL or MySQL with encryption

### SMTP Credentials

SMTP credentials for sending training emails are stored in configuration files:

- Use environment variables for production
- Never commit SMTP passwords to version control
- Rotate SMTP credentials regularly
- Use app-specific passwords where available

## Dependency Security

We regularly scan dependencies for vulnerabilities using:

- **GitHub Dependabot** - Automated dependency updates
- **Safety** - Python package vulnerability scanner
- **Bandit** - Python security linter

### Running Security Scans

```bash
# Install security tools
pip install safety bandit

# Scan dependencies
safety check -r requirements.txt

# Scan code for security issues
bandit -r automation/ dashboard/

# Check for outdated packages
pip list --outdated
```

## Disclosure Policy

- **Coordinated Disclosure**: We practice responsible disclosure
- **Public Disclosure**: After a fix is available and deployed
- **Credit**: Security researchers who report vulnerabilities will be credited (if desired)
- **Bug Bounty**: Currently not available, but under consideration

## Security Hall of Fame

We recognize and thank security researchers who help us keep this platform secure:

- *Be the first to report a vulnerability!*

## Contact

For security-related questions or concerns:

- **Email**: security@company.com
- **PGP Key**: Available upon request
- **Response Time**: Within 48 hours

## Legal

This security policy applies to:

- The main repository: https://github.com/Raoof128/phishing-platform
- All official releases and distributions
- Documentation and associated materials

Unauthorized testing or attacks on production deployments are prohibited and may be illegal. Always obtain proper authorization before security testing.

---

**Last Updated**: 2025-01-15
**Version**: 1.0
**Next Review**: 2025-04-15
