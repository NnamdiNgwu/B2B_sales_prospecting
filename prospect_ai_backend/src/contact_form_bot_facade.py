from loguru import logger
from pathlib import Path
from src.contact_form_manager import ContactFormManager

class ContactFormBotState:
    def __init__(self):
        logger.debug("Initializing ContactFormBotState")
        self.reset()

    def reset(self):
        logger.debug("Resetting ContactFormBotState")
        self.parameters_set = False
        self.gpt_answerer_set = False
        self.driver_set = False

    def validate_state(self, required_keys):
        logger.debug(f"Validating ContactFormBotState with required keys: {required_keys}")
        for key in required_keys:
            if not getattr(self, key):
                logger.error(f"State validation failed: {key} is not set")
                raise ValueError(f"{key.replace('_', ' ').capitalize()} must be set before proceeding.")
        logger.debug("State validation passed")

class ContactFormBotFacade:
    def __init__(self, driver):
        logger.debug("Initializing ContactFormBotFacade")
        self.driver = driver
        self.state = ContactFormBotState()
        self.contact_manager = ContactFormManager(driver)
        # self.contact_manager.output_dir = output_dir
        self.parameters = None
        self.gpt_answerer = None

    def set_parameters(self, parameters, output_dir: Path):
        logger.debug("Setting parameters in facade")
        if not parameters:
            raise ValueError("Parameters cannot be empty.")
        self.parameters = parameters
        self.contact_manager.set_parameters(parameters, output_dir)  # Pass output_dir to manager
        self.state.parameters_set = True
        logger.debug("Parameters set successfully")

    def set_gpt_answerer(self, gpt_answerer):
        logger.debug("Setting GPT answerer in facade")
        if not gpt_answerer:
            raise ValueError("GPT answerer cannot be empty.")
        self.gpt_answerer = gpt_answerer
        self.contact_manager.set_gpt_answerer(gpt_answerer)  # Fixes AttributeError
        self.state.gpt_answerer_set = True
        logger.debug("GPT answerer set successfully")

    def start_contact_campaign(self):
        logger.debug("Starting contact campaign via facade")
        self.state.validate_state(['parameters_set', 'gpt_answerer_set'])
        self.contact_manager.start_contact_campaign()
        logger.debug("Contact campaign completed successfully")