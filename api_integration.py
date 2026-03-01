import json
import base64
import requests

# ngrok http --domain=newly-major-ape.ngrok-free.app 8080
# https://newly-major-ape.ngrok-free.app/identityiq/
# https://newly-major-ape.ngrok-free.app/identityiq/identityRequest/identityRequest.jsf#/requests

# https://genuine-enhanced-grackle.ngrok-free.app/iiq/plugin/rest/identityai/
# https://genuine-enhanced-grackle.ngrok-free.app/iiq/identityRequest/identityRequest.jsf#/requests

sailpoint_url = 'https://57df5ac5debb.ngrok-free.app/iiq/plugin/rest/identityai'

def get_encoded_credentials(file_path='auth.txt', request_type='GET'):
    """
    Function to get the Base64 encoded credentials from the provided file.
    """
    with open(file_path, 'r') as file:
        credentials = file.read().strip()
    
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    if request_type.upper() == "POST":
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_credentials}'
        }
    else:  # Default is GET
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded_credentials}'
        }
    
    return encoded_credentials

def get_user_entitlements(user_name):
    """
    Function to get entitlements for all applications assigned to a specific user from SailPoint.
    """
    user_name = user_name.replace("'", "")
    if not user_name:
        user_name = 'vishnu'  # Default user

    encoded_credentials = get_encoded_credentials()
    url = f"{sailpoint_url}/getIdentityEntitlements?userName={user_name}"
    
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        user_entitlements = [
            {
                'userName': entitlement_info['userName'],
                'applicationName': entitlement_info['applicationName'],
                'entitlements': entitlement_info.get('entitlements', [])
            }
            for entitlement_info in data
        ]
        if not user_entitlements:
            return f"There are no entitlements connected to the user {user_name}."
        return user_entitlements
    else:
        return f"Error retrieving entitlements for user {user_name}. Status code: {response.status_code}."

def get_user_application_entitlements(user_application):
    """
    Function to get user application entitlements.
    """
    user_application = user_application.replace("'", "")
    if not user_application:
        return "User application input is required."

    user_name, application_name = None, None
    if ',' in user_application:
        user_name, application_name = [val.strip() for val in user_application.split(',')]

    if not user_name:
        user_name = 'vishnu'

    encoded_credentials = get_encoded_credentials()
    url = f"{sailpoint_url}/getIdentityApplicationEntitlements?userName={user_name}&applicationName={application_name}"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if len(data) == 1:
            return data[0]
        return f"The user {user_name} doesn't have any entitlements for the application {application_name}."
    else:
        return f"Error retrieving entitlements for user {user_name} in application {application_name}. Status code: {response.status_code}."

def get_application_entitlements(application_name):
    """
    Function to get the list of entitlements for a given application.
    """
    if not application_name:
        return "Application name is required."

    encoded_credentials = get_encoded_credentials()
    url = f"{sailpoint_url}/getApplicationEntitlements?applicationName={application_name}"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for app in data:
            if app['applicationName'] == application_name:
                return {
                    "applicationName": app['applicationName'],
                    "entitlements": app['entitlements']
                }
        return f"Application {application_name} not found."
    else:
        return f"Error: {response.status_code}, {response.text}"

def get_user_roles(user_name):
    """
    Function to get assigned roles for a given user from SailPoint.
    """
    if not user_name:
        user_name = 'vishnu'

    encoded_credentials = get_encoded_credentials()
    url = f"{sailpoint_url}/getAssignedRoles?userName={user_name}"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data[0].get('roleNames', []) if data else []
    else:
        return f"Error fetching roles for {user_name}. Status code: {response.status_code}"

# changed the status endpoint to the approvers endpoint
def get_request_status(request_id):
    """
    Function to get request status for a given request ID.
    """
    encoded_credentials = get_encoded_credentials()
    url = f"{sailpoint_url}/getIdentityRequestApprovers?requestId={request_id}"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else f"Error: {response.status_code}, {response.text}"

def get_approver_details(request_id):
    """
    Function to get approver details for a given request ID.
    """
    encoded_credentials = get_encoded_credentials()
    url = f"{sailpoint_url}/getIdentityRequestApprovers?requestId={request_id}"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else f"Error: {response.status_code}, {response.text}"

def get_pending_requests(user_name):
    """
    Function to get pending requests for a given user.
    """
    user_name = user_name.replace("'", "") or "vishnu"
    encoded_credentials = get_encoded_credentials()
    url = f"{sailpoint_url}/getAllPendingIdentityRequests?userName={user_name}"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        return response_data if response_data else "No pending requests"
    else:
        return f"Error: {response.status_code}, {response.text}"

def raise_identity_request(inp):
    """
    Function to launch a workflow for IdentityRequest (raise a request).
    """
    inp = inp.replace("'", "")
    user_name, attribute_value = None, None

    if ',' in inp:
        user_name, attribute_value = [val.strip() for val in inp.split(',')]

    encoded_credentials = get_encoded_credentials()
    url = f"{sailpoint_url}/identityRequestLaunchWorkflow"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }


    payload = {
        "userName": user_name if user_name else "vishnu",
        "applicationName": "Fortuna-loan-AppUsers",
        "attributeName": "groupmbr",
        "attributeValue": attribute_value if attribute_value else "PlanReview"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        request_id = response_data[0].get("IdentityRequestId") if isinstance(response_data, list) and response_data else None
        if request_id:
            request_link = f"https://genuine-enhanced-grackle.ngrok-free.app/iiq/identityRequest/identityRequest.jsf#/request/{request_id}"
            return {
                "request_link": request_link,
                "message": "Request raised successfully."
            }
        else:
            return {
                "request_link": None,
                "message": "Request not raised."
            }
    else:
        return {
            "request_link": None,
            "status_code": response.status_code,
            "message": response.text
        }