class PromptReader:
    """
    A class to read prompts from a file.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the PromptReader with the file path.

        Args:
            file_path (str): The path to the file containing the prompt.
        """
        self.file_path = file_path

    def read_prompt(self) -> str:
        """
        Reads the prompt from the file.

        Returns:
            str: The content of the file as the prompt.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If the file cannot be read.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                prompt = file.read().strip()
                return prompt
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except IOError as e:
            raise IOError(f"Error reading file {self.file_path}: {e}")
