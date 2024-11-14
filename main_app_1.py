import streamlit as st
import pandas
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from datetime import datetime, timedelta, date

# Set up the page layout and style
st.set_page_config(page_title="Credit Card Application", page_icon="💳", layout="centered")
st.markdown(
    """
    <style>
    .title {
        font-size: 2em; color: #333; text-align: center; font-weight: bold;
    }
    .form-label {
        font-weight: 600; color: #4B4B4B;
    }
    .submit-button {
        background-color: #4CAF50; color: white; font-weight: bold; font-size: 1em; padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Header Styling
st.markdown("<h1 class='title'>Credit Card Application Form</h1>", unsafe_allow_html=True)
st.write("Please complete the form below to apply.")

# Form layout
with st.form(key='user_form'):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<label class='form-label'>First Name</label>", unsafe_allow_html=True)
        f_name = st.text_input('', key='f_name', placeholder="John")

    with col2:
        st.markdown("<label class='form-label'>Last Name</label>", unsafe_allow_html=True)
        l_name = st.text_input('', key='l_name', placeholder="Doe")

    st.markdown("<label class='form-label'>Street Address</label>", unsafe_allow_html=True)
    st_address = st.text_input('', key='st_address', placeholder="123 Main St")

    col1, col2, col3 = st.columns([1, 1, 1.2])
    with col1:
        st.markdown("<label class='form-label'>City</label>", unsafe_allow_html=True)
        city = st.text_input('', key='city', placeholder="City")
    with col2:
        st.markdown("<label class='form-label'>State</label>", unsafe_allow_html=True)
        state = st.text_input('', key='state', placeholder="State")
    with col3:
        st.markdown("<label class='form-label'>Zip</label>", unsafe_allow_html=True)
        zip = st.text_input('', key='zip', placeholder="12345")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<label class='form-label'>DOB (mm/dd/yyyy)</label>", unsafe_allow_html=True)
        dobx = st.text_input('', key='dobx', placeholder="MM/DD/YYYY")
    with col2:
        st.markdown("<label class='form-label'>SSN</label>", unsafe_allow_html=True)
        ssn = st.text_input('', key='ssn', placeholder="XXX-XX-XXXX", help="Your social security number")

    st.markdown("<label class='form-label'>Email</label>", unsafe_allow_html=True)
    email = st.text_input('', key='email', placeholder="email@example.com")

    st.markdown("<label class='form-label'>Upload Your License</label>", unsafe_allow_html=True)
    license_d = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key='license_d')

    st.markdown(
        "<button class='submit-button' type='submit'>Submit Application</button>",
        unsafe_allow_html=True,
    )
    submit_button = st.form_submit_button(label='Submit')

# Azure Document Analysis
if submit_button:
    with st.spinner("Processing..."):
        st.write(f"**Applicant:** {f_name} {l_name}")
        
        def url(fname):
            if fname == "JELANI":
                return "https://fa3pub.blob.core.windows.net/pub/BadID2.png?sp=r&st=2024-11-13T22:04:50Z&se=2024-11-14T06:04:50Z&sv=2022-11-02&sr=b&sig=IXBA0AlzncTX0MUzJqS1xpfFgtanDU%2BGDQ%2Bu7rd6AHk%3D"
            elif fname == "BRENDA":
                return "https://fa3pub.blob.core.windows.net/pub/GoodID2.png?sp=r&st=2024-11-13T22:07:55Z&se=2024-11-14T06:07:55Z&sv=2022-11-02&sr=b&sig=i34rBVTKaQbyRCW3f8CPFyLLvTrKhpsP97VNNhjrp1w%3D"
            elif fname == "PETER":
                return "https://fa3pub.blob.core.windows.net/pub/GlaredID1.png?sp=r&st=2024-11-13T22:06:03Z&se=2024-11-14T06:06:03Z&sv=2022-11-02&sr=b&sig=dQ8HLCPZay0TlR%2FSRN2oyK4NIx6ENLSsopBAhp0rf9I%3D"
            else:
                return "https://fa3pub.blob.core.windows.net/pub/GlaredID1.png?sp=r&st=2024-11-13T22:06:03Z&se=2024-11-14T06:06:03Z&sv=2022-11-02&sr=b&sig=dQ8HLCPZay0TlR%2FSRN2oyK4NIx6ENLSsopBAhp0rf9I%3D"

        endpoint = "https://ocr-fa-1.cognitiveservices.azure.com/"
        key = "CIhb71fs9A6obdQ2PSChcdPYHbGITYDDHd8T4iyaYdIZakK7ZsezJQQJ99AKACYeBjFXJ3w3AAALACOGqlJk"
        formUrl = url(fname=f_name)
        document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        
        try:
            poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-idDocument", formUrl)
            id_documents = poller.result()
            counter = 0

            st.subheader("Verification Results")
            for idx, id_document in enumerate(id_documents.documents):
                st.write(f"**Recognizing ID Document #{idx + 1}**")

                first_name = id_document.fields.get("FirstName")
                st.write("First Name:", first_name.value, f"(Confidence: {first_name.confidence:.2f})")
                if first_name and first_name.value == f_name:
                    st.success("First Name matches.")
                    counter += 1
                else:
                    st.error("First Name does not match.")

                last_name = id_document.fields.get("LastName")
                st.write("Last Name:", last_name.value, f"(Confidence: {last_name.confidence:.2f})")
                if last_name and last_name.value == l_name:
                    st.success("Last Name matches.")
                    counter += 1
                else:
                    st.error("Last Name does not match.")

                dob = id_document.fields.get("DateOfBirth")
                db_dt = date.fromisoformat(str(dob.value))
                doby = datetime.strptime(dobx, "%m/%d/%Y").strftime('%Y-%m-%d')

                if db_dt == doby:
                    st.success("Date of Birth matches.")
                    counter += 1
                else:
                    st.error("Date of Birth does not match.")

                doe = id_document.fields.get("DateOfExpiration")
                if date.fromisoformat(str(doe.value)) > date.today():
                    st.success("License is valid.")
                    counter += 1
                else:
                    st.error("License has expired.")
                    counter -= 4

            if counter >= 3:
                st.success("ID check passed.")
            else:
                st.error("ID check failed.")
        except Exception as e:
            st.error("An error occurred during document analysis.")
            st.write(e)
