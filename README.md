AI Request Manager
==================

**AI Request Manager** is a Streamlit-based chatbot that helps users interact with a SailPoint IdentityIQ environment through natural language.  
Behind the scenes it uses AWS Bedrock (Anthropic Claude 3 Haiku) and LangChain tools to:

- **Raise access requests** (identity requests) for users
- **Check request status and approver details**
- **List user roles and entitlements across applications**
- **List application entitlements**
- **View pending requests for a user**

The UI is a simple chat interface; the agent routes queries to SailPoint REST APIs via `api_integration.py`.

---

## Features

- **Chat-based approval assistant**
  - Streamlit chat UI (`Request_Manager.py`)
  - Conversation memory with `ConversationSummaryBufferMemory`
  - Backed by `ChatBedrock` with Claude 3 Haiku

- **Identity & access operations (via tools in `memory_agent.py`)**
  - `Raise Identity Request` → raises a SailPoint identity request for a user and entitlement
  - `Get User Roles` → lists roles assigned to a user
  - `Get User Entitlements` → lists entitlements for a user across applications
  - `Get User Entitlements for a Specific Application`
  - `Get Application Entitlements`
  - `Get Request Status by ID`
  - `Get Approver Details by Request ID`
  - `Get Pending Requests for a User`

- **SailPoint REST integration (`api_integration.py`)**
  - Uses an ngrok-exposed IdentityIQ REST endpoint
  - Handles:
    - Getting roles and entitlements
    - Launching identity requests
    - Looking up pending requests and approvers

---

## Architecture Overview

- **`Request_Manager.py`**
  - Streamlit entrypoint (`st.title`, `st.chat_input`, chat history)
  - Initializes a `ChatBedrock` LLM and `ConversationSummaryBufferMemory`
  - On each user message, calls `memory_agent.result(...)` and displays the response

- **`memory_agent.py`**
  - Creates a `ChatBedrock` instance and defines a set of LangChain `Tool`s that wrap functions from `api_integration.py`
  - Defines an instruction-heavy router prompt that:
    - Parses the user’s intent from the current command
    - Chooses the right tool (e.g., raise request, get entitlements, get pending requests)
  - Uses `ConversationalChatAgent` + `AgentExecutor` to execute tools and return a final text answer

- **`api_integration.py`**
  - Contains the actual HTTP calls to SailPoint IdentityIQ REST endpoints (proxied via ngrok)
  - Reads basic auth credentials from `auth.txt`, base64-encodes them, and sets `Authorization: Basic ...` headers
  - Implements helpers such as:
    - `get_user_entitlements`, `get_user_application_entitlements`
    - `get_application_entitlements`
    - `get_user_roles`
    - `get_pending_requests`
    - `get_approver_details`
    - `get_request_status`
    - `raise_identity_request` (returns a direct IdentityIQ request link when successful)

---

## Prerequisites

- **Python** 3.10+ (recommended)
- **pip** for dependency installation
- An **AWS account** with:
  - Access to **Bedrock**
  - The **Claude 3 Haiku** model enabled (`anthropic.claude-3-haiku-20240307-v1:0`)
  - A local AWS profile named `krishna_paruchuri` (or update the code to use your own profile)
- A reachable **SailPoint IdentityIQ** REST endpoint, exposed via ngrok or similar, matching the URLs configured in `api_integration.py`
- An `auth.txt` file containing `username:password` for Basic Auth to the SailPoint endpoint

---

## Installation

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configuration

- **AWS Bedrock credentials**
  - Configure your AWS credentials in `~/.aws/credentials` and `~/.aws/config`
  - Ensure the profile name in both `Request_Manager.py` and `memory_agent.py` matches your profile  
    (currently: `krishna_paruchuri`)

- **SailPoint / ngrok URL**
  - In `api_integration.py`, update `sailpoint_url` to point to your IdentityIQ REST base URL:
    ```python
    sailpoint_url = "https://<your-ngrok-domain>.ngrok-free.app/iiq/plugin/rest/identityai"
    ```

- **Basic auth credentials**
  - Create an `auth.txt` file in the project root:
    ```text
    username:password
    ```
  - This is read by `get_encoded_credentials` in `api_integration.py`.

---

## Running the App

From the project root:

```bash
streamlit run Request_Manager.py
```

Then open the URL that Streamlit prints (usually `http://localhost:8501`) in your browser.

---

## Usage Examples

Once the app is running, try prompts like:

- **Raise an access request**
  - “Raise an access request for `james` to get `PlanReview`.”
  - “Give me `PlanReview` access.”

- **Check request status**
  - “What is the status of request `12345`?”
  - “Who is the approver for request `12345`?”

- **View roles and entitlements**
  - “What roles do I have?”
  - “Show all entitlements for `vishnu`.”
  - “What entitlements does `vishnu` have in `Fortuna-loan-AppUsers`?”

- **Inspect application entitlements**
  - “List the entitlements available for `Fortuna-loan-AppUsers`.”

- **Pending requests**
  - “Show my pending requests.”
  - “Show pending requests for `vishnu`.”

The agent will decide which tools to call and return structured answers (tables or bullet lists) where appropriate.

---

## Project Structure

- `Request_Manager.py` – Streamlit UI entrypoint
- `memory_agent.py` – LangChain agent, tools, and routing prompt
- `api_integration.py` – SailPoint IdentityIQ REST API integration helpers
- `requirements.txt` – Python dependencies
- `README.md` – This documentation

---

## Notes & Limitations

- The current implementation assumes:
  - A working ngrok tunnel or otherwise reachable IdentityIQ REST endpoint
  - Credentials in `auth.txt` are valid and authorized
  - The default user `vishnu` is used when no username is provided
- Error messages from the SailPoint API are surfaced directly back to the user where possible.

If you change endpoints, authentication, or default usernames, update `api_integration.py` and `memory_agent.py` accordingly.