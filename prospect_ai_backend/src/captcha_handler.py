import time
from typing import Dict, Optional

from loguru import logger
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class CaptchaHandler:
    """
    A class to detect and manage CAPTCHAs, supporting both manual
    and automated solving methods.
    """

    def __init__(self, driver: WebDriver, config: Optional[Dict] = None):
        """
        Initializes the CaptchaHandler.

        Args:
            driver: The Selenium WebDriver instance.
            config: A configuration dictionary, potentially containing API keys
                    for automated solving services (e.g., 'captcha_solver_api_key').
        """
        self.driver = driver
        self.config = config or {}
        self.captcha_selectors = [
            'iframe[src*="recaptcha"]',  # Google reCAPTCHA
            'iframe[src*="hcaptcha"]',   # hCaptcha
            '.cf-turnstile',             # Cloudflare Turnstile
            'div.g-recaptcha',
            'div.h-captcha'
        ]
        logger.debug("CaptchaHandler initialized.")

    def manage_captcha(self) -> bool:
        """
        Detects and handles a CAPTCHA if present. It prioritizes automated
        solving if configured, otherwise falls back to manual intervention.

        Returns:
            True if a CAPTCHA was detected, False otherwise.
        """
        if not self._is_captcha_present():
            logger.debug("No CAPTCHA detected.")
            return False

        logger.warning("CAPTCHA detected on the page.")
        
        # Provide room for automated solving
        if self.config.get("captcha_solver_api_key"):
            self._solve_automated()
        else:
            self._solve_manually()
        
        return True

    def _is_captcha_present(self) -> bool:
        """Checks if a known CAPTCHA element is visible on the page."""
        try:
            for selector in self.captcha_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and elements[0].is_displayed():
                    return True
            return False
        except Exception as e:
            logger.debug(f"Error while checking for CAPTCHA: {e}")
            return False

    def _solve_manually(self):
        """
        Pauses the script to allow for manual CAPTCHA solving.
        This is the "human-in-the-loop" pattern.
        """
        pause_duration = self.config.get("manual_captcha_timeout", 60)
        logger.info(f"Please solve the CAPTCHA manually. Script will pause for {pause_duration} seconds.")
        time.sleep(pause_duration)
        logger.info("Resuming script. Attempting to proceed with form submission.")


    
    def _solve_automated(self):
        """
        Integrates with a dedicated third-party CAPTCHA solving service.
        This is the standard, reliable approach for automation.
        """
        logger.info("Attempting to solve CAPTCHA with a dedicated service.")
        try:
            # 1. Find the CAPTCHA's site-key from the page's HTML
            site_key_element = self.driver.find_element(By.CSS_SELECTOR, '.g-recaptcha')
            site_key = site_key_element.get_attribute('data-sitekey')
            page_url = self.driver.current_url

            # 2. Send the site-key and URL to the solving service
            # (This would be a separate library/module for the service)
            from third_party_solver import CaptchaSolver 
            solver = CaptchaSolver(api_key=self.config["captcha_solver_api_key"])
            solution_token = solver.solve_recaptcha_v2(site_key, page_url)

            if solution_token:
                # 3. Inject the solution token into the page and submit
                # The service's documentation explains how to do this.
                # It usually involves executing JavaScript to set the value of a hidden textarea.
                self.driver.execute_script(
                    f"document.getElementById('g-recaptcha-response').innerHTML = '{solution_token}';"
                )
                logger.info("Successfully received and injected CAPTCHA solution.")
            else:
                logger.error("Failed to get a solution from the CAPTCHA service.")
                self._solve_manually() # Fallback to manual

        except Exception as e:
            logger.error(f"Automated CAPTCHA solving failed: {e}. Falling back to manual.")
            self._solve_manually()

    # def _solve_automated(self):
        # """
        # Placeholder for integrating an automated CAPTCHA solving service.
        # """
        # logger.info("Automated CAPTCHA solving is configured (but not yet implemented).")
        # # Example of future implementation:
        # # ---------------------------------
        # # api_key = self.config["captcha_solver_api_key"]
        # # solver = ThirdPartyCaptchaSolver(api_key)
        # # page_url = self.driver.current_url
        # # site_key = self._find_captcha_site_key() # e.g., data-sitekey attribute
        # # solution = solver.solve_recaptcha_v2(site_key, page_url)
        # # self._submit_captcha_solution(solution)
        # # logger.info("Attempted to solve CAPTCHA automatically.")
        # #
        # # For now, we fall back to manual as a placeholder.
        # logger.warning("Automated solver not implemented. Falling back to manual intervention.")
        # self._solve_manually()