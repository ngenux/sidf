import abc
import logging

class LLMClient(abc.ABC):
    """
    Abstract base class for Large Language Model (LLM) clients.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def get_response(self, prompt, **kwargs):
        """
        Abstract method to get a response from the LLM API.

        Args:
            prompt (str): The text prompt for the model.
            **kwargs: Additional arguments specific to the implementation.

        Returns:
            str: The response from the LLM.
        """
        pass
