import json
import boto3
from .llm_client import LLMClient

class BedrockClient(LLMClient):
    """
    AWS Bedrock client for interacting with Bedrock models.
    """

    def __init__(self, aws_access_key, aws_secret_key, region="us-east-1"):
        super().__init__()
        self.runtime = boto3.client(
            service_name="bedrock-runtime",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region,
        )

    def get_response(self, prompt, encoded_file=None, mime_type=None, model_id=None):
        """
        Sends a request to the Bedrock API and returns the response.

        Args:
            prompt (str): The text prompt for the API.
            encoded_file (str): Base64-encoded file data (optional).
            mime_type (str): MIME type of the file (optional).
            model_id (str): The model ID to use for inference.

        Returns:
            str: The text response from the Bedrock API.
        """
        try:
            # Construct content based on inputs
            content = [{"type": "text", "text": prompt}]
            if encoded_file and mime_type:
                content.append(
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": encoded_file,
                        },
                    }
                )

            # Construct request body
            messages = [{"role": "user", "content": content}]
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 10000,
                "messages": messages,
                "temperature": 0.1,
                "top_k": 250,
                "top_p": 0.999,
            })

            # Invoke Bedrock model
            response = self.runtime.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=body,
            )

            response_body = json.loads(response.get("body").read())
            return response_body['content'][0]['text']

        except Exception as e:
            self.logger.error(f"Error in Bedrock API call: {e}")
            return None
        
    
    def get_response_text(self, prompt,data,model_id=None):
        """
        Sends a request to the Bedrock API and returns the response.

        Args:
            prompt (str): The text prompt for the API.
            model_id (str): The model ID to use for inference.

        Returns:
            str: The text response from the Bedrock API.
        """
        try:
            # Construct content based on inputs
            content = [{"type": "text", "text": prompt}]
            if data:
                content.append(
                    {
                        "type": "text",
                        "text":json.dumps(data)
                    }
                )

            # Construct request body
            messages = [{"role": "user", "content": content}]
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 10000,
                "messages": messages,
            })

            # Invoke Bedrock model
            response = self.runtime.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=body,
            )

            response_body = json.loads(response.get("body").read())
            return response_body['content'][0]['text']

        except Exception as e:
            self.logger.error(f"Error in Bedrock API call: {e}")
            return None