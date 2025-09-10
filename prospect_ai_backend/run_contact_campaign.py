import os
import re
import sys
import yaml
import click
import jsonschema
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from src.contact_form_manager import ContactFormManager
from src.contact_form_bot_facade import ContactFormBotFacade
# from src.llm.llm_manager import GPTAnswerer  # Adapted from original
from src.llm.llm_manager import B2BMessagePersonalizer  # Adapted for B2B
from loguru import logger

class ConfigError(Exception):
    pass


class ConfigValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

    @staticmethod
    def validate_yaml_file(yaml_path: Path) -> dict:
        try:
            with open(yaml_path, 'r') as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise ConfigError(f"Error reading file {yaml_path}: {exc}")
        except FileNotFoundError:
            raise ConfigError(f"File not found: {yaml_path}")

    @staticmethod
    def validate_config(config_yaml_path: Path) -> dict:
        parameters = ConfigValidator.validate_yaml_file(config_yaml_path)
        if 'contact_campaign' not in parameters:
            raise ConfigError(f"Missing 'contact_campaign' section in config file {config_yaml_path}")
        contact_params = parameters['contact_campaign']
        
        # Separate required keys: top-level vs. nested under 'contact_campaign'
        top_level_required_keys = {
            'outputFileDirectory': str,  # Top-level keys from original/B2B
            'delay_between_submissions': int,
            'max_submissions_per_hour': int,
            'respect_robots_txt': bool,
            'user_agent': str,
            'max_retries': int
        }
        
        nested_required_keys = {
            'name': str,  # Nested under 'contact_campaign'
            'email': str,
            'websites': list,
            'llm_model_type': str,
            'llm_model': str,
            'llm_api_key': str,
            'form_types': dict
        }
        
        # Validate top-level keys
        for key, expected_type in top_level_required_keys.items():
            if key not in parameters:
                raise ConfigError(f"Missing top-level key '{key}' in config file {config_yaml_path}")
            elif not isinstance(parameters[key], expected_type):
                raise ConfigError(f"Invalid type for top-level key '{key}' in config file {config_yaml_path}. Expected {expected_type}.")
        
        # Validate nested keys under 'contact_campaign'
        for key, expected_type in nested_required_keys.items():
            if key not in contact_params:
                raise ConfigError(f"Missing nested key '{key}' under 'contact_campaign' in config file {config_yaml_path}")
            elif not isinstance(contact_params[key], expected_type):
                raise ConfigError(f"Invalid type for nested key '{key}' in config file {config_yaml_path}. Expected {expected_type}.")
        
        # Additional validations (adapted from original)
        if not ConfigValidator.validate_email(contact_params['email']):
            raise ConfigError(f"Invalid email in config file {config_yaml_path}")
        
        if not all(isinstance(site, str) for site in contact_params['websites']):
            raise ConfigError(f"'websites' must be a list of strings in config file {config_yaml_path}")
        
        if 'contact_us' not in contact_params['form_types'] or 'request_quote' not in contact_params['form_types']:
            raise ConfigError(f"'form_types' must include 'contact_us' and 'request_quote' in config file {config_yaml_path}")
        
        # Optional: Integrate JSON Schema for advanced validation (from config_schema.json)
        try:
            schema_path = config_yaml_path.parent / 'config_schema.json'  # Assume in same dir
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    schema = yaml.safe_load(f)  # Or json.load if it's JSON
                jsonschema.validate(parameters, schema)
                logger.info("JSON Schema validation passed")
        except ImportError:
            logger.warning("jsonschema not installed; skipping advanced validation")
        except jsonschema.ValidationError as e:
            raise ConfigError(f"JSON Schema validation failed: {e}")
        
        return parameters

class FileManager:
    @staticmethod
    def validate_config_file(config_path: Path) -> Path:
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        return config_path

def setup_chrome_driver():
    """Setup Chrome WebDriver (adapted from original init_browser)"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")

   
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def setup_and_run_campaign(config: dict, scrape_only: bool):
    """Initializes components and runs the specified campaign."""
    driver = None
    try:
        output_dir = Path(config['outputFileDirectory'])
        output_dir.mkdir(exist_ok=True)
        logger.info(f"Output directory set to {output_dir}")

        llm_api_key = os.getenv('OPENAI_API_KEY') or config['contact_campaign']['llm_api_key']
        if not llm_api_key:
            raise ConfigError("Missing OpenAI API key. Set OPENAI_API_KEY env var or in config.")

        message_personalizer = B2BMessagePersonalizer(config['contact_campaign'], llm_api_key)
        logger.info("B2B message personalizer initialized")

        driver = setup_chrome_driver()
        logger.info("Chrome WebDriver initialized")

        facade = ContactFormBotFacade(driver)
        facade.set_parameters(config['contact_campaign'], output_dir)
        facade.set_gpt_answerer(message_personalizer)

        if scrape_only:
            logger.info("Running in scrape-only mode. Data will be collected but not submitted.")
            # In the future, you would call a dedicated scraping method here.
            # facade.start_scraping_campaign() 
            logger.warning("Scrape-only mode is not fully implemented yet.")
        else:
            facade.start_contact_campaign()
        
        logger.info("Campaign completed successfully.")
    
    finally:
        if driver:
            driver.quit()
            logger.info("Chrome WebDriver closed")


@click.command()
@click.argument('config_path', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('--scrape-only', is_flag=True, help="Only collects prospect data without contacting them.")
def main(config_path: Path, scrape_only: bool):
    """
    Runs the ProspectAI Navigator bot to automate B2B outreach campaigns.

    CONFIG_PATH: The path to your YAML configuration file.
    """
    try:
        config = ConfigValidator.validate_config(config_path)
        logger.info(f"Loaded and validated configuration from {config_path}")
        setup_and_run_campaign(config, scrape_only)

    except (ConfigError, ValueError, FileNotFoundError) as e:
        logger.error(f"Configuration or setup error: {str(e)}")
        sys.exit(1)
    except WebDriverException as e:
        logger.error(f"WebDriver error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# def load_config(config_path: str) -> dict:
#     """Load and validate configuration (adapted from original)"""
#     config_file = Path(config_path)
#     FileManager.validate_config_file(config_file)
#     return ConfigValidator.validate_config(config_file)

# def main():
#     output_dir = None
#     if len(sys.argv) != 2:
#         print("Usage: python run_contact_campaign.py <config_file>")
#         sys.exit(1)

#     config_path = sys.argv[1]
#     driver = None
#     output_dir = None

#     try:
#         # Load and validate configuration (adapted from original)
#         # config = load_config(config_path)
#         config = ConfigValidator.validate_config(Path(config_path))
#         logger.info(f"Loaded and validated configuration from {config_path}")

#         # ensure output dir is set and assigned to the outer var
#         output_dir = Path(config['outputFileDirectory'])
#         output_dir.mkdir( exist_ok=True)
#         logger.info(f"Output directory set to {output_dir}")

#         # Setup GPT answerer (adapted from original GPTAnswerer creation)
#         llm_api_key = os.getenv('OPENAI_API_KEY') or config['contact_campaign']['llm_api_key']
#         if not llm_api_key:
#             raise ConfigError("Missing OpenAI API key. Set OPENAI_API_KEY env var or in config.")

#         message_personalizer = B2BMessagePersonalizer(config['contact_campaign'], llm_api_key)
#         logger.info("B2B message personalizer initialized")

#         # Setup WebDriver (adapted from original)
#         driver = setup_chrome_driver()
#         logger.info("Chrome WebDriver initialized")

#         # Initialize contact form manager and set GPT (fixes AttributeError)
#        # Use facade for state-managed setup (adapted from original AIHawkBotFacade)
       
#         facade = ContactFormBotFacade(driver)
#         facade.set_parameters(config['contact_campaign'], output_dir)  # Sets parameters and validates
#         # facade.set_gpt_answerer(gpt_answerer)  # Sets GPT and validates
#         facade.set_gpt_answerer(message_personalizer)

#         # Start the contact campaign via facade
#         facade.start_contact_campaign()
#         logger.info("Contact campaign completed successfully")

#     except (ConfigError, ValueError) as e:
#         logger.error(f"Configuration error: {str(e)}")
#     except WebDriverException as e:
#         logger.error(f"WebDriver error: {str(e)}")
#     except Exception as e:
#         logger.error(f" An unexpected error occurred: {str(e)}")
#         sys.exit(1)
#     finally:
#         if driver:
#             driver.quit()
#             logger.info("Chrome WebDriver closed")

# if __name__ == "__main__":
#     main()