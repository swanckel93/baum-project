# StudioHub - Implementation Plan

## Development Methodology: Vibecodeing

Building iteratively with working software at each milestone. Each week delivers immediate value to the business.

---

## Milestone 1: Core Data Model & Basic CRUD
**Duration**: Week 1  
**Goal**: Establish foundational data structure and basic interface

### Technical Deliverables
```python
# Core entities
Project -> Campaign -> Item -> Quote
                           -> Task
User, Craftsman, Client
```

### Implementation Tasks
- [ ] Initialize FastAPI project structure
- [ ] Define SQLAlchemy models
- [ ] Create PostgreSQL schema with migrations
- [ ] Build CRUD endpoints for all entities
- [ ] Create React project with TypeScript
- [ ] Implement basic forms and tables
- [ ] Add navigation between entities

### Success Criteria
- Can create a project and break it into campaigns/items
- Can add multiple quotes per item
- Basic data validation working
- All relationships properly enforced

### File Structure
```
backend/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── project.py
│   │   ├── campaign.py
│   │   ├── item.py
│   │   └── quote.py
│   └── routers/
│       └── v1/
frontend/
├── src/
│   ├── pages/
│   │   ├── Projects.tsx
│   │   └── Items.tsx
│   └── api/
```

---

## Milestone 2: Financial Engine Core
**Duration**: Week 2  
**Goal**: Replace manual invoice creation process

### Implementation Tasks
- [ ] Quote comparison interface
- [ ] Invoice data model
- [ ] PDF generation service (reportlab)
- [ ] Invoice template with company branding
- [ ] Cost breakdown calculator
- [ ] Margin calculation (per item and project)
- [ ] Local PDF storage
- [ ] Invoice listing and retrieval

### Key Components
```python
# services/invoice.py
class InvoiceGenerator:
    def create_invoice(campaign_id: int) -> PDF
    def calculate_margins(item_id: int) -> MarginData
    
# services/pdf.py  
class PDFService:
    def generate_quote_pdf(quote_id: int) -> bytes
    def generate_invoice_pdf(invoice_id: int) -> bytes
```

### Success Criteria
- Generate professional invoice PDF in < 2 seconds
- Accurate margin calculations
- Side-by-side quote comparison
- PDF includes all necessary legal/tax information

---

## Milestone 3: WhatsApp Sending
**Duration**: Week 3  
**Goal**: Automate document delivery via WhatsApp

### Implementation Tasks
- [ ] WhatsApp Business API account setup
- [ ] Environment configuration for API credentials
- [ ] Message template creation and approval
- [ ] PDF attachment service
- [ ] Delivery status webhook handler
- [ ] Retry logic for failed sends
- [ ] Phone number validation
- [ ] Message history tracking

### API Integration
```python
# services/whatsapp.py
class WhatsAppService:
    def send_document(phone: str, pdf: bytes, caption: str)
    def send_template(phone: str, template_id: str, params: dict)
    def check_delivery_status(message_id: str)
```

### Templates Required
1. Quote delivery: "Adjunto presupuesto para {PROJECT_NAME}"
2. Invoice delivery: "Factura {INVOICE_NUMBER} - {CAMPAIGN_NAME}"
3. Quote request: "Solicitud de presupuesto: {ITEM_DESCRIPTION}"

### Success Criteria
- Send invoice/quote with single button click
- Delivery confirmation within UI
- 95%+ successful delivery rate

---

## Milestone 4: Document Management & S3
**Duration**: Week 4  
**Goal**: Centralize all project documents

### Implementation Tasks
- [ ] AWS S3 bucket configuration
- [ ] IAM roles and security setup
- [ ] File upload API with streaming
- [ ] CAD file ZIP extraction and organization
- [ ] S3 folder structure (project/campaign/item)
- [ ] Presigned URL generation
- [ ] Document metadata tracking
- [ ] File browser UI component
- [ ] Migration of existing PDFs to S3

### S3 Structure
```
studiohub-docs/
├── projects/
│   ├── {project_id}/
│   │   ├── cad/
│   │   ├── invoices/
│   │   ├── quotes/
│   │   └── attachments/
```

### Success Criteria
- Upload 500MB CAD files without timeout
- Generate shareable links valid for 7 days
- Automatic backup of all generated documents
- Search documents by project/date/type

---

## Milestone 5: Status Tracking & Pipeline View
**Duration**: Week 5  
**Goal**: Visual project management

### Implementation Tasks
- [ ] Status enum definition and transitions
- [ ] Kanban board component
- [ ] Drag-and-drop status updates
- [ ] Timeline/Gantt view
- [ ] Deadline field and calculations
- [ ] Color coding for delays
- [ ] Status change history log
- [ ] Bulk operations interface
- [ ] Email/WhatsApp alerts for delays

### Status Pipeline
```
DESIGN → QUOTING → APPROVED → MANUFACTURING → QUALITY_CHECK → DELIVERED
```

### Success Criteria
- Update 10 items status in < 30 seconds
- Visual indication of bottlenecks
- Accurate deadline tracking
- Historical status analytics

---

## Milestone 6: WhatsApp Chat Integration - Read
**Duration**: Weeks 6-7  
**Goal**: Centralize WhatsApp conversations

### Implementation Tasks
- [ ] WhatsApp webhook receiver setup
- [ ] Message queue (Redis + Celery)
- [ ] WebSocket server for real-time updates
- [ ] Chat UI component with pagination
- [ ] Contact synchronization
- [ ] Message search functionality
- [ ] Conversation-to-project linking
- [ ] Media message handling
- [ ] Encryption/decryption for stored messages

### Architecture
```python
# Webhook -> Queue -> Processor -> WebSocket -> Frontend
webhook_handler -> Redis Queue -> Celery Worker -> Socket.IO -> React
```

### Success Criteria
- < 1 second delay for message appearance
- Search across 10,000+ messages
- Link conversations to projects/items
- Handle 100 messages/minute

---

## Milestone 7: Smart Parsing & Automation
**Duration**: Weeks 8-9  
**Goal**: Extract information from WhatsApp automatically

### Implementation Tasks
- [ ] Quote parser with regex patterns
- [ ] Multi-language parsing (Spanish/Catalan)
- [ ] Currency and number extraction
- [ ] Status keyword detection
- [ ] Confidence scoring algorithm
- [ ] Manual approval queue for low confidence
- [ ] Parser training interface
- [ ] Auto-association with pending requests
- [ ] Parsing rules configuration

### Parsing Patterns
```python
PRICE_PATTERNS = [
    r"precio.*?(\d+[\d,\.]*)\s*€",
    r"total.*?(\d+[\d,\.]*)",
    r"(\d+[\d,\.]*)\s*euros"
]

STATUS_KEYWORDS = {
    "COMPLETED": ["terminado", "acabado", "listo"],
    "IN_PROGRESS": ["empezando", "trabajando", "en proceso"],
}
```

### Success Criteria
- 85%+ accuracy on price extraction
- 90%+ accuracy on status updates
- Handle mixed language messages
- Process 1 message in < 100ms

---

## Milestone 8: Historical Intelligence
**Duration**: Week 10  
**Goal**: Predict costs based on history

### Implementation Tasks
- [ ] Historical price database schema
- [ ] Item similarity algorithm
- [ ] Price range prediction model
- [ ] Craftsman reliability scoring
- [ ] Seasonality detection
- [ ] Price trend visualization
- [ ] Anomaly detection for unusual quotes
- [ ] Suggestion API for new quotes
- [ ] Confidence intervals for predictions

### Prediction Model
```python
class PricePredictor:
    def predict_range(item_description: str) -> PriceRange
    def find_similar_items(item: Item, threshold: float) -> List[Item]
    def calculate_reliability(craftsman_id: int) -> ReliabilityScore
```

### Success Criteria
- Predictions within 15% of actual quotes
- Identify unreliable craftsmen (>2 std dev)
- Detect seasonal patterns
- Suggest alternatives for overpriced quotes

---

## Milestone 9: Advanced Financial Analytics
**Duration**: Week 11  
**Goal**: Complete business intelligence

### Implementation Tasks
- [ ] KPI dashboard design
- [ ] Revenue/profit tracking
- [ ] Project profitability ranking
- [ ] Craftsman cost analysis
- [ ] Design time ROI calculation
- [ ] Export to CSV/Excel
- [ ] Payment tracking system
- [ ] Outstanding invoice alerts
- [ ] Monthly/quarterly reports
- [ ] Comparative period analysis

### Key Metrics
```typescript
interface DashboardMetrics {
  monthlyRevenue: number
  monthlyProfit: number
  averageMargin: number
  outstandingInvoices: number
  projectsInProgress: number
  bottleneckItems: Item[]
  topCraftsmen: Craftsman[]
}
```

### Success Criteria
- Dashboard loads in < 2 seconds
- Accurate financial calculations
- Exportable reports for accountant
- Actionable insights identified

---

## Milestone 10: Polish & Production
**Duration**: Week 12  
**Goal**: Production-ready system

### Implementation Tasks
- [ ] Authentication system (JWT)
- [ ] User management and permissions
- [ ] Database migration to PostgreSQL
- [ ] Automated backup configuration
- [ ] Error handling and logging
- [ ] Performance optimization
- [ ] Mobile responsive design
- [ ] User preferences
- [ ] Documentation
- [ ] Deployment scripts

### Production Checklist
- [ ] SSL certificates configured
- [ ] Environment variables secured
- [ ] Rate limiting implemented
- [ ] CORS properly configured
- [ ] Database indexes optimized
- [ ] Monitoring alerts setup
- [ ] Backup verification
- [ ] Load testing passed

---

## Daily Development Workflow

### Morning (2 hours)
1. Review previous day's work
2. Define 2-3 specific features
3. Create test cases
4. Set up development environment

### Coding Session (4-5 hours)
1. Implement features with Claude Code
2. Write tests alongside code
3. Regular commits with clear messages
4. Update documentation

### Evening (1 hour)
1. Manual testing with real data
2. Note bottlenecks and issues
3. Plan next day's goals
4. Update progress tracking

---

## Technical Guidelines

### Code Organization
```
project/
├── backend/
│   ├── app/
│   │   ├── core/         # Config, security
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas  
│   │   ├── services/     # Business logic
│   │   ├── routers/      # API endpoints
│   │   └── workers/      # Celery tasks
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable UI
│   │   ├── pages/       # Route pages
│   │   ├── hooks/       # Custom hooks
│   │   ├── services/    # API clients
│   │   └── types/       # TypeScript types
│   └── package.json
└── docker-compose.yml
```

### Development Principles
1. **Test critical paths** (invoice generation, WhatsApp sending)
2. **Feature flags** for gradual rollout
3. **Rollback capability** for each milestone
4. **Real data testing** from day one
5. **Documentation as you build**

### Git Strategy
- Main branch: Production ready
- Develop branch: Current milestone
- Feature branches: Individual features
- Tag each milestone completion

---

## Risk Management

### Technical Risks
| Risk | Mitigation | Contingency |
|------|------------|-------------|
| WhatsApp API delays | Start approval process Week 1 | Use SMS fallback |
| Parsing accuracy low | Collect real messages early | Manual override UI |
| S3 costs exceed budget | Monitor usage closely | Local storage option |
| Performance issues | Load test each milestone | Caching strategy |

### Schedule Risks
- **Buffer time**: 20% built into each milestone
- **Critical path**: M2 (Invoice) → M3 (WhatsApp) → M5 (Status)
- **Parallel work**: M4 (S3) can be delayed without impact

---

## Success Metrics by Milestone

| Milestone | Success Metric | Business Impact |
|-----------|---------------|-----------------|
| M1 | Data structure validated | Foundation ready |
| M2 | First invoice generated | Manual work eliminated |
| M3 | First WhatsApp sent | Communication automated |
| M4 | Documents centralized | No more file searching |
| M5 | Projects visible | Bottlenecks identified |
| M6 | Chats integrated | Single communication view |
| M7 | First auto-parsed quote | Data entry eliminated |
| M8 | First price prediction | Better cost estimates |
| M9 | Dashboard live | Business insights available |
| M10 | System stable | Production ready |

---

## Post-Launch Support Plan

### Week 13-14: Stabilization
- Bug fixes from real usage
- Performance tuning
- User training
- Documentation updates

### Month 2-3: Optimization
- Feature refinements based on feedback
- Additional parsing rules
- Report customization
- Workflow optimizations

### Future Roadmap
- Client portal
- Mobile app
- Multi-language UI
- Advanced AI features