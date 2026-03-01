from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryBufferMemory
from langchain_aws import ChatBedrock
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
    ConversationalChatAgent
)
from langchain.agents import initialize_agent
from langchain import hub
from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain.memory import ChatMessageHistory

from langchain.globals import set_verbose

set_verbose(True)

from raise_request import get_role_id
from api_integration import get_user_entitlements, get_user_application_entitlements, get_user_roles, get_pending_requests, get_approver_details, get_request_status, raise_identity_request, get_application_entitlements

def result(input_text, conversational_memory):
    llm=ChatBedrock(
        # credentials_profile_name='default',
        credentials_profile_name='krishna_paruchuri',
        model_id='anthropic.claude-3-haiku-20240307-v1:0',
        # model_id='anthropic.claude-v2:1',
        # model_id='amazon.titan-text-express-v1',
        model_kwargs= {
            "max_tokens": 300,
            "temperature": 0,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman:"]} )


    # request_status_tools = [
    #     Tool(
    #             name="Get the role id",
    #             func=get_role_id,
    #             description="Use this tool to get the role id as an integer from the role name."
    #         ),
    #         Tool(
    #             name="Get Request Status",
    #             func=get_request_status,
    #             description="Use this tool to get the status of a request with a specific role id."
    #         ),
    # ]
    
    # request_status_prompt = """Get the role id as an integer from the provided role name and get the request status using the role id. 
    # ONLY Use TOOL RESPONSE to provide the output, don't ever use the chat history or any other information while answering the status of the request."""
    # request_status_agent = ConversationalChatAgent.from_llm_and_tools(llm=ChatBedrock(
    #     credentials_profile_name='default',
    #     model_id='anthropic.claude-3-haiku-20240307-v1:0',
    #     # model_id='anthropic.claude-v2:1',
    #     # model_id='amazon.titan-text-express-v1',
    #     model_kwargs= {
    #         "max_tokens": 300,
    #         "temperature": 0,
    #         "top_p": 0.9,
    #         "stop_sequences": ["\n\nHuman:"]}), tools=request_status_tools, system_message=request_status_prompt)
    # request_status_agent_executor = AgentExecutor.from_agent_and_tools(agent=request_status_agent, tools=request_status_tools, memory=conversational_memory, handle_parsing_errors=True)


    # raise_request_tools = [
    #         Tool(
    #             name = "Raise Request",
    #             func = insert_request,
    #             description = "Use this tool to raise a request with the provided role name and the user."
    #         ),
    #     ]
    
    # raise_request_prompt = """Raise a request using the provided role name for the provided user. Provide the input to the function as `role name,user name` if both role name and user name is provided. If the user name is not provided, provide just the `role name` as an input. 
    # Return the link returned from the function in the output for the user to verify that the request is raised. If the request has not been raised due to some error, summarize the error and provide it as output.
    # Provide the output in the format as shown below:
    # Mention that the request has been raised for the user.
    # Link: Request Link to verify that the request has been raised."""
    # raise_request_agent = ConversationalChatAgent.from_llm_and_tools(llm=ChatBedrock(
    #     credentials_profile_name='default',
    #     model_id='anthropic.claude-3-haiku-20240307-v1:0',
    #     # model_id='anthropic.claude-v2:1',
    #     # model_id='amazon.titan-text-express-v1',
    #     model_kwargs= {
    #         "max_tokens": 300,
    #         "temperature": 0,
    #         "top_p": 0.9,
    #         "stop_sequences": ["\n\nHuman:"]} ), tools=raise_request_tools, system_message=raise_request_prompt)
    # raise_request_agent_executor = AgentExecutor.from_agent_and_tools(agent=raise_request_agent, tools=raise_request_tools, memory=conversational_memory, handle_parsing_errors=True)


    # roles_tools = [
    #         Tool(
    #             name="Get all the roles",
    #             func=get_all_roles,
    #             description="Use this tool to get all the roles."
    #         ),
    #         Tool(
    #             name="Get the roles of the user",
    #             func=get_user_roles,
    #             description="Use this tool to get the roles of the user."
    #         ),
    #     ]
    
    # roles_prompt = """Analyze the user's query and determine the user's intent.
    # If the user wants to get all the available roles, provide all the available roles in a table format.
    # If the user wants to get all the roles that he have access to the user, provide all the available roles for the user in a table format."""

    # roles_agent = ConversationalChatAgent.from_llm_and_tools(llm=ChatBedrock(
    #     credentials_profile_name='default',
    #     model_id='anthropic.claude-3-haiku-20240307-v1:0',
    #     # model_id='anthropic.claude-v2:1',
    #     # model_id='amazon.titan-text-express-v1',
    #     model_kwargs= {
    #         "max_tokens": 300,
    #         "temperature": 0,
    #         "top_p": 0.9,
    #         "stop_sequences": ["\n\nHuman:"]} ), tools=roles_tools, system_message=roles_prompt)
    # roles_agent_executor = AgentExecutor.from_agent_and_tools(agent=roles_agent, tools=roles_tools, memory=conversational_memory, handle_parsing_errors=True)

    # def request_status_agent_executor_wrapper(original_prompt):
    #     return request_status_agent_executor.invoke(input={"input": original_prompt})
    
    def raise_request_agent_executor_wrapper(original_prompt):
        return raise_request_agent_executor.invoke(input={"input": original_prompt})
    
    # def roles_agent_executor_wrapper(original_prompt):
    #     return roles_agent_executor.invoke(input={"input": original_prompt})

    # # def request_status_agent_executor_wrapper(original_prompt):
    # #     if not original_prompt.strip():
    # #         return request_status_agent_executor.invoke(input={"input": original_prompt})

    # # def raise_request_agent_executor_wrapper(original_prompt):
    # #     if not original_prompt.strip():
    # #         return raise_request_agent_executor.invoke(input={"input": original_prompt})
        

    # # def roles_agent_executor_wrapper(original_prompt):
    # #     if not original_prompt.strip():
    # #         return roles_agent_executor.invoke(input={"input": original_prompt})

    
    tools = [
        # Tool(
        #     name="Raise Request Agent",
        #     func=raise_request_agent_executor_wrapper,
        #     description="""useful when you need to raise a request for the given role name and the user.""",
        # ),
        # Tool(
        #     name="Request Status Agent",
        #     func=request_status_agent_executor_wrapper,
        #     description="""useful when you need to provide status for the given role name.""",
        # ),
        # Tool(
        #     name="Get the entitlements of the user",
        #     func=get_user_entitlements,
        #     description="Use this tool to get entitlements of the user."
        #     ),
        Tool(
            name="Raise Identity Request",
            func=raise_identity_request,
            description="""Use this tool to raise a request for a user for a given application and attribute.
            Provide input in the format `user_name, entitlement`.
            Example: `'james', 'PlanReview'`.
            - If no user is provided in the current command and an entitlement is specified, use: `'','entitlement'` to raise the request for the current user for the entitlement."""
        ),
        Tool(
            name="Get the roles of the user",
            func=get_user_roles,
            description="Use this tool to get the roles of the user."
        ),
        # Tool(
        #     name="Clone Access",
        #     func=clone_accesses,
        #     description="""Use this tool to clone roles and entitlements from the specified source user to the specified target user in the current command. Provide input in the format `'' or source_user, '' or target_user`.
        #         Example: `'Barbara.Wilson',''` for cloning from Barbara to the current user.
        #         Or `'','Barbara.Wilson'` for cloning from the current user to Barbara.
        #         Or `'Aaron.Nichols','Barbara.Wilson'` for cloning from Aaron to Barbara."""
        # ),
        Tool(
            name="Get User Entitlements",
            func=get_user_entitlements,
            description="""Use this tool to get the list of entitlements for a given user across all applications. Input should be in the format: `user_name`. Output the entitlements for each application in a table format."""
        ), 
        Tool(
            name="Get User Entitlements for a Specific Application",
            func=get_user_application_entitlements,
            description="""Use this tool to get the list of entitlements for a given user for a specific application. Input should be in the format: `user_name, application_name`.
            Example:
            - If no specific user or "me" is provided in the current command, and an application is specified, use: `'','application'` to get the entitlements for the current user in the application.
            - If both user and application are provided in the current command, use: `'user','application'` to get the entitlements for the user for the application.
            """,
        ),
        Tool(
            name="Get Request Status by ID",
            func=get_request_status,
            description="""Use this tool to get the request status for a given request ID. Input the request ID as an argument."""
        ),
        # Tool(
        #     name="Get Requests for a Given Period",
        #     func=get_requests_for_period,
        #     description="""Use this tool to retrieve all request statuses for a given user within a specified period. Input the username as an argument. Input '' if no username is provided. Output the request ids along with the entitlemnt or role name for each request."""
        # ),
        Tool(
            name="Get Approver Details by Request ID",
            func=get_approver_details,
            description="""Use this tool to get the current approver details for a specific request ID. Input the request ID as an argument. Output the request ids along with the entitlemnt or role name for each request."""
        ),
        Tool(
            name="Get Pending Requests for a User",
            func=get_pending_requests,
            description="""Use this tool to get all pending requests for a specific user. Input the username as an argument. Input '' if no username is provided. Output the request ids along with the entitlemnt or role name for each request."""
        ),
        Tool(
            name="Get Application Entitlements",
            func=get_application_entitlements,
            description="""Use this tool to get the entitlements for a given application name. Input the application name as an argument."""
        ), 
    ]

    # - If the user wants to get all the entitlements they have access to, call the `get_user_entitlements` function with the username as an argument and provide all available entitlements along with their respective applications in the output as a table. If no entitlements are found, mention 'No entitlements assigned.' If there is no specific user mentioned, pass an empty string '' to the function.
    
    # - If the user requests entitlements for a specific application, call the `get_user_entitlements` function with the `username, application name` as argument. If no entitlements are found for that application, mention 'No entitlements assigned for this application'. If there is no specific user mentioned, pass an empty string '' for the username, and for the application name pass an empty string '' to the function.

    # router_prompt = """
    # Analyze the user's query and determine the user's intent accurately without assumptions. Pass the input to the tools only from the current command, Do not use variables from the conversation history.
    
    # - If the user wants to get all the roles they have access to, call the `get_user_roles` function with the username as an argument and provide all available roles for the user in the output as a table. If there are no roles, mention 'No roles assigned.' If there is no specific user mentioned, pass an empty string '' to the function.

    # - If the user wants to get the entitlements information, use the `Get Entitlements Information` tool. Only use the current command to get the user and application information.
        # - If the user asks to retrieve **entitlements information**, use the `Get Entitlements Information` tool.
    
    # - If the user wants to clone accesses from one user to another, use the `clone access` tool. Provide the request links explicitly along with the relevant information in the output for clone access.

    # - If the user wants to raise a request use the `raise request agent` tool.

    # - If the user wants to get the status of a request use the `request status agent` tool.

    # - If the user doesn't ask for any of the above, reply accordingly without using any tools.

    # Ensure that the response is clear and follows the instructions precisely.
    # """

    # router_prompt = """
    # Analyze the user's query and determine the intent based on the current command accurately without assumptions.

    # - If the user asks to **raise a request** for a user for a specific user and entitlement, use the `Raise Request` tool. Input should be in the format: `user_name, entitlement`. Provide the request link in the ouput for the user.
    # - If the user asks for request status using a request ID, use the Get Request Status by ID tool. Present the available fields in a bulleted list or a table. Only include the available fields (such as Request ID, Application Name, Entitlement or Role, Approval Status, Request Description, Approvers, Provisioning Status, and Message), and omit any missing fields. Do not output the information in paragraph form.
    # - If the user asks for **requests over a period** for a specific **user**, use the `Get Requests for a Given Period` tool. Provide the request ids along with the entitlement or role name in the output. If there are many requests, show the top 5 and mention the total number of requests.
    # - If the user asks for **approver details** for a specific **request ID**, use the `Get Approver Details by Request ID` tool.
    # - If the user asks for **pending requests** for a specific **user**, use the `Get Pending Requests for a User` tool. If there are many pending requests show the top 5 and mention the total number of pending requests.  Explicitly output the request id, entitlement or role name, application name, and the approval state for each request in the chat.
    # - If the user asks to **raise a request** for a role or a user, use the `Raise Request Agent` tool.
    # - If the user asks to **clone access** between users, use the `Clone Access` tool.
    # - If the user asks to retrieve **user roles**, use the `Get the Roles of the User` tool.
    # - If the user asks for **user entitlements**, use the `Get User Entitlements` tool. Input should be in the format: `user_name`.
    # - If the user asks for **user entitlements for a specific application**, use the `Get User Entitlements for a Specific Application` tool. Input should be in the format: `user_name, application_name`.
    # - If the user asks to retrieve **entitlements information** for a specific **application**, use the `Get Application Entitlements` tool. Return the list of entitlements for the application, and if the application is not found, return a message saying that the application is not found.
    # - If none of the above apply, provide a relevant response without using any tools.

    # Ensure clarity in the response and follow the instructions strictly.
    # """

    router_prompt = """
    Analyze the user's query and determine the intent based on the current command accurately without assumptions.

    - If the user asks to **raise a request** for a user for a specific user and entitlement, use the `Raise Request` tool. Input should be in the format: `user_name, entitlement`. Provide the request link in the ouput for the user.
    - If the user asks for request status using a request ID, use the Get Request Status by ID tool. Present the available fields in a bulleted list or a table. Only include the available fields (such as Request ID, Application Name, Entitlement or Role, Approval Status, Request Description, Approvers, Provisioning Status, and Message), and omit any missing fields. Do not output the information in paragraph form.
    - If the user asks for **requests over a period** for a specific **user**, use the `Get Requests for a Given Period` tool. Provide the request ids along with the entitlement or role name in the output. If there are many requests, show the top 5 and mention the total number of requests.
    - If the user asks for **approver details** for a specific **request ID**, use the `Get Approver Details by Request ID` tool.
    - If the user asks for pending requests for a specific user, use the Get Pending Requests for a User tool. If there are many pending requests, show the top 5 and mention the total number of pending requests. Explicitly output the Request ID, Entitlement or Role Name, Application Name, and Approval Status in a table format. Ensure the table includes column headers for each field, with each request's details shown in a separate row. Do not provide the information in paragraph form.
    - If the user asks to **raise a request** for a role or a user, use the `Raise Request Agent` tool.
    - If the user asks to **clone access** between users, use the `Clone Access` tool.
    - If the user asks to retrieve **user roles**, use the `Get the Roles of the User` tool.
    - If the user asks for **user entitlements**, use the `Get User Entitlements` tool. Input should be in the format: `user_name`.
    - If the user asks for **user entitlements for a specific application**, use the `Get User Entitlements for a Specific Application` tool. Input should be in the format: `user_name, application_name`.
    - If the user asks to retrieve **entitlements information** for a specific **application**, use the `Get Application Entitlements` tool. Return the list of entitlements for the application, and if the application is not found, return a message saying that the application is not found.
    - If none of the above apply, provide a relevant response without using any tools.

    Ensure clarity in the response and follow the instructions strictly.
    """

    router_agent = ConversationalChatAgent.from_llm_and_tools(llm=ChatBedrock(
        # credentials_profile_name='default',
        credentials_profile_name='krishna_paruchuri',
        model_id='anthropic.claude-3-haiku-20240307-v1:0',
        # model_id='anthropic.claude-v2:1',
        # model_id='amazon.titan-text-express-v1',
        model_kwargs= {
            "max_tokens": 300,
            "temperature": 0,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman:"]} ), tools=tools, system_message=router_prompt)
    router_agent_executor = AgentExecutor.from_agent_and_tools(agent=router_agent, tools=tools, memory=conversational_memory, handle_parsing_errors=True)

    result = router_agent_executor.invoke(input={"input":input_text})
    return result["output"]