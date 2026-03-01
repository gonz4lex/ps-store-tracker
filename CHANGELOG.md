# Changelog

All notable changes to PlayStation Store Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial public release preparation
- Comprehensive docstrings and type hints
- Security documentation and vulnerability reporting guidelines
- Contributing guidelines and Code of Conduct
- .env.example template for configuration
- .dockerignore for optimized container builds

### Changed
- Removed hardcoded credentials from scripts
- Updated environment variable handling for secure credential management
- Enhanced documentation with project structure details

### Security
- Removed exposed credentials from repository
- Implemented secure .env-based configuration
- Added security.md with best practices

## [0.1.0] - 2026-03-01

### Added
- Initial project structure
- Gmail IMAP email fetching functionality
- PlayStation Store receipt email parser
- SQLite database storage for purchases
- Analytics module with spending insights
- Streamlit dashboard with login authentication
- Docker and docker-compose configuration
- Support for emoji purchase tracking and monthly/yearly spending reports
