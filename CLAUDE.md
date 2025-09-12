# CLAUDE.md

## Project Overview
**StudioHub** - Design Studio Orchestration Platform for Estudio Baum Arquitectos

A WhatsApp-integrated project management system that automates craftsman communication, quote collection, and invoice generation for architectural design projects.

## Architecture
- **Backend**: FastAPI + PostgreSQL + SQLAlchemy + Celery
- **Frontend**: React + TypeScript + Tailwind CSS
- **Integrations**: WhatsApp Business API, AWS S3
- **Queue**: Redis + Celery for async processing

## Core Data Model
```
Project → Campaign → Item → Quote/Task
User, Craftsman, Client entities
```

## Key Business Logic
- **Quote Processing**: Multi-craftsman comparison with margin calculations
- **Invoice Generation**: PDF creation with company branding
- **WhatsApp Parsing**: Extract prices/status from Spanish messages
- **Document Management**: CAD files and project assets in S3

## Development Approach
- **Methodology**: "Vibecodeing" - iterative weekly milestones
- **Testing**: Focus on critical paths (invoice generation, WhatsApp sending)
- **Deployment**: Docker containerization

## File Structure
```
backend/app/
├── models/          # SQLAlchemy entities
├── schemas/         # Pydantic validation
├── services/        # Business logic
├── routers/         # API endpoints
└── workers/         # Celery tasks

frontend/src/
├── components/      # Reusable UI
├── pages/          # Route components
├── services/       # API clients
└── types/          # TypeScript definitions
```

## Current Implementation Status
- **Phase**: Development planning complete
- **Next**: Milestone 1 - Core data model and basic CRUD
- **Priority**: Financial engine (invoice generation) and WhatsApp integration

## Key Technical Challenges
1. WhatsApp message parsing for Spanish quotes/status updates
2. PDF generation with proper margin calculations
3. Real-time WebSocket integration for chat
4. S3 document organization and presigned URLs

## Environment Context
- **Users**: Spanish/Catalan speaking architects
- **Craftsmen**: Limited digital skills, WhatsApp-only communication
- **Focus**: Minimize admin work, maximize design time

## Development Workflow

### Development Principles
- **DRY** (Don't Repeat Yourself) - Reusable components and services
- **SOLID** - Single responsibility, open/closed, dependency inversion
- **KISS** (Keep It Simple, Stupid) - Minimal complexity, clear code
- **REST** - RESTful API design with proper HTTP methods and status codes

### Process
1. **Read & Understand** - Analyze current milestone/issue requirements
2. **Plan** - Create detailed task breakdown with checkboxes
3. **Confirm** - Get approval before implementation
4. **Code** - Implement features following architecture
5. **Review** - Human code review and feedback
6. **Test** - Write comprehensive tests
7. **Commit** - Push when tests pass

### GitHub Integration
- **Milestones**: Track weekly development phases (M1-M10)
- **Issues**: Break milestones into specific tasks
- **Branches**: Feature branches for each issue (`issue-{number}-{description}`)
- **Pull Requests**: Draft PR created for each issue branch
- **CI/CD**: GitHub Actions run test suite on PR to main
- **Merge**: Tests pass → Human approval → Issue auto-closed
- **Commits**: Concise, descriptive messages

### Branch Strategy
- **main**: Production-ready code and documentation only
- **develop**: Main development branch for current milestone work
- **feature branches**: Individual features branch from develop (`issue-{number}-{description}`)
- **Documentation**: Can be committed directly to main (markdown files only)
- **Code**: Must go through develop → feature branch → PR → develop → main workflow

### Terminal Usage
Claude is authorized to use standard development commands:
- `bash`, `grep`, `find`, `sed`, `awk`
- `git` operations (clone, branch, commit, push, merge)
- `gh` CLI for GitHub management
- `curl`, `wget` for API testing
- `docker`, `docker-compose` for containerization
- Package managers: `uv` (default), `pip`, `npm`, `yarn`

### Testing Priorities
- Invoice PDF generation accuracy
- WhatsApp API reliability
- Quote parsing confidence scoring
- Document upload/retrieval performance

### Commit Standards
- Format: `type: brief description`
- Types: `feat`, `fix`, `docs`, `test`, `refactor`
- Examples: `feat: add invoice PDF generation`, `fix: quote parsing regex`