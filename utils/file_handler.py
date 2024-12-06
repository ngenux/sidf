import base64
import mimetypes
import logging
import streamlit as st


class StreamlitFileHandler:
    """
    A class to handle files uploaded via Streamlit's st.file_uploader.
    """

    @staticmethod
    def read_uploaded_file(uploaded_file):
        """
        Reads the uploaded file and encodes it in base64 format.
        
        Args:
            uploaded_file (UploadedFile): A file uploaded via Streamlit.

        Returns:
            dict: A dictionary containing the encoded file data and its MIME type.
                  Returns None if no file is uploaded or an error occurs.
        """
        if uploaded_file is None:
            logging.error("No file uploaded.")
            return None

        try:
            # Read file content
            file_bytes = uploaded_file.read()

            # Encode the file in base64
            encoded_file = base64.b64encode(file_bytes).decode("utf-8")

            # Detect the MIME type
            mime_type = mimetypes.guess_type(uploaded_file.name)[0] or "application/octet-stream"

            return {
                "file_name": uploaded_file.name,
                "mime_type": mime_type,
                "encoded_file": encoded_file,
            }
        except Exception as e:
            logging.error(f"Error processing uploaded file: {e}")
            return None