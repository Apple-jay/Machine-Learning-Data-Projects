import streamlit as st
import pandas
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from datetime import datetime, timedelta,date

# st.balloons()

st.title(" Credit Card Application Form")

with st.form(key='user_form'):
    f_name = st.text_input('First name', key='f_name')
    l_name = st.text_input('Last name', key='l_name')
    st_address = st.text_input('Street address', key='st_address')
    city = st.text_input('City', key='city')
    state = st.text_input('State', key='state')
    zip = st.text_input('Zip', key='zip')
    dobx = st.text_input('DOB (mm/dd/yyyy)', key='dobx')
    ssn = st.text_input('SSN', key='ssn', type="password")
    email = st.text_input('Email', key='email')
    license_d=st.file_uploader("Please upload copy of your license", key='license_d')
    submit_button=st.form_submit_button(label='Submit')
# first_name = st.text_input('First name', key='first_name')
# first_name = st.text_input('First name', key='first_name')
# first_name = st.text_input('First name', key='first_name')
# first_name = st.text_input('First name', key='first_name')

# **********************code statrts for Azure call
f_name = f_name.upper()
l_name = l_name.upper()

if submit_button:
    st.write(f_name)
    st.write(l_name)

    def url(fname):
        if fname == "THOR THUNDER":
            return "https://fa3pub.blob.core.windows.net/pub/BadID3.png?sp=r&st=2024-11-14T14:35:34Z&se=2024-11-14T22:35:34Z&sv=2022-11-02&sr=b&sig=nJtNKvVheGumYCi3xNa9XrWRz8plnI8DhyJXgDwnRG4%3D"
        elif fname == "BRENDA":
            return "https://fa3pub.blob.core.windows.net/pub/GoodID2.png?sp=r&st=2024-11-14T14:37:13Z&se=2024-11-14T22:37:13Z&sv=2022-11-02&sr=b&sig=VlFZHx%2FGzw1vDBG8irin68L6qhU7m2r732XXC8944zA%3D"
        elif fname == "JOHN LEWIS":
            return "https://fa3pub.blob.core.windows.net/pub/Blurred1.png?sp=r&st=2024-11-14T14:29:14Z&se=2024-11-14T22:29:14Z&sv=2022-11-02&sr=b&sig=jvDeTYSRwwMUfQ1KPXkWkXF%2Bni%2F%2B11yTWFxabH%2BUo2E%3D"
        else:
            return "https://fa3pub.blob.core.windows.net/pub/BadID3.png?sp=r&st=2024-11-14T14:35:34Z&se=2024-11-14T22:35:34Z&sv=2022-11-02&sr=b&sig=nJtNKvVheGumYCi3xNa9XrWRz8plnI8DhyJXgDwnRG4%3D"
    
    endpoint = "https://ocr-fa-1.cognitiveservices.azure.com/"
    key = "CIhb71fs9A6obdQ2PSChcdPYHbGITYDDHd8T4iyaYdIZakK7ZsezJQQJ99AKACYeBjFXJ3w3AAALACOGqlJk"

    # sample document
    # formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/DriverLicense.png"
    formUrl = url(fname=f_name)


    document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
        
    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-idDocument", formUrl)
    id_documents = poller.result()
    counter=0
    for idx, id_document in enumerate(id_documents.documents):
        st.write("-------- Recognizing ID document #{} --------".format(idx + 1))

        first_name = id_document.fields.get("FirstName")
        st.write("First Name: {} has confidence: {}".format(first_name.value, first_name.confidence))
        if first_name and first_name.value == f_name:
            st.write("First Name on application matches first name on DL")
            counter=counter+1
        else:
            st.write("First name does not match")

        last_name = id_document.fields.get("LastName")
        st.write("Last Name: {} has confidence: {}".format(last_name.value, last_name.confidence))
        if last_name and last_name.value == l_name:
            st.write("Last Name on application matches last name on DL")
            counter=counter+1
        else:
            st.write("Last name does not match")

        dob = id_document.fields.get("DateOfBirth")
        if dob:
            st.write("Date of Birth: {} has confidence: {}".format(dob.value, dob.confidence))

        db_t=dob.value   
        dbt1=str(db_t)
        # st.write(dbt1)
        
        db_dt=date.fromisoformat(str(dbt1))
        doby=datetime.strptime(dobx, "%m/%d/%Y").strftime('%Y-%m-%d')
        # x_dt2=date.fromisoformat(str(db_dt))


        # st.write(db_dt)
        # st.write(doby)

        # st.write(type(dbt1))
        # st.write(type(doby))

        if dbt1 == doby:
            st.write("Date of birth matches DOB on DL")
            counter=counter+1
        else:
            st.write("Date of birth does not match DOB on DL")

        doe = id_document.fields.get("DateOfExpiration")
        st.write("Date of Expiration: {} has confidence: {}".format(doe.value, doe.confidence))
        tpr=str(doe.value)
        # st.write(tpr)
        doe_dt=date.fromisoformat(str(tpr))
        t_dt=date.today()
        # st.write(t_dt)
        if doe_dt > t_dt:
            st.write("Expiry date valid on DL")
            counter=counter+1
        else:
            st.write("Expired drivers license provided")
            counter=counter-4

        sex = id_document.fields.get("Sex")
        if sex:
            st.write("Sex: {} has confidence: {}".format(sex.value, sex.confidence))
        address = id_document.fields.get("Address")
        # if address:
            # st.write("Address: {} has confidence: {}".format(address.value, address.confidence))
            # st.write(address.value)
        # p1= type(address.value)
        # st.write(p1)
        # myary = p1.split(",")
        # for word in myary:
        #     if "state=" in word.lower():
        #         ar1=word.split(":")
        #         st= word.replace("state=",'')
        #         print(st)
        #         print(ar1)
        #     if "postal_code" in word.lower():
        #         zipx=word.replace("postal_code=",'')
        #         print(zip)
        # if state and first_name.value == st:
        #     st.write(
        #         "State on application matches state DL"
        #         )
        #     counter=counter+1
        # else:
        #     st.write("State does not match")    

        # if zipx and first_name.value == zip:
        #     st.write(
        #         "Zip on application matches Zip DL"
        #         )
        #     counter=counter+1
        # else:
        #     st.write("Zip does not match")                
        # stx = id_document.fields.get("state")
        # st.write(stx) 
        # zipx = id_document.fields.get("postal_code")
        # st.write(dob.value) 
        # st.write(doe.value) 
        country_region = id_document.fields.get("CountryRegion")
        if country_region:
            st.write(
                "Country/Region: {} has confidence: {}".format(
                    country_region.value, country_region.confidence
                )
            )
        region = id_document.fields.get("Region")
        if region:
            st.write(
                "Region: {} has confidence: {}".format(region.value, region.confidence)
            )
    if counter>=3:
        st.write("ID check passed")
    else:
        st.write("ID check failed")  


        
