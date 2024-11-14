"""
This code sample shows Prebuilt ID Document operations with the Azure Form Recognizer client library. 
The async versions of the samples require Python 3.6 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""
# BAD2
fnam1 ="JELANI"
lname1="SAMPLE"
zip1='85007'

# gOOD 2
fname2='BRENDA'
lname2='SAMPLE'
zip2='29999'

# glared 1
fname3='PETER'
lname3='GRIFFIN'
zip3='08666'
def url(fname):
    if fname == "JELANI":
        return "https://fa3pub.blob.core.windows.net/pub/BadID2.png?sp=r&st=2024-11-13T22:04:50Z&se=2024-11-14T06:04:50Z&sv=2022-11-02&sr=b&sig=IXBA0AlzncTX0MUzJqS1xpfFgtanDU%2BGDQ%2Bu7rd6AHk%3D"
    elif fname == "BRENDA":
        return "https://fa3pub.blob.core.windows.net/pub/GoodID2.png?sp=r&st=2024-11-13T22:07:55Z&se=2024-11-14T06:07:55Z&sv=2022-11-02&sr=b&sig=i34rBVTKaQbyRCW3f8CPFyLLvTrKhpsP97VNNhjrp1w%3D"
    elif fname == "PETER":
        return "https://fa3pub.blob.core.windows.net/pub/GlaredID1.png?sp=r&st=2024-11-13T22:06:03Z&se=2024-11-14T06:06:03Z&sv=2022-11-02&sr=b&sig=dQ8HLCPZay0TlR%2FSRN2oyK4NIx6ENLSsopBAhp0rf9I%3D"


from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

"""
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""
endpoint = "https://ocr-fa-1.cognitiveservices.azure.com/"
key = "CIhb71fs9A6obdQ2PSChcdPYHbGITYDDHd8T4iyaYdIZakK7ZsezJQQJ99AKACYeBjFXJ3w3AAALACOGqlJk"


# sample document
# formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/DriverLicense.png"
formUrl = url(fname="JELANI")

document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-idDocument", formUrl)
id_documents = poller.result()
counter=0
for idx, id_document in enumerate(id_documents.documents):
    print("--------Recognizing ID document #{}--------".format(idx + 1))
    first_name = id_document.fields.get("FirstName")
    if first_name:
        print(
            "First Name: {} has confidence: {}".format(
                first_name.value, first_name.confidence
            )
        )
    if first_name and first_name.value == fnam1:
        print(
            "First Name on application matches first name on DL"
            )
        counter=counter+1
    else:
        print("First name does not match")
    last_name = id_document.fields.get("LastName")
    if last_name:
        print(
            "Last Name: {} has confidence: {}".format(
                last_name.value, last_name.confidence
            )
        )
    if last_name and last_name.value == lname1:
        print(
            "Last Name on application matches last name on DL"
            )
        counter=counter+1
    else:
        print("First name does not match")
    document_number = id_document.fields.get("DocumentNumber")
    if document_number:
        print(
            "Document Number: {} has confidence: {}".format(
                document_number.value, document_number.confidence
            )
        )
    dob = id_document.fields.get("DateOfBirth")
    if dob:
        print(
            "Date of Birth: {} has confidence: {}".format(dob.value, dob.confidence)
        )
    doe = id_document.fields.get("DateOfExpiration")
    if doe:
        print(
            "Date of Expiration: {} has confidence: {}".format(
                doe.value, doe.confidence
            )
        )
    sex = id_document.fields.get("Sex")
    if sex:
        print("Sex: {} has confidence: {}".format(sex.value, sex.confidence))
    address = id_document.fields.get("Address")
    if address:
        print(
            "Address: {} has confidence: {}".format(
                address.value, address.confidence
            )
        )
    if address.value and zip1 in  str(address.value):
        print(
            "zip on application matches zip on DL"
            )
        counter=counter+1
    else:
        print("zip does not match")
 
    country_region = id_document.fields.get("CountryRegion")
    if country_region:
        print(
            "Country/Region: {} has confidence: {}".format(
                country_region.value, country_region.confidence
            )
        )
    region = id_document.fields.get("Region")
    if region:
        print(
            "Region: {} has confidence: {}".format(region.value, region.confidence)
        )
if counter==3:
    print("ID check passed")
else:
    print("ID check failed")

    
