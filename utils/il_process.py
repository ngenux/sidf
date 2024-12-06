from .file_handler import StreamlitFileHandler
from .prompt import PromptReader
import json 
class ProcessIL:
    def __init__(self, ind_licence, bedrock_client):
        self.ind_licence = ind_licence
        self.bedrock_client = bedrock_client
        self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    def process_files(self):
        """Process the uploaded files and get response from the model."""
       
        file_data = StreamlitFileHandler.read_uploaded_file(self.ind_licence)

        # Read the prompt from the file
        pr = PromptReader("prompts/il_prompt.txt")
        prompt = pr.read_prompt()
        print(prompt)
        # Get the response from the model
        il_response = self.bedrock_client.get_response(
            prompt=prompt,
            encoded_file=file_data["encoded_file"],
            mime_type=file_data["mime_type"],
            model_id=self.model_id,
        )

        # For demo purposes, print the response
        print(il_response)
        il_response = json.loads(il_response)
        return il_response