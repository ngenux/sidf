from .file_handler import StreamlitFileHandler
from .prompt import PromptReader
import json
class ProcessCR:
    def __init__(self, comm_licence, bedrock_client):
        self.comm_licence = comm_licence
        self.bedrock_client = bedrock_client
        self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    def process_files(self):
        """Process the uploaded files and get response from the model."""
       
        file_data = StreamlitFileHandler.read_uploaded_file(self.comm_licence)

        # Read the prompt from the file
        pr = PromptReader("prompts/cr_prompt.txt")
        prompt = pr.read_prompt()
        print(prompt)
        # Get the response from the model
        cr_response = self.bedrock_client.get_response(
            prompt=prompt,
            encoded_file=file_data["encoded_file"],
            mime_type=file_data["mime_type"],
            model_id=self.model_id,
        )

        # For demo purposes, print the response
        print(cr_response)
        cr_response = json.loads(cr_response)
        return cr_response