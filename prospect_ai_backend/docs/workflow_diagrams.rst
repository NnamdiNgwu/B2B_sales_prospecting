#############################
ProspectAI Navigator Workflows
#############################

Note: All diagrams are created using Mermaid.

1. Main Campaign Flow
=====================

This diagram shows the high-level process from starting the application to completing a B2B outreach campaign.

.. mermaid::

   graph TD
       A[Start] --> B[Parse Command Line Arguments]
       B --> C[Load Configuration (YAML files)]
       C --> D[Initialize Components (Scraper, Automator, LLM)]
       D --> E{Scrape-Only Mode?}
       E -->|Yes| F[Scrape Prospects & Company Info]
       F --> G[Save Prospects to JSON]
       G --> H[End]
       E -->|No| I[Start Outreach Campaign]
       I --> J[Load Prospects to Contact]
       J --> K{For each Prospect}
       K --> L[Find Company Website & Contact Form]
       L --> M[Personalize Message with LLM]
       M --> N[Automate Contact Form Submission]
       N --> O[Log Result (Contacted, Failed, Skipped)]
       O --> K
       K --> P[Generate Final Reports]
       P --> H

2. Contact Form Submission Process
=================================

This sequence diagram details the interaction between different components when submitting a single contact form.

.. mermaid::

   sequenceDiagram
       participant User
       participant ProspectAINavigator
       participant WebsiteScraper
       participant B2BMessagePersonalizer
       participant ContactFormAutomator

       User->>ProspectAINavigator: Run run_contact_campaign.py
       ProspectAINavigator->>WebsiteScraper: Find company website for Prospect 'X'
       WebsiteScraper-->>ProspectAINavigator: Return website URL
       ProspectAINavigator->>ContactFormAutomator: Navigate to website and find contact form
       ContactFormAutomator-->>ProspectAINavigator: Confirm form found
       ProspectAINavigator->>B2BMessagePersonalizer: Generate message for Prospect 'X' at Company 'Y'
       B2BMessagePersonalizer-->>ProspectAINavigator: Return personalized message
       ProspectAINavigator->>ContactFormAutomator: Fill form with prospect data and personalized message
       ContactFormAutomator->>ContactFormAutomator: Handle potential CAPTCHA (pause for user)
       ContactFormAutomator->>ContactFormAutomator: Submit form
       ContactFormAutomator-->>ProspectAINavigator: Return submission status (Success/Fail)
       ProspectAINavigator->>ProspectAINavigator: Log result to output JSON file

3. Message Personalization Process
=================================

This diagram outlines how a generic message is tailored for a specific prospect using an LLM.

.. mermaid::

   graph TD
       A[Start Message Personalization] --> B[Get Prospect & Company Details]
       B --> C[Construct Prompt for LLM]
       C --> D[Send Prompt to LLM (e.g., GPT-4, Claude)]
       D --> E[Receive Personalized Message]
       E --> F[Return Formatted Message Text]
       F --> G[End Personalization]

4. LLM Manager Workflow
========================

This shows the general flow for any interaction with the configured Large Language Model.

.. mermaid::

   graph LR
       A[Receive Text Prompt] --> B[Prepare API Request]
       B --> C[Send to LLM API Endpoint]
       C --> D[Receive API Response]
       D --> E[Parse Response JSON]
       E --> F[Return Formatted Text]