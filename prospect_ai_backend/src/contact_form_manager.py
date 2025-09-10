import time
import random
import json
from pathlib import Path
from typing import Dict, List, Optional
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import src.utils as utils
from src.contact_form_automator import ContactFormAutomator
from loguru import logger

class ContactFormManager:
    """
    Enhanced manager for B2B contact form automation with form type awareness
    """
    
    def __init__(self, driver):
        # super().__init__(driver)  # Correct call passing only the driver
        self.driver = driver
        self.gpt_answerer = None  # Placeholder for LLM integration
        self.contact_automator = None
        self.output_file_directory = None
        self.contact_data = {}
        self.websites = []
        self.submission_results = []
        self.form_type_config = {}
        
        logger.info("Enhanced ContactFormManager initialized")
    

    def set_gpt_answerer(self, gpt_answerer):
        """Set GPT answerer (adapted from original's set_gpt_answerer_and_resume_generator)"""
        self.gpt_answerer = gpt_answerer

    def set_parameters(self, parameters: Dict, output_dir: Path):
        """Set enhanced parameters for contact form automation"""
        logger.info("Setting enhanced parameters for ContactFormManager")
        # self.parameters = parameters
        # contact_params = parameters.get('contact_campaign', {})
        # websites = contact_params.get('websites', [])
        # logger.info(f"Parameters set: {len(websites)} websites to contact")
    # ... rest

        self.contact_data = {
            'name': parameters.get('name'),
            'email': parameters.get('email'),
            'phone': parameters.get('phone'),
            'company': parameters.get('company'),
            'subject': parameters.get('subject'),
            'message': parameters.get('message'),
            'country': parameters.get('country'),
            'items_needed': parameters.get('items_needed')
        }
        
        self.websites = parameters.get('websites', [])
        self.form_types = parameters.get('form_types', {})

        self.output_file_directory = output_dir
        self.output_file_directory.mkdir(exist_ok=True)
        
        # Form type configurations
        self.form_type_config = parameters.get('form_types', {})
        
        # Rate limiting settings
        self.delay_between_submissions = parameters.get('delay_between_submissions', 30)
        self.max_submissions_per_hour = parameters.get('max_submissions_per_hour', 20)

        # This log should report the number of websites to contact
        logger.info(f"Parameters set: {len(self.websites)} websites to contact")

    def start_contact_campaign(self):
        """Start the enhanced contact form submission campaign"""
        logger.info("Starting enhanced contact form submission campaign")
        # contact_params = self.parameters.get('contact_campaign', {})
        # websites = contact_params.get('websites', [])
        
        self.contact_automator = ContactFormAutomator(self.driver, self.gpt_answerer, self.output_file_directory)
        
        successful_submissions = 0
        hourly_submissions = 0
        hour_start_time = time.time()

        for i, website_url in enumerate(self.websites):
            logger.info(f"Processing website {i+1}/{len(self.websites)}: {website_url}")

            try:
                # Check hourly rate limit
                if hourly_submissions >= self.max_submissions_per_hour:
                    elapsed_time = time.time() - hour_start_time
                    if elapsed_time < 3600:
                        sleep_time = 3600 - elapsed_time
                        logger.info(f"Hourly limit reached. Sleeping for {sleep_time/60:.1f} minutes")
                        time.sleep(sleep_time)
                        hourly_submissions = 0
                        hour_start_time = time.time()
                
                # Submit contact form
                result = self.contact_automator.submit_contact_form(website_url, self.contact_data)
                
                # Record result
                self.submission_results.append(result)
                self._write_result_to_file(result)
                
                if result['success']:
                    successful_submissions += 1
                    hourly_submissions += 1
                    logger.info(f"✅ Successfully submitted contact form for {website_url}")
                    logger.info(f"   Form type: {result.get('form_type', 'unknown')}")
                    logger.info(f"   Confirmation: {result.get('confirmation_message', 'N/A')}")
                else:
                    logger.warning(f"❌ Failed to submit contact form for {website_url}: {result.get('error', 'Unknown error')}")
                
                # Delay between submissions
                if i < len(self.websites) - 1:
                    logger.info(f"Waiting {self.delay_between_submissions} seconds before next submission")
                    time.sleep(self.delay_between_submissions)
                    
            except Exception as e:
                logger.error(f"Unexpected error processing {website_url}: {str(e)}")
                error_result = {
                    'success': False,
                    'error': str(e),
                    'website': website_url,
                    'submission_time': time.time()
                }
                self.submission_results.append(error_result)
                self._write_result_to_file(error_result)
        
        # Generate enhanced campaign summary
        self._generate_campaign_summary(successful_submissions)

    def _write_result_to_file(self, result: Dict):
        """Write submission result to appropriate file with enhanced data"""
        status = 'success' if result['success'] else 'failed'
        file_path = self.output_file_directory / f"contact_submissions_{status}.json"
        
        # Prepare enhanced data for JSON storage
        json_data = {
            'website': result['website'],
            'success': result['success'],
            'form_type': result.get('form_type', 'unknown'),
            'submission_time': result.get('submission_time', time.time()),
            'contact_data': result.get('form_data', {}),
            'error': result.get('error'),
            'confirmation_message': result.get('confirmation_message'),
            'required_fields_detected': result.get('required_fields', []),
            'filled_fields': result.get('filled_fields', [])
        }
        
        # Write to file
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([json_data], f, indent=2)
        else:
            with open(file_path, 'r+', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
                existing_data.append(json_data)
                f.seek(0)
                json.dump(existing_data, f, indent=2)
                f.truncate()
        
        logger.debug(f"Enhanced result written to {file_path}")

    def _generate_campaign_summary(self, successful_submissions: int):
        """Generate enhanced campaign summary with form type analytics"""
        total_submissions = len(self.submission_results)
        success_rate = (successful_submissions / total_submissions * 100) if total_submissions > 0 else 0
        
        # Analyze form types
        form_type_stats = {}
        for result in self.submission_results:
            form_type = result.get('form_type', 'unknown')
            if form_type not in form_type_stats:
                form_type_stats[form_type] = {'total': 0, 'successful': 0}
            form_type_stats[form_type]['total'] += 1
            if result['success']:
                form_type_stats[form_type]['successful'] += 1
        
        summary = {
            'campaign_summary': {
                'total_websites': len(self.websites),
                'total_submissions': total_submissions,
                'successful_submissions': successful_submissions,
                'failed_submissions': total_submissions - successful_submissions,
                'success_rate': round(success_rate, 2),
                'campaign_start_time': getattr(self, 'campaign_start_time', time.time()),
                'campaign_end_time': time.time(),
                'average_delay': self.delay_between_submissions,
                'form_type_breakdown': form_type_stats
            },
            'results': self.submission_results
        }
        
        summary_file = self.output_file_directory / "campaign_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Enhanced campaign completed: {successful_submissions}/{total_submissions} successful submissions ({success_rate:.1f}% success rate)")
        logger.info("Form type breakdown:")
        for form_type, stats in form_type_stats.items():
            type_success_rate = (stats['successful'] / stats['total'] * 100) if stats['total'] > 0 else 0
            logger.info(f"  {form_type}: {stats['successful']}/{stats['total']} ({type_success_rate:.1f}%)")
        
        logger.info(f"Enhanced summary saved to {summary_file}")