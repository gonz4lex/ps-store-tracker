# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please email security@example.com with:

- A description of the vulnerability
- Steps to reproduce it
- Potential impact

**Do not** open a public GitHub issue for security vulnerabilities.

## Security Best Practices

### Credentials and Secrets

- Never commit `.env` files to version control
- Always use `.env.example` as a template
- Rotate Gmail app passwords regularly
- Use environment-specific configurations

### Email Security

- This tool uses Gmail app passwords (compatible with 2FA)
- Credentials are never persisted to disk
- Temporary session credentials are cleared when the app exits

### Data Storage

- Purchase data is stored in SQLite locally
- No data is transmitted to external servers
- Users are responsible for securing their `data/` directory

### Docker Security

- Keep base images updated (`python:3.10-slim`)
- Never build images with secrets embedded
- Use `.dockerignore` to exclude sensitive files
- Run containers with minimal required privileges

## Known Limitations

- Parser depends on PlayStation email format; changes may break extraction
- SQLite is suitable for personal use; consider PostgreSQL for production
- Credentials required for email access via IMAP

## Updates and Patches

Keep the project and dependencies updated:

```bash
pip install --upgrade -r requirements.txt
```

## Contact

For security inquiries, contact the maintainers privately.
