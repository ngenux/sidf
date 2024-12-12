import streamlit as st
from PIL import Image
from utils.file_handler  import StreamlitFileHandler
from llm.bedrock_client import BedrockClient
from utils.prompt import PromptReader
from utils.cr_process import ProcessCR
from utils.il_process import ProcessIL
from utils.doc_process import ProcessDoc
from dotenv import load_dotenv
import os
from logger_config import logger
from concurrent.futures import ThreadPoolExecutor
load_dotenv()

class DocumentProcessingApp:
    def __init__(self, title, subtitle, logo_img_path, sidebar_img_path, model_id):
        self.title = title
        self.subtitle = subtitle
        self.logo_img_path = logo_img_path
        self.sidebar_img_path = sidebar_img_path
        self.model_id = model_id

    def configure_page(self):
        """Configure the Streamlit page settings."""
        img = Image.open(self.logo_img_path)
        st.set_page_config(page_title="Document Processing Application", page_icon=img, layout="wide")

    def display_header(self):
        """Display the title and subtitle."""
        st.markdown(f"<h3 style='text-align:center;padding: 0px 0px;color:black;'>{self.title}</h3>"
                    f"<h4 style='text-align:center;color:grey;font-size:80%;'><i>{self.subtitle}</i></h4>",
                    unsafe_allow_html=True)

    def customize_sidebar(self):
        """Customize the sidebar."""
        st.markdown(
            """
            <style>
                [data-testid=stSidebar] [data-testid=stImage]{
                    text-align: center;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    width: 100%;
                }
            </style>
            """, unsafe_allow_html=True
        )

        with st.sidebar:
            org_img = Image.open(self.sidebar_img_path)
            st.image(org_img)

    def upload_files(self):
        """Handle file uploads."""
        doc_file = st.file_uploader("Upload Loan Application", type=["pdf", "docx"])
        industry_licence = st.file_uploader("Upload Industry License", type=["jpg", "png"])
        comm_licence = st.file_uploader("Upload Commercial Registration", type=["jpg", "png"])
        return doc_file, industry_licence, comm_licence

 
def log_task_start(task_name):
    logger.info(f"{task_name} has started.")
 
def process_document(doc_file, bedrock_client):
    log_task_start("Document Processing")
    if doc_file:
        doc_process = ProcessDoc(doc_file, bedrock_client)
        return doc_process.file_processor()
    return None
 
 
def process_commercial_registration(comm_licence, bedrock_client):
    log_task_start("Commercial Registration Processing")
    if comm_licence:
        cr_processor = ProcessCR(comm_licence, bedrock_client)
        return cr_processor.process_files()
    return None
 
 
def process_industry_license(industry_licence, bedrock_client):
    log_task_start("Industry License Processing")
    if industry_licence:
        il_process = ProcessIL(industry_licence, bedrock_client)
        return il_process.process_files()
    return None

def main():
    # Create the DocumentProcessingApp instance
    app = DocumentProcessingApp(
        title="A Streamlit application for document processing",
        subtitle="Brought to you by the Ngenux Data Science and Analytics Team",
        logo_img_path="static/image.png",
        sidebar_img_path="static/Ngenux.jpeg",
        model_id="anthropic.claude-3-haiku-20240307-v1:0"
    )

    app.configure_page()
    app.display_header()
    app.customize_sidebar()

    bedrock_client = BedrockClient(
                            aws_access_key=os.getenv("AWS_ACCESS_KEY_ID"),
                            aws_secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                        )
    doc_file, industry_licence, comm_licence = app.upload_files()
    
    cr_response = None
    il_response = None 
    doc_response = None
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col3:
        btn_result = st.button("Process", key="parse")
        if btn_result:
            logger.info("Starting parallel processing for all tasks.")
            with ThreadPoolExecutor() as executor:
                futures = {
                    "doc_response": executor.submit(
                        process_document, doc_file, bedrock_client
                    ),
                    "cr_response": executor.submit(
                        process_commercial_registration, comm_licence, bedrock_client
                    ),
                    "il_response": executor.submit(
                        process_industry_license, industry_licence, bedrock_client
                    ),
                }
            results = {key: future.result() for key, future in futures.items()}
            doc_response = results["doc_response"]
            cr_response = results["cr_response"]
            il_response = results["il_response"]
            logger.info("Completed parallel processing for all tasks.")

    if doc_response :
        st.write("Fields which do not have data:")
        # Extract the missing data
        missing_data = doc_response.get('missing', {}).get('missing_data', '')
        # Display the missing data in a text box
        st.text_area("Missing Data", value=str(missing_data), height=200)
        
        # extract inconsistent data
        inconsistent_data = doc_response.get("inc_data",{})
        st.text_area("Inconcsistent Data", value=str(inconsistent_data), height=200)

        # Check Industry License Response
        if il_response and "رقم القرار" in il_response:
            if doc_response.get("cr_and_il", {}).get("industrial_license_value") == il_response["رقم القرار"]:
                st.write("Industry license number from Loan Application is same as Industry license number in image uploaded.")
                print("Industry license number from Loan Application is same as Industry license number in image uploaded.")
            else:
                st.write("Industry license number from Loan Application is not matched with image uploaded.")
                print("Industry license number from Loan Application is not matched with image uploaded.")
        else:
            st.write("Industry License response is missing or invalid.")
            print("Industry License response is missing or invalid.")

        # Check Commercial Registration Response
        if cr_response and "رقم المنشأة" in cr_response:
            if doc_response.get("cr_and_il", {}).get("commercial_register_value") == cr_response["رقم المنشأة"]:
                st.write("Commercial Registration number from Loan Application is same as CR-number in image uploaded.")
                print("Commercial Registration number from Loan Application is same as CR-number in image uploaded.")
            else:
                st.write("Commercial Registration number from Loan Application is not same as CR-number in image uploaded.")
                print("Commercial Registration number from Loan Application is not same as CR-number in image uploaded.")
        else:
            st.write("Commercial Registration response is missing or invalid.")
            print("Commercial Registration response is missing or invalid.")

if __name__ == "__main__":
    main()
