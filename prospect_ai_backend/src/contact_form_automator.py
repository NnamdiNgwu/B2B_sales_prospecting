
import time
import random
import os
from typing import Dict, List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from loguru import logger
import src.utils as utils  # Leverage existing utilities

class ContactFormAutomator:
    """
    Enhanced automator for B2B contact forms with GPT integration for personalization.
    Adapts ai_job_hunt's logic for form filling, now with dynamic GPT-powered messaging.
    """

    def __init__(self, driver, gpt_answerer=None, output_dir=None):
        self.driver = driver
        self.gpt_answerer = gpt_answerer  # GPT integration for personalization
        self.output_dir = output_dir
        # check if output directory exists before using it
        if self.output_dir:
            os.makedirs(self.output_dir, exist_ok=True)
            logger.info(f"Output directory ensured: {self.output_dir}")
        else:
            logger.warning("No output directory specified, results may not be saved.")

        # B2B-specific selectors (unchanged, but now GPT-enhanced)
        self.form_selectors = {
            'name': [
                'input[name*="name" i]', 'input[name*="first" i]', 'input[name*="full" i]',
                'input[placeholder*="name" i]', 'input[id*="name" i]', 'input[class*="name" i]',
                '#name', '#fullname', '#contact-name', '.name-input',
                'input[aria-label*="name" i]', 'input[aria-describedby*="name" i]', 'input[autocomplete*="name"]'
            ],
            'email': [
                'input[type="email"]', 'input[name*="email" i]', 'input[name*="mail" i]',
                'input[placeholder*="email" i]', 'input[id*="email" i]', 'input[class*="email" i]',
                '#email', '#contact-email', '.email-input',
                'input[aria-label*="email" i]', 'input[aria-describedby*="email" i]', 'input[autocomplete*="email"]'
            ],
            'phone': [
                'input[type="tel"]', 'input[name*="phone" i]', 'input[name*="mobile" i]',
                'input[name*="tel" i]', 'input[placeholder*="phone" i]', 'input[id*="phone" i]',
                '#phone', '#contact-phone', '.phone-input',
                'input[aria-label*="phone" i]', 'input[aria-describedby*="phone" i]'
            ],
            'subject': [
                'input[name*="subject" i]', 'input[name*="topic" i]', 'select[name*="subject" i]',
                'input[placeholder*="subject" i]', 'input[id*="subject" i]',
                '#subject', '#contact-subject', 'input[aria-label*="subject" i]', 'input[data-form-field-id*="subject"]'
            ],
            'message': [
                'textarea[name*="message" i]', 'textarea[name*="comment" i]', 'textarea[name*="inquiry" i]',
                'textarea[name*="comments" i]', 'textarea[placeholder*="message" i]', 
                'textarea[placeholder*="comment" i]', 'textarea[id*="message" i]', 
                'textarea[class*="message" i]', '#message', '#comments', '#contact-message', 
                '.message-textarea', 'textarea[aria-label*="message" i]', 'textarea[data-form-field-id*="message"]'
            ],
            'country': [
                'select[name*="country" i]', 'input[name*="country" i]',
                'select[id*="country" i]', '#country', '.country-select',
                'select[aria-label*="country" i]', 'input[aria-label*="country" i]', 'select[data-form-field-id*="country"]'
            ],
            'company': [
                'input[name*="company" i]', 'input[name*="organization" i]',
                'input[placeholder*="company" i]', 'input[id*="company" i]',
                '#company', '#organization', 'input[aria-label*="company" i]'
            ],
            'items_needed': [
                'input[name*="items" i]', 'input[name*="product" i]', 'textarea[name*="items" i]',
                'input[placeholder*="what items" i]', 'input[placeholder*="products" i]',
                'textarea[placeholder*="what items" i]', 'textarea[placeholder*="products" i]',
                '#items-needed', '#products', 'input[aria-label*="items" i]'
            ],
            'submit': [
                'button[type="submit"]', 'input[type="submit"]', 'button[name*="submit" i]',
                'button[id*="submit" i]', 'button[class*="submit" i]', '.submit-btn',
                'button:contains("Submit")', 'button:contains("Send")', 'button:contains("Contact")',
                'button:contains("Request")', 'button:contains("Submit RFQ")', 'button:contains("Quote")',
                'button:contains("Get Quote")', 'button:contains("Send Message")',
                'button[aria-label*="submit" i]', 'button[aria-label*="send" i]'
            ]
        }
        logger.info("ContactFormAutomator initialized with GPT support")

    def submit_contact_form(self, website_url: str, contact_data: Dict[str, str]) -> Dict[str, any]:
        """Main method with GPT-enhanced personalization."""
        logger.info(f"Starting GPT-enhanced contact form submission for: {website_url}")
        try:
            self.driver.get(website_url)
            time.sleep(random.uniform(2, 4))
            
            form_type = self._detect_form_type()
            logger.info(f"Detected form type: {form_type}")
            
            # GPT: Personalize data based on website content
            # personalized_data = self._personalize_with_gpt(contact_data, website_url, form_type)
            # Pass only the original message to the personalization method
            original_message = contact_data.get('message', '')
            personalized_message = self._personalize_with_gpt(original_message)
            contact_data['message'] = personalized_message

            form_result = self._find_and_fill_form(contact_data, form_type)
            if not form_result['success']:
                return {'success': False, 'error': form_result['error'], 'website': website_url, 'form_type': form_type}
            
            submit_result = self._submit_form()
            return {
                'success': submit_result['success'],
                'website': website_url,
                # 'form_data': personalized_data,
                'form_data': contact_data,
                'form_type': form_type,
                'submission_time': time.time(),
                'error': submit_result.get('error'),
                'confirmation_message': submit_result.get('confirmation')
            }
        except Exception as e:
            logger.error(f"Error submitting contact form for {website_url}: {str(e)}")
            return {'success': False, 'error': str(e), 'website': website_url}
    

    def _personalize_with_gpt(self, original_message: str) -> str:
        """Personalize the contact message using the B2BMessagePersonalizer."""
        if not self.gpt_answerer:
            logger.warning("GPT personalizer not available, using default message.")
            return original_message
        
        try:
            # Get website content for context, limiting to a reasonable size
            website_content = self.driver.find_element(By.TAG_NAME, "body").text[:4000]

            # Call the new, dedicated personalization method
            personalized_message = self.gpt_answerer.personalize_message(
                website_content=website_content,
                original_message=original_message
            )
            logger.info("GPT successfully personalized the message.")
            return personalized_message

        except Exception as e:
            logger.warning(f"GPT personalization failed: {e}, falling back to the original message.")
            return original_message

    
    # def _personalize_with_gpt(self, contact_data: Dict[str, str], website_url: str, form_type: str) -> Dict[str, str]:
    #     """Enhanced GPT personalization with caching and better prompts."""
    #     if not self.gpt_answerer:
    #         logger.warning("GPT not available, using default data")
    #         return contact_data
        
    #     try:
    #         page_text = self.driver.find_element(By.TAG_NAME, 'body').text[:500]
    #         company_name = self._extract_company_from_url(website_url)
            
    #         # Improved prompt with industry context
    #         prompt = f"""
    #         Website content: "{page_text}"
    #         Company: "{company_name}"
    #         Form type: "{form_type}"
            
    #         Personalize this B2B inquiry message. Make it professional, concise (<150 words), and relevant to their industry/services.
    #         Original: "{contact_data.get('message', '')}"
            
    #         Focus on partnership potential.
    #         """
            
    #         personalized_message = self.gpt_answerer.answer_question_textual_wide_range(prompt)
    #         if personalized_message:
    #             contact_data['message'] = personalized_message.strip()
    #             logger.info(f"GPT personalized for {company_name}")
            
    #         # Subject personalization
    #         if form_type == 'request_quote':
    #             subject_prompt = f"Create a subject line for a quote request to {company_name} in their industry."
    #             personalized_subject = self.gpt_answerer.answer_question_textual_wide_range(subject_prompt)
    #             if personalized_subject:
    #                 contact_data['subject'] = personalized_subject.strip()
        
    #     except Exception as e:
    #         logger.warning(f"GPT failed: {e}, falling back to defaults")
        
    #     return contact_data

    def _extract_company_from_url(self, url: str) -> str:
        """Extract company name from URL for GPT context."""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            return domain.split('.')[0].replace('www', '').title()
        except:
            return "the company"


    def _detect_form_type(self) -> str:
        """Detect the type of contact form based on page content"""
        try:
            page_text = self.driver.page_source.lower()
            title_text = self.driver.title.lower()
            
            # Check for specific form types
            if any(keyword in page_text or keyword in title_text for keyword in 
                   ['contact us', 'contact-us', 'get in touch', 'reach us']):
                return 'contact_us'
            elif any(keyword in page_text or keyword in title_text for keyword in 
                     ['request quote', 'quote request', 'get quote', 'rfq']):
                return 'request_quote'
            elif any(keyword in page_text or keyword in title_text for keyword in 
                     ['inquiry', 'send message', 'contact form']):
                return 'general_inquiry'
            else:
                return 'unknown'
                
        except Exception as e:
            logger.warning(f"Error detecting form type: {e}")
            return 'unknown'

    def _find_and_fill_form(self, contact_data: Dict[str, str], form_type: str) -> Dict[str, any]:
        """Enhanced form finding and filling with required field detection"""
        try:
            form = self._find_form_element()
            if not form:
                return {'success': False, 'error': 'No contact form found'}
            
            # Get required fields
            required_fields = self._get_required_fields(form)
            logger.info(f"Required fields detected: {required_fields}")
            
            # Fill form fields
            filled_fields = {}
            missing_required = []
            
            for field_type, selectors in self.form_selectors.items():
                if field_type == 'submit':
                    continue
                    
                field_value = contact_data.get(field_type)
                if not field_value and field_type in required_fields:
                    missing_required.append(field_type)
                    continue
                
                if field_value:
                    field_element = self._find_field_element(form, selectors)
                    if field_element:
                        self._fill_field(field_element, field_value, field_type)
                        filled_fields[field_type] = field_value
                        time.sleep(random.uniform(0.5, 1.5))
            
            if missing_required:
                return {
                    'success': False, 
                    'error': f'Missing required fields: {missing_required}'
                }
            
            if not filled_fields:
                return {'success': False, 'error': 'No form fields could be filled'}
            
            return {
                'success': True, 
                'filled_fields': filled_fields,
                'required_fields': required_fields,
                'form_element': form
            }
            
        except Exception as e:
            logger.error(f"Error finding/filling form: {e}")
            return {'success': False, 'error': str(e)}
    

    def _get_required_fields(self, form: WebElement) -> List[str]:
        """Detect required fields by checking for 'required' attributes, asterisks in labels, and parent classes."""
        required_fields = set()
        
        try:
            # Strategy 1: Find all elements with 'required' or 'aria-required="true"'
            required_elements = form.find_elements(By.CSS_SELECTOR, '[required], [aria-required="true"]')
            
            # Strategy 2: Find labels containing a '*' and get their associated input
            asterisk_labels = form.find_elements(By.XPATH, ".//label[contains(.,'*')]")
            for label in asterisk_labels:
                try:
                    # Find input associated by 'for' attribute
                    input_id = label.get_attribute('for')
                    if input_id:
                        element = form.find_element(By.ID, input_id)
                        required_elements.append(element)
                except NoSuchElementException:
                    continue

            # Strategy 3: Find parent containers with a 'required' class
            required_containers = form.find_elements(By.CSS_SELECTOR, '[class*="required"]')
            for container in required_containers:
                try:
                    # Find the first input, textarea, or select within this container
                    element = container.find_element(By.CSS_SELECTOR, 'input, textarea, select')
                    required_elements.append(element)
                except NoSuchElementException:
                    continue
            
             # For each identified required element, determine its field type
            for element in required_elements:
                for field_type, selectors in self.form_selectors.items():
                    if field_type == 'submit':
                        continue
                    # Check if the element matches any of the selectors for a given field type
                    for selector in selectors:
                        try:
                            # This is a trick to check if an element matches a selector
                            if element.get_attribute('outerHTML') == form.find_element(By.CSS_SELECTOR, f'{selector}[outerHTML="{element.get_attribute("outerHTML")}"]').get_attribute('outerHTML'):
                                required_fields.add(field_type)
                                break # Move to the next element once type is found
                        except:
                            continue
                    if field_type in required_fields:
                        break # Already found type for this element

        except Exception as e:
            logger.warning(f"Error detecting required fields: {e}")
        
        return list(required_fields) # Remove duplicates

    # def _get_required_fields(self, form: WebElement) -> List[str]:
    #     """Detect required fields based on labels, asterisks, and aria-required"""
    #     required_fields = []
        
    #     try:
    #         # Look for labels with asterisks
    #         labels = form.find_elements(By.TAG_NAME, 'label')
    #         for label in labels:
    #             label_text = label.text.lower().strip()
    #             if '*' in label_text or 'required' in label_text:
    #                 # Map label text to field type
    #                 if any(word in label_text for word in ['name', 'your name', 'full name']):
    #                     required_fields.append('name')
    #                 elif 'email' in label_text:
    #                     required_fields.append('email')
    #                 elif any(word in label_text for word in ['phone', 'telephone', 'mobile']):
    #                     required_fields.append('phone')
    #                 elif any(word in label_text for word in ['subject', 'topic']):
    #                     required_fields.append('subject')
    #                 elif any(word in label_text for word in ['country']):
    #                     required_fields.append('country')
    #                 elif any(word in label_text for word in ['company', 'organization']):
    #                     required_fields.append('company')
            
    #         # Check for aria-required attributes
    #         inputs = form.find_elements(By.TAG_NAME, 'input')
    #         textareas = form.find_elements(By.TAG_NAME, 'textarea')
    #         selects = form.find_elements(By.TAG_NAME, 'select')
            
    #         for element in inputs + textareas + selects:
    #             if element.get_attribute('aria-required') == 'true' or element.get_attribute('required') is not None:
    #                 field_name = element.get_attribute('name') or element.get_attribute('id') or ''
    #                 field_name = field_name.lower()
                    
    #                 if 'name' in field_name:
    #                     required_fields.append('name')
    #                 elif 'email' in field_name:
    #                     required_fields.append('email')
    #                 elif 'phone' in field_name or 'tel' in field_name:
    #                     required_fields.append('phone')
    #                 elif 'subject' in field_name:
    #                     required_fields.append('subject')
    #                 elif 'country' in field_name:
    #                     required_fields.append('country')
    #                 elif 'company' in field_name:
    #                     required_fields.append('company')
        
    #     except Exception as e:
    #         logger.warning(f"Error detecting required fields: {e}")
        
    #     return list(set(required_fields))  # Remove duplicates

    def _find_form_element(self) -> Optional[WebElement]:
        """Enhanced form detection with more patterns"""
        form_selectors = [
            'form[action*="contact"]', 'form[action*="submit"]', 'form[action*="send"]',
            'form[name*="contact"]', 'form[id*="contact"]', 'form[class*="contact"]',
            '.contact-form', '#contact-form', '#contactForm',
            'form:has(input[type="email"])', 'form:has(textarea)',
            'form:has(button[type="submit"])', 'form:has(input[name*="email"])',
            '.wpcf7-form', '.gform_wrapper form',  # Common form plugins
            '.contact-form form', '.quote-form', '.inquiry-form'
        ]
        
        for selector in form_selectors:
            try:
                if selector.startswith('.'):
                    forms = self.driver.find_elements(By.CLASS_NAME, selector[1:])
                elif selector.startswith('#'):
                    forms = self.driver.find_elements(By.ID, selector[1:])
                else:
                    forms = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                if forms:
                    # Return the form with the most input fields
                    return max(forms, key=lambda f: len(f.find_elements(By.TAG_NAME, 'input')))
                    
            except Exception:
                continue
        
        return None
    

    def _find_field_element(self, form: WebElement, selectors: List[str]) -> Optional[WebElement]:
        """Find a field element by trying CSS selectors first, then by searching for its visible label text."""
        # Strategy 1: Try direct CSS selectors
        for selector in selectors:
            try:
                element = form.find_element(By.CSS_SELECTOR, selector)
                if element and element.is_displayed() and element.is_enabled():
                    return element
            except NoSuchElementException:
                continue
        
        # Strategy 2: Find by label text (more robust for complex forms)
        # Extract potential label texts from selectors (e.g., 'name' from 'input[name*="name"]')
        label_texts = set()
        for s in selectors:
            if 'name' in s: label_texts.add('name')
            if 'email' in s: label_texts.add('email')
            if 'phone' in s: label_texts.add('phone')
            if 'company' in s: label_texts.add('company')
            if 'subject' in s: label_texts.add('subject')
            if 'message' in s: label_texts.add('message')

        for text in label_texts:
            try:
                # Find the label that contains the text, case-insensitive
                label = form.find_element(By.XPATH, f".//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text}')]")
                input_id = label.get_attribute('for')
                if input_id:
                    element = form.find_element(By.ID, input_id)
                    if element.is_displayed() and element.is_enabled():
                        return element
            except NoSuchElementException:
                continue

        return None
    
    

    # def _find_field_element(self, form: WebElement, selectors: List[str]) -> Optional[WebElement]:
    #     """Enhanced field finding with better selector matching"""
    #     for selector in selectors:
    #         try:
    #             if selector.startswith('#'):
    #                 element = form.find_element(By.ID, selector[1:])
    #             elif selector.startswith('.'):
    #                 element = form.find_element(By.CLASS_NAME, selector[1:])
    #             elif ':contains' in selector:
    #                 # Handle text-based selectors
    #                 search_text = selector.split('"')[1]
    #                 elements = form.find_elements(By.XPATH, f".//*[contains(text(), '{search_text}')]")
    #                 if elements:
    #                     # Look for associated input
    #                     for elem in elements:
    #                         try:
    #                             input_elem = elem.find_element(By.XPATH, "./following::input[1]") or \
    #                                        elem.find_element(By.XPATH, "./preceding::input[1]")
    #                             if input_elem.is_displayed():
    #                                 return input_elem
    #                         except:
    #                             continue
    #                 continue
    #             else:
    #                 element = form.find_element(By.CSS_SELECTOR, selector)
                
    #             if element and element.is_displayed() and element.is_enabled():
    #                 return element
                    
    #         except NoSuchElementException:
    #             continue
        
    #     return None

    def _fill_field(self, element: WebElement, value: str, field_type: str):
        """Enhanced field filling with better handling of different input types"""
        try:
            # Clear existing value
            element.clear()
            time.sleep(0.2)
            
            # Handle select dropdowns
            if element.tag_name.lower() == 'select':
                
                select = Select(element)
                try:
                    select.select_by_visible_text(value)
                    logger.debug(f"Selected dropdown option: {value}")
                    return
                except:
                    # If exact match fails, try partial match
                    options = [opt.text for opt in select.options]
                    for opt_text in options:
                        if value.lower() in opt_text.lower():
                            select.select_by_visible_text(opt_text)
                            logger.debug(f"Selected partial match: {opt_text}")
                            return
            
            # Handle text inputs and textareas
            # Type the value with human-like delays
            for char in value:
                element.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            logger.debug(f"Filled {field_type} field with: {value}")
            
        except Exception as e:
            logger.warning(f"Error filling {field_type} field: {e}")

    def _submit_form(self) -> Dict[str, any]:
        """Enhanced form submission with multiple submit button strategies"""
        try:
            # Find submit button
            submit_button = self._find_submit_button()
            if not submit_button:
                return {'success': False, 'error': 'Submit button not found'}
            
            # Scroll to submit button
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)
            
            # Click submit button
            submit_button.click()
            time.sleep(2)
            
            # Check for success indicators
            return self._check_submission_success()
            
        except ElementClickInterceptedException:
            logger.warning("Submit button click intercepted, trying JavaScript click")
            try:
                self.driver.execute_script("arguments[0].click();", submit_button)
                time.sleep(2)
                return self._check_submission_success()
            except Exception as e:
                return {'success': False, 'error': f'JavaScript click failed: {str(e)}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _find_submit_button(self) -> Optional[WebElement]:
        """Enhanced submit button detection"""
        submit_selectors = self.form_selectors['submit']
        
        for selector in submit_selectors:
            try:
                if ':contains' in selector:
                    # Handle text-based selectors
                    button_text = selector.split('"')[1]
                    buttons = self.driver.find_elements(By.XPATH, f"//button[contains(text(), '{button_text}')]")
                    if buttons:
                        return buttons[0]
                else:
                    if selector.startswith('#'):
                        button = self.driver.find_element(By.ID, selector[1:])
                    elif selector.startswith('.'):
                        button = self.driver.find_element(By.CLASS_NAME, selector[1:])
                    else:
                        button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if button.is_displayed() and button.is_enabled():
                        return button
                        
            except NoSuchElementException:
                continue
        
        return None

    def _check_submission_success(self) -> Dict[str, any]:
        """Enhanced success detection with more patterns"""
        try:
            # Wait for page changes or success messages
            time.sleep(3)
            
            # Check for success indicators
            success_indicators = [
                'thank you', 'message sent', 'form submitted', 'success',
                'confirmation', 'we received your message', 'thank you for contacting',
                'thank you for your inquiry', 'your request has been submitted',
                'quote request received', 'we will contact you soon'
            ]
            
            page_text = self.driver.page_source.lower()
            
            for indicator in success_indicators:
                if indicator in page_text:
                    return {
                        'success': True,
                        'confirmation': f"Found success indicator: '{indicator}'"
                    }
            
            # Check if redirected to thank you page
            current_url = self.driver.current_url.lower()
            if any(word in current_url for word in ['thank', 'success', 'confirmation', 'submitted']):
                return {
                    'success': True,
                    'confirmation': f"Redirected to success page: {current_url}"
                }
            
            # Check for form disappearance (common success indicator)
            try:
                form = self._find_form_element()
                if not form:
                    return {
                        'success': True,
                        'confirmation': 'Contact form no longer visible (likely submitted successfully)'
                    }
            except:
                pass
            
            # Check for specific success elements
            try:
                success_elements = self.driver.find_elements(By.XPATH, 
                    "//*[contains(@class, 'success') or contains(@class, 'thank') or contains(@class, 'confirmation')]")
                if success_elements:
                    return {
                        'success': True,
                        'confirmation': 'Found success/confirmation element on page'
                    }
            except:
                pass
            
            # If no clear success indicators, assume success if no error messages
            error_indicators = ['error', 'failed', 'invalid', 'required', 'please try again', 'field is required']
            has_errors = any(indicator in page_text for indicator in error_indicators)
            
            if not has_errors:
                return {
                    'success': True,
                    'confirmation': 'No error messages found, assuming successful submission'
                }
            else:
                return {
                    'success': False,
                    'error': 'Error messages detected on page'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error checking submission success: {str(e)}'
            }