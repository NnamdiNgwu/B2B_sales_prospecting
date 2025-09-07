<<<<<<< HEAD
# B2B_sales_prospecting

Requirements
Click on each deliverable to expand details
Pitch Deck (≤20 slides, excluding appendix)
Product-Demo Video (max 3 min)
Live Product Link
Technical Appendix (optional)
Judging Criteria
Market Need & User Impact
Clear definition of problem/pain-point and target audience
Evidence of demand (e.g., surveys, market analysis, wait-lists)
Technical Execution
Robustness of the working prototype
Quality of LLM-agent integration
Feasibility of scaling from MVP to full product
Scalability & Business Model
Strategic plan (timelines, milestones)
Path to monetization and a self-sustaining business
Pitch Quality
Clarity and persuasiveness of narrative
Cohesive story linking problem, solution, and market opportunity
Ability to inspire investor confidence


Business Name: ProspectAI Navigator
"Your AI-powered B2B sales prospecting assistant. Automate lead generation, get personalized outreach recommendations, and close more deals faster."


graph TB
    subgraph "User Interface Layer"
        A[Web Dashboard]
        B[CLI Interface]
        C[Configuration Files]
    end
    
    subgraph "Authentication & Access"
        D[LinkedIn Authenticator]
        E[Sales Navigator Auth]
        F[CRM Integrations]
    end
    
    subgraph "Data Collection Layer"
        G[LinkedIn Scraper]
        H[Company Profile Extractor]
        I[Contact Information Harvester]
        J[Industry Data Collector]
    end
    
    subgraph "AI Processing Engine"
        K[Lead Scoring AI]
        L[Personalization Engine]
        M[Message Generator]
        N[Prospect Qualifier]
    end
    
    subgraph "Database Layer"
        O[Prospect Database]
        P[Company Database]
        Q[Interaction History]
        R[Templates Library]
    end
    
    subgraph "Outreach Engine"
        S[LinkedIn Messenger]
        T[Email Automation]
        U[Sequence Manager]
        V[Follow-up Scheduler]
    end
    
    subgraph "Analytics & Reporting"
        W[Performance Dashboard]
        X[ROI Analytics]
        Y[Conversion Tracking]
        Z[A/B Testing]
    end
    
    subgraph "External Integrations"
        AA[CRM Systems]
        BB[Email Platforms]
        CC[Sales Tools]
        DD[Data Enrichment APIs]
    end
    
    A --> D
    B --> D
    C --> D
    D --> G
    E --> G
    F --> AA
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    N --> O
    O --> P
    P --> Q
    Q --> R
    R --> S
    S --> T
    T --> U
    U --> V
    V --> W
    W --> X
    X --> Y
    Y --> Z
    AA --> O
    BB --> T
    CC --> K
    DD --> H




    Key Features of ProspectAI Navigator
Automated Lead Generation: Scrapes LinkedIn for qualified prospects
AI-Powered Personalization: Uses LLM to create personalized outreach messages
Lead Scoring: Automatically scores prospects based on criteria
CRM Integration: Syncs with popular CRM systems
Compliance Management: Respects LinkedIn limits and terms of service
Analytics Dashboard: Tracks conversion rates and ROI
A/B Testing: Tests different message templates for optimization
Multi-Channel Outreach: LinkedIn, email, website contact form and other platforms
Automated Follow-ups: Sequences and schedules follow-up messages
Company Intelligence: Gathers comprehensive company data
This architecture maintains the robust foundation of the AI job hunt project while completely transforming it for B2B sales prospecting use cases.




ProspectAI Navigator - Project Requirements
1. Project Overview
Project Name: ProspectAI Navigator
Version: 1.0
Project Type: B2B Sales Prospecting Automation Platform
Development Timeline: 12-16 weeks

1.1 Business Objective
Develop an AI-powered B2B sales prospecting platform that automates lead generation, personalizes outreach, and manages sales sequences to increase conversion rates and reduce manual prospecting time by 70%.

1.2 Target Users
Sales Development Representatives (SDRs)
Account Executives
Sales Managers
Business Development Teams
Small to Medium B2B Companies
2. Functional Requirements
2.1 User Interface Layer
2.1.1 Web Dashboard
Requirement ID: UI-001
Priority: High
Description: Modern web-based dashboard for prospect management
Acceptance Criteria:
Responsive design supporting desktop and tablet
Real-time prospect pipeline visualization
Interactive prospect filtering and search
Campaign performance metrics display
Dark/light theme toggle
2.1.2 CLI Interface
Requirement ID: UI-002
Priority: Medium
Description: Command-line interface for automation and scripting
Acceptance Criteria:
Support for batch operations
Progress indicators for long-running tasks
Configurable output formats (JSON, CSV, table)
Integration with CI/CD pipelines
2.1.3 Configuration Management
Requirement ID: UI-003
Priority: High
Description: YAML-based configuration system
Acceptance Criteria:
Hierarchical configuration structure
Environment-specific configs (dev, staging, prod)
Configuration validation and error reporting
Hot-reload capabilities
2.2 Authentication & Access Control
2.2.1 LinkedIn Authentication
Requirement ID: AUTH-001
Priority: Critical
Description: Secure LinkedIn login and session management
Acceptance Criteria:
OAuth 2.0 implementation
Multi-factor authentication support
Session persistence and renewal
Rate limiting compliance
Cookie and CSRF protection
2.2.2 Sales Navigator Integration
Requirement ID: AUTH-002
Priority: High
Description: Enhanced LinkedIn Sales Navigator access
Acceptance Criteria:
Premium account detection
Advanced search capabilities
Lead recommendations integration
Saved search synchronization
2.2.3 CRM Authentication
Requirement ID: AUTH-003
Priority: High
Description: Multi-CRM authentication system
Acceptance Criteria:
Support for Salesforce, HubSpot, Pipedrive
API key management
Token refresh mechanisms
Permission scope validation
2.3 Data Collection Layer
2.3.1 LinkedIn Scraper
Requirement ID: DATA-001
Priority: Critical
Description: Intelligent LinkedIn profile and company data extraction
Acceptance Criteria:
Respect LinkedIn rate limits (max 100 profiles/hour)
CAPTCHA detection and handling
Proxy rotation support
Data quality validation
Anti-detection measures
2.3.2 Company Profile Extractor
Requirement ID: DATA-002
Priority: High
Description: Comprehensive company information gathering
Acceptance Criteria:
Company size, industry, location extraction
Recent news and updates collection
Technology stack identification
Financial information gathering
Social media presence analysis
2.3.3 Contact Information Harvester
Requirement ID: DATA-003
Priority: High
Description: Email and phone number discovery
Acceptance Criteria:
Email pattern recognition
Domain-based email guessing
Phone number extraction from profiles
Contact verification mechanisms
GDPR compliance for EU contacts
2.3.4 Industry Data Collector
Requirement ID: DATA-004
Priority: Medium
Description: Industry trends and market intelligence
Acceptance Criteria:
Industry classification accuracy >95%
Market trend analysis
Competitor identification
Industry-specific pain points database
2.4 AI Processing Engine
2.4.1 Lead Scoring AI
Requirement ID: AI-001
Priority: Critical
Description: ML-based prospect qualification and scoring
Acceptance Criteria:
Scoring algorithm with 85%+ accuracy
Customizable scoring criteria
Real-time score updates
Score explanation and reasoning
A/B testing for scoring models
2.4.2 Personalization Engine
Requirement ID: AI-002
Priority: Critical
Description: AI-powered message personalization
Acceptance Criteria:
Integration with GPT-4, Claude, or Gemini
Context-aware message generation
Tone and style customization
Multi-language support (English, Spanish, French)
Personalization quality scoring
2.4.3 Message Generator
Requirement ID: AI-003
Priority: High
Description: Automated message creation for different scenarios
Acceptance Criteria:
Template-based generation
Dynamic content insertion
Message variant generation
Compliance checking (CAN-SPAM, GDPR)
Character limit optimization
2.4.4 Prospect Qualifier
Requirement ID: AI-004
Priority: High
Description: Automated prospect qualification system
Acceptance Criteria:
Rule-based qualification engine
Machine learning qualification models
Custom qualification criteria
Qualification confidence scoring
Manual override capabilities
2.5 Database Layer
2.5.1 Prospect Database
Requirement ID: DB-001
Priority: Critical
Description: Comprehensive prospect data management
Acceptance Criteria:
PostgreSQL or MongoDB implementation
Data deduplication mechanisms
Full-text search capabilities
Data retention policies
Backup and recovery procedures
2.5.2 Company Database
Requirement ID: DB-002
Priority: High
Description: Company information storage and management
Acceptance Criteria:
Hierarchical company structure support
Change tracking and versioning
Related company identification
Data enrichment workflows
Integration with external databases
2.5.3 Interaction History
Requirement ID: DB-003
Priority: Critical
Description: Complete interaction tracking system
Acceptance Criteria:
Timeline-based interaction logs
Outcome tracking and analysis
Response time measurements
Engagement scoring
Data export capabilities
2.5.4 Templates Library
Requirement ID: DB-004
Priority: Medium
Description: Message template management system
Acceptance Criteria:
Version control for templates
Performance metrics per template
Template categorization and tagging
User-specific template libraries
Template sharing capabilities
2.6 Outreach Engine
2.6.1 LinkedIn Messenger
Requirement ID: OUT-001
Priority: Critical
Description: Automated LinkedIn messaging system
Acceptance Criteria:
Connection request automation
Message sending with delays
Message status tracking
Bulk messaging capabilities
Error handling and retry logic
2.6.2 Email Automation
Requirement ID: OUT-002
Priority: High
Description: Multi-channel email outreach platform
Acceptance Criteria:
SMTP integration
Email deliverability optimization
Bounce and spam monitoring
Email tracking (opens, clicks)
Unsubscribe management
2.6.3 Sequence Manager
Requirement ID: OUT-003
Priority: High
Description: Multi-step outreach sequence automation
Acceptance Criteria:
Drag-and-drop sequence builder
Conditional logic support
Multi-channel sequences
Sequence performance analytics
Manual intervention capabilities
2.6.4 Follow-up Scheduler
Requirement ID: OUT-004
Priority: High
Description: Intelligent follow-up scheduling system
Acceptance Criteria:
Time zone-aware scheduling
Business hours optimization
Follow-up frequency controls
Engagement-based scheduling
Calendar integration
2.7 Analytics & Reporting
2.7.1 Performance Dashboard
Requirement ID: ANALYTICS-001
Priority: High
Description: Real-time campaign performance monitoring
Acceptance Criteria:
KPI visualization (response rate, conversion rate)
Campaign comparison tools
Drill-down capabilities
Export functionality
Mobile-responsive design
2.7.2 ROI Analytics
Requirement ID: ANALYTICS-002
Priority: High
Description: Return on investment tracking and analysis
Acceptance Criteria:
Cost per lead calculations
Revenue attribution tracking
Time-to-close analysis
Pipeline value tracking
Forecast modeling
2.7.3 Conversion Tracking
Requirement ID: ANALYTICS-003
Priority: Medium
Description: Detailed conversion funnel analysis
Acceptance Criteria:
Multi-stage funnel tracking
Drop-off point identification
Conversion rate optimization
Cohort analysis
Attribution modeling
2.7.4 A/B Testing
Requirement ID: ANALYTICS-004
Priority: Medium
Description: Systematic message and strategy testing
Acceptance Criteria:
Test setup and management
Statistical significance calculation
Automated test conclusion
Results visualization
Test history tracking
2.8 External Integrations
2.8.1 CRM Systems
Requirement ID: INT-001
Priority: Critical
Description: Bi-directional CRM synchronization
Acceptance Criteria:
Real-time data synchronization
Conflict resolution mechanisms
Custom field mapping
Bulk data operations
Webhook support
2.8.2 Email Platforms
Requirement ID: INT-002
Priority: High
Description: Integration with email service providers
Acceptance Criteria:
Support for SendGrid, Mailgun, AWS SES
Deliverability optimization
Template synchronization
Analytics integration
Compliance monitoring
2.8.3 Sales Tools
Requirement ID: INT-003
Priority: Medium
Description: Integration with popular sales tools
Acceptance Criteria:
Zapier integration
Slack notifications
Calendar scheduling tools
Video conferencing platforms
Document management systems
2.8.4 Data Enrichment APIs
Requirement ID: INT-004
Priority: High
Description: Third-party data enrichment services
Acceptance Criteria:
Clearbit, ZoomInfo, Apollo integration
Data quality scoring
Cost optimization
Rate limiting management
Data freshness tracking
3. Non-Functional Requirements
3.1 Performance Requirements
Response Time: Web interface response time < 2 seconds
Throughput: Handle 1000+ prospects per hour
Scalability: Support 100+ concurrent users
Availability: 99.5% uptime SLA
3.2 Security Requirements
Data Encryption: AES-256 encryption for data at rest
Transport Security: TLS 1.3 for data in transit
Authentication: Multi-factor authentication required
Access Control: Role-based permissions system
Audit Logging: Complete audit trail for all actions
3.3 Compliance Requirements
GDPR: Full GDPR compliance for EU prospects
CAN-SPAM: Email marketing compliance
LinkedIn ToS: Adherence to LinkedIn terms of service
Data Retention: Configurable data retention policies
Privacy: Privacy by design implementation
3.4 Usability Requirements
Learning Curve: New users productive within 2 hours
Documentation: Comprehensive user and API documentation
Support: In-app help and tutorial system
Accessibility: WCAG 2.1 AA compliance
Internationalization: Support for multiple languages
4. Technical Requirements
4.1 Technology Stack
Backend: Python 3.11+, FastAPI/Django
Frontend: React.js 18+, TypeScript
Database: PostgreSQL 15+ with Redis caching
AI/ML: OpenAI GPT-4, Anthropic Claude, or Google Gemini
Infrastructure: Docker, Kubernetes, AWS/GCP
Monitoring: Prometheus, Grafana, ELK Stack
4.2 Development Standards
Code Quality: 90%+ test coverage
Documentation: Inline code documentation
Version Control: Git with GitFlow workflow
CI/CD: Automated testing and deployment
Code Review: Mandatory peer review process
4.3 Deployment Requirements
Environment: Cloud-native deployment
Containerization: Docker containers
Orchestration: Kubernetes or Docker Swarm
Monitoring: Application and infrastructure monitoring
Backup: Automated daily backups
5. Project Constraints
5.1 Time Constraints
MVP Delivery: 8 weeks
Full Feature Release: 16 weeks
Beta Testing: 4 weeks minimum
5.2 Budget Constraints
Development Team: 4-6 developers
Infrastructure: Cloud hosting budget
Third-party APIs: Data enrichment service costs
Licensing: AI model API costs
5.3 Legal Constraints
Platform Compliance: LinkedIn terms of service
Data Protection: GDPR and privacy regulations
Email Marketing: CAN-SPAM compliance
Export Controls: Data transfer restrictions
6. Success Criteria
6.1 Business Metrics
Lead Generation: 70% reduction in manual prospecting time
Conversion Rate: 25% improvement in outreach response rates
User Adoption: 80% user retention after 30 days
ROI: 300% ROI within 6 months of deployment
6.2 Technical Metrics
Performance: Sub-2 second response times
Reliability: 99.5% uptime
Security: Zero critical security vulnerabilities
Quality: 90%+ test coverage, <1% bug rate
7. Risk Assessment
7.1 High-Risk Items
LinkedIn API Changes: Mitigation through multiple data sources
Legal Compliance: Regular legal review and updates
Data Quality: Comprehensive validation and verification
AI Model Costs: Budget monitoring and optimization
7.2 Medium-Risk Items
Third-party Dependencies: Vendor diversification strategy
Performance Scaling: Load testing and optimization
User Adoption: Comprehensive training and support
7.3 Low-Risk Items
Technology Stack: Proven, stable technologies
Team Expertise: Experienced development team
Market Demand: Validated market need
This comprehensive requirements document provides the foundation for developing ProspectAI Navigator as a robust, scalable, and compliant B2B sales prospecting platform.


src/
├── components/
│   ├── Dashboard/
│   │   ├── index.ts
│   │   ├── Dashboard.tsx
│   │   ├── Header/
│   │   ├── Metrics/
│   │   ├── Pipeline/
│   │   ├── Filters/
│   │   └── Table/
│   ├── UI/
│   │   ├── index.ts
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Card/
│   │   ├── Modal/
│   │   └── Layout/
│   └── Charts/
├── hooks/
├── services/
├── utils/
├── types/
├── contexts/
├── constants/
└── assets/



brew install node

npm create vite@latest

select react
select variant: typescript
cd "Prospect AI"
  npm install
  npm run dev


 Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
=======
# ProspectAI Navigator

<a name="top"></a>
<div align="center">
<img src="./assets/pai.png">

  [![Email](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:nnamdi.ngwu@yandex.com)

**🤖🔍 Your AI-powered B2B sales prospecting assistant. Automate lead generation, get personalized outreach recommendations, and close more deals faster.**

</div>

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Documentation](#documentation)
7. [Troubleshooting](#troubleshooting)
8. [Conclusion](#conclusion)
9. [Contributors](#contributors)
10. [License](#license)
11. [Disclaimer](#disclaimer)

## Introduction

ProspectAI Navigator is a cutting-edge, automated tool designed to revolutionize B2B sales prospecting and outreach. In today's competitive market, connecting with the right decision-makers is critical. This program offers sales teams a significant advantage by leveraging automation and artificial intelligence to identify, engage, and qualify a large number of relevant prospects efficiently and in a personalized manner, maximizing your chances of closing more deals.

### The Challenge of Modern B2B Prospecting

Modern B2B sales teams face information overload and repetitive manual tasks. ProspectAI Navigator automates the most time-consuming aspects of the sales process, allowing you to focus on building relationships and having meaningful conversations with qualified leads.

## Features

1.  **Automated Lead Generation**
    -   Scrapes company websites and public business directories for qualified prospects based on customizable criteria (industry, company size, role, location).
    -   Continuously scans for new prospects to keep your pipeline full.

2.  **Multi-Channel Outreach Engine**
    -   Automates outreach sequences via email and website contact forms.
    -   Manages follow-ups and tracks engagement status.

3.  **AI-Powered Personalization**
    -   Integrates with GPT-4, Claude, and Gemini to generate dynamic, context-aware messages for each prospect.
    -   Matches tone and style to fit your brand and the prospect's company culture.

4.  **Scalable Campaign Management**
    -   Run and manage multiple outreach campaigns simultaneously.
    -   Provides detailed tracking and analytics on campaign performance (e.g., response rates, conversions).

5.  **Intelligent Prospect Filtering**
    -   Use company and title blacklists to avoid unwanted prospects.
    -   Smart filtering to focus on high-value, relevant leads that match your Ideal Customer Profile (ICP).

6.  **Secure Data Handling**
    -   Manages sensitive campaign data and credentials securely using local YAML configuration files.

## Installation

**Confirmed successful runs on the following:**

-   Operating Systems:
    -   Windows 10
    -   Ubuntu 22
-   Python versions:
    -   3.10
    -   3.11.9 (64b)
    -   3.12.5 (64b)

1.  **Download and Install Python:**
    Ensure you have a compatible Python version installed. If not, download and install it from [Python's official website](https://www.python.org/downloads/).

2.  **Download and Install Google Chrome:**
    Download and install the latest version of Google Chrome from the [official website](https://www.google.com/chrome).

3.  **Clone the repository:**
    ```bash
    git clone https://github.com/NnamdiNgwu/B2B_sales_prospecting.git
    cd B2B_sales_prospecting/prospect_ai
    ```

4.  **Activate virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    For Windows-based machines:
    ```bash
    .\venv\Scripts\activate
    ```

5.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### 1. secrets.yaml

This file contains sensitive information like your email credentials and LLM API keys. **Never share or commit this file to version control.**

-   `email_address: [Your business email address]`
-   `email_password: [Your email password or app-specific password]`
-   `llm_api_key: [Your OpenAI, Claude, or Gemini API key]`
    -   To obtain an API key, refer to the official documentation for [OpenAI](https://platform.openai.com/account/api-keys), [Anthropic (Claude)](https://console.anthropic.com/settings/keys), or [Google (Gemini)](https://ai.google.dev/gemini-api/docs/api-key).
    -   **Note:** For OpenAI, you need to add credit to your account to use the API. A free-tier account has strict rate limits that may cause errors.

### 2. config.yaml

This file defines your prospecting parameters and bot behavior.

-   `target_roles:` A list of job titles to target (e.g., "Chief Technology Officer", "VP of Sales").
-   `target_industries:` A list of industries to focus on (e.g., "Software Development", "Financial Services").
-   `target_locations:` A list of geographic locations to search within.
-   `contact_once_per_company: [True/False]` Set to `True` to contact only one prospect per company.
-   `company_blacklist:` A list of companies to exclude from your search.
-   `title_blacklist:` A list of keywords in job titles to avoid (e.g., "Intern", "Assistant").
-   `llm_model_type`: Choose the model provider: `openai`, `ollama`, `claude`, or `gemini`.
-   `llm_model`: Specify the model name (e.g., `gpt-4o`, `claude-3-opus-20240229`).

### 3. contact_form_config.yaml

This file maps field names found on website contact forms to the data used to fill them. This allows the bot to correctly fill out forms on different websites.

-   `field_mappings:`
    -   `first_name:` List of possible HTML `name` attributes for the first name field (e.g., `['fname', 'first_name']`).
    -   `last_name:` List for the last name field.
    -   `email:` List for the email field.
    -   `phone:` List for the phone number field.
    -   `company:` List for the company name field.
    -   `message:` List for the main message/comment box.
-   `submit_button_selectors:` A list of CSS selectors or text to identify the form submission button.

## Usage

1.  **Configure Your Campaign:**
    Ensure your `data_folder` contains correctly filled-out `secrets.yaml`, `config.yaml`, and `contact_form_config.yaml` files.

2.  **Run the Bot:**
    Execute the main script to start your outreach campaign. The bot will use your configuration to find prospects, generate personalized messages, and contact them.
    ```bash
    python run_contact_campaign.py
    ```

3.  **Scrape-Only Mode:**
    To collect prospect data without sending any messages, run in scrape-only mode. This is useful for building lead lists for manual review.
    ```bash
    python run_contact_campaign.py --scrape-only
    ```

4.  **Review Output:**
    The `output/` directory will contain JSON files tracking the campaign's progress:
    -   `prospects.json`: A list of all identified prospects.
    -   `contacted.json`: Prospects that were successfully contacted.
    -   `failed.json`: Outreach attempts that failed.
    -   `skipped.json`: Prospects that were skipped due to blacklisting or other rules.

## Troubleshooting

#### 1. LLM API Rate Limit Errors
-   **Solution:** Check your API billing settings and usage limits on your provider's dashboard (OpenAI, Anthropic, etc.). If you are on a free tier, consider upgrading or adding credits to increase your rate limits.

#### 2. Contact Form Submission Errors
-   **Issue:** The bot fails to fill or submit a website's contact form.
-   **Solution:** Websites have unique form structures. Update your `contact_form_config.yaml` with the correct `name` attributes and selectors for the target website's form fields and submit button. Inspect the website's HTML to find these values.

#### 3. Bot Fails to Find Prospects
-   **Issue:** The bot runs but doesn't find any leads.
-   **Solution:**
    -   Broaden your search criteria in `config.yaml` (e.g., add more roles or locations).
    -   Ensure your configuration files are correctly formatted and complete.

## Documentation

### For Developers

-   [Workflow Diagrams](docs/workflow_diagrams.md): Understand the architecture and data flow of the application.
-   [LangChain Developer Documentation](https://python.langchain.com/v0.2/docs/integrations/components/): Learn more about the LLM framework used in this project.

#### Automating Documentation

To generate and view developer documentation:

```bash
pip install -U sphinx furo
sphinx-quickstart
make html
open build/html/index.html
```

## Conclusion

ProspectAI Navigator provides a significant advantage in the modern sales landscape by automating and enhancing the prospecting process. With features like AI-powered personalization and multi-channel outreach, it offers unparalleled efficiency. By leveraging cutting-edge automation, this tool not only saves countless hours but also significantly increases the effectiveness of your outreach campaigns.

## Contributors

ProspectAI Navigator is an evolving project. Your feedback, suggestions, and contributions are highly valued. Feel free to open issues, suggest enhancements, or submit pull requests to help improve the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is intended for educational and professional purposes only. The creator assumes no responsibility for any consequences arising from its use. Users are advised to comply with the terms of service of all relevant platforms and adhere to applicable laws and regulations (e.g., GDPR, CAN-SPAM). The use of automated tools may carry risks; proceed with caution and at your own discretion.
>>>>>>> d46392347ef9862ae14f4663f5d6fe6ed03dda1b
