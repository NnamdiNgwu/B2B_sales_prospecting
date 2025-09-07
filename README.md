
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
