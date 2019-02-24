import os
import base64
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Signer, SignHere, Tabs, Recipients, Document, RecipientViewRequest


# Settings
# Fill in these constants
#
# Obtain an OAuth access token from https://developers.hqtest.tst/oauth-token-generator
access_token = 'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQoAAAABAAUABwCAuqI6eJrWSAgAgPrFSLua1kgCAO3OHEV2K8VFtZlarh_1k08VAAEAAAAYAAEAAAAFAAAADQAkAAAAZjBmMjdmMGUtODU3ZC00YTcxLWE0ZGEtMzJjZWNhZTNhOTc4EgABAAAACwAAAGludGVyYWN0aXZlMACAjXE5eJrWSDcABa2cV8lJ2kC3aXWjv1LWFA.4H-Urk-BTclO33TAiagKzfzzwekPNihoJT1yu-BBepood49pnbdH-dQoLeEMwuTsS9sk6A2wNl9TpmFgDxqwNhqRV1Ao2LPX_fh2105gsqqPogUGvlbe00sY-l5I7hSI9pDPYMORPdMbQabfEw6QRnMHafVqoXXagDdygRxnI6oG3hIaeXXcf5iilTYpbW2PVFvOzYBdzKhQMgRSYEnyl1qJUfVe3CTNbpzBCgiB8LdQ_bKG7wfLNArzpFqM_x7-NM8gbJLQ1RMSFtZOl9pTsAzKlVQhlVhLXHzYGRRd-b_jFcFh5YjFWzKzCqQvvXXUdBCEpoVVDGU1Wq9DE5e39A'
# Obtain your accountId from demo.docusign.com -- the account id is shown in the drop down on the
# upper right corner of the screen by your picture or the default picture.
account_id = '7988731'
# Recipient Information:
signer_name = 'Aman Yadav'
signer_email = 'amanyadava@gmail.com'
# The document you wish to send. Path is relative to the root directory of this repo.
file_name_path = 'demo_documents/World_Wide_Corp_lorem.pdf'
# The url of this web application
base_url = 'http://127.0.0.1:5000'
client_user_id = '123' # Used to indicate that the signer will use an embedded
                       # Signing Ceremony. Represents the signer's userId within
                       # your application.
authentication_method = 'None' # How is this application authenticating
                               # the signer? See the `authenticationMethod' definition
                               # https://developers.docusign.com/esign-rest-api/reference/Envelopes/EnvelopeViews/createRecipient

# The API base_path
base_path = 'https://demo.docusign.net/restapi'

# Set FLASK_ENV to development if it is not already set
if 'FLASK_ENV' not in os.environ:
    os.environ['FLASK_ENV'] = 'development'

# Constants
APP_PATH = os.path.dirname(os.path.abspath(__file__))

def embedded_signing_ceremony():
    """
    The document <file_name> will be signed by <signer_name> via an
    embedded signing ceremony.
    """

    #
    # Step 1. The envelope definition is created.
    #         One signHere tab is added.
    #         The document path supplied is relative to the working directory
    #
    with open(os.path.join(APP_PATH, file_name_path), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    # Create the document model
    document = Document( # create the DocuSign document object
        document_base64 = base64_file_content,
        name = 'Example document', # can be different from actual file name
        file_extension = 'pdf', # many different document types are accepted
        document_id = 1 # a label used to reference the doc
    )

    # Create the signer recipient model
    signer = Signer( # The signer
        email = signer_email, name = signer_name, recipient_id = "1", routing_order = "1",
        client_user_id = client_user_id, # Setting the client_user_id marks the signer as embedded
    )

    # Create a sign_here tab (field on the document)
    sign_here = SignHere( # DocuSign SignHere field/tab
        document_id = '1', page_number = '1', recipient_id = '1', tab_label = 'SignHereTab',
        x_position = '195', y_position = '147')

    # Add the tabs model (including the sign_here tab) to the signer
    signer.tabs = Tabs(sign_here_tabs = [sign_here]) # The Tabs object wants arrays of the different field/tab types

    # Next, create the top level envelope definition and populate it.
    envelope_definition = EnvelopeDefinition(
        email_subject = "Please sign this document sent from the Python SDK",
        documents = [document], # The order in the docs array determines the order in the envelope
        recipients = Recipients(signers = [signer]), # The Recipients object wants arrays for each recipient type
        status = "sent" # requests that the envelope be created and sent.
    )

    #
    #  Step 2. Create/send the envelope.
    #
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header("Authorization", "Bearer " + access_token)

    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(account_id, envelope_definition=envelope_definition)

    #
    # Step 3. The envelope has been created.
    #         Request a Recipient View URL (the Signing Ceremony URL)
    #
    envelope_id = results.envelope_id
    recipient_view_request = RecipientViewRequest(
        authentication_method = authentication_method, client_user_id = client_user_id,
        recipient_id = '1', return_url = base_url + '/thank_you_seeker',
        user_name = signer_name, email = signer_email
    )

    results = envelope_api.create_recipient_view(account_id, envelope_id,
        recipient_view_request = recipient_view_request)

    #
    # Step 4. The Recipient View URL (the Signing Ceremony URL) has been received.
    #         Redirect the user's browser to it.
    #
    return results.url
