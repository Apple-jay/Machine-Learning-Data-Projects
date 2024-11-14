import streamlit as st
import pandas as pd
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from datetime import datetime, date

# Page title
st.set_page_config(page_title="Credit Card Application", page_icon="💳")
st.title("📄 Credit Card Application Form")

# Form Input Section
st.markdown("### Applicant Information")
with st.form(key='user_form'):
    col1, col2 = st.columns(2)
    with col1:
        f_name = st.text_input('First Name', key='f_name')
    with col2:
        l_name = st.text_input('Last Name', key='l_name')
    
    st_address = st.text_input('Street Address', key='st_address')
    
    col3, col4, col5 = st.columns(3)
    with col3:
        city = st.text_input('City', key='city')
    with col4:
        state = st.text_input('State', key='state')
    with col5:
        zip_code = st.text_input('Zip', key='zip')
    
    dob = st.date_input("Date of Birth", key='dob')
    ssn = st.text_input('SSN', key='ssn', type="password")
    email = st.text_input('Email', key='email')
    
    license_d = st.file_uploader("Upload a Copy of Your License", type=["png", "jpg", "jpeg"], key='license_d')
    
    submit_button = st.form_submit_button(label='Submit Application')

# Azure OCR and Document Analysis
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

if submit_button:
    st.subheader("📝 Verification Results")
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    formUrl = url(fname=f_name)

    with st.spinner("Analyzing uploaded document..."):
        poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-idDocument", formUrl)
        id_documents = poller.result()
    
    # Verification logic
    counter = 0
    for idx, id_document in enumerate(id_documents.documents):
        st.write(f"**Document {idx + 1}**")
        first_name = id_document.fields.get("FirstName")
        last_name = id_document.fields.get("LastName")
        dob_on_dl = id_document.fields.get("DateOfBirth")
        
        if first_name and first_name.value == f_name:
            st.success(f"First Name: Match (Confidence: {first_name.confidence:.2f})")
            counter += 1
        else:
            st.error("First Name: Does Not Match")
        
        if last_name and last_name.value == l_name:
            st.success(f"Last Name: Match (Confidence: {last_name.confidence:.2f})")
            counter += 1
        else:
            st.error("Last Name: Does Not Match")

        if dob_on_dl and dob_on_dl.value == dob.strftime('%Y-%m-%d'):
            st.success(f"Date of Birth: Match (Confidence: {dob_on_dl.confidence:.2f})")
            counter += 1
        else:
            st.error("Date of Birth: Does Not Match")

        # Expiration Date Check
        doe = id_document.fields.get("DateOfExpiration")
        if doe:
            expiry_date = date.fromisoformat(str(doe.value))
            if expiry_date > date.today():
                st.success("License Expiration Date: Valid")
                counter += 1
            else:
                st.warning("License Expiration Date: Expired")
                counter -= 4

    # Final ID Verification Result
    if counter >= 3:
        st.success("✅ ID Verification Passed")
    else:
        st.error("❌ ID Verification Failed")
