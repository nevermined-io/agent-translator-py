[![banner](https://raw.githubusercontent.com/nevermined-io/assets/main/images/logo/banner_logo.png)](https://nevermined.io)

Translator Agent using Nevermined's Payments API
================================================

> Python agent that translates text using OpenAI's API and integrates with Nevermined's task system.

> [nevermined.io](https://nevermined.io)

* * *

Table of Contents
-----------------

*   [Translator Agent using Nevermined's Payments API](#translator-agent-using-nevermineds-payments-api)
    *   [Introduction](#introduction)
    *   [Getting Started](#getting-started)
        *   [Prerequisites](#prerequisites)
        *   [Installation](#installation)
    *   [Tutorial](#tutorial)
        *   [Implementing the Nevermined Integration](#implementing-the-nevermined-integration)
            *   [1. Setting Up the Environment](#1-setting-up-the-environment)
            *   [2. Installing Dependencies](#2-installing-dependencies)
    *   [Configuring Environment Variables](#configuring-environment-variables)
        *   [1. Nevermined API Key (`NVM_API_KEY`)](#1-nevermined-api-key-nvm_api_key)
        *   [2. Agent DID (`AGENT_DID`)](#2-agent-did-agent_did)
        *   [3. Other Environment Variables](#3-other-environment-variables)
        *   [4. Setting Up the `.env` File](#4-setting-up-the-env-file)
    *   [Integrating Nevermined Payment Protocol into Your Agent](#integrating-nevermined-payment-protocol-into-your-agent)
        *   [Initializing the Payments Client](#initializing-the-payments-client)
        *   [Subscribing to the AI Protocol](#subscribing-to-the-ai-protocol)
        *   [Handling Incoming Tasks](#handling-incoming-tasks)
            *   [Retrieving Step Information](#retrieving-step-information)
            *   [Processing the Task](#processing-the-task)
            *   [Updating Task Status and Logging](#updating-task-status-and-logging)
    *   [License](#license)

* * *

Introduction
------------

The Translator Agent is a Python application that translates text using OpenAI's API and integrates with Nevermined's Payments API to handle task management and execution. This agent listens for translation tasks assigned to it via Nevermined's AI protocol, processes them, and updates the task status accordingly.

Getting Started
---------------

### Prerequisites

*   Python 3.10 or higher
*   Nevermined API Key
*   OpenAI API Key
*   Git

### Installation

1.  **Clone the repository**
    
    ```bash
    git clone https://github.com/nevermined-io/agent-translator-py.git
    cd agent-translator-py
    ```
    
2.  **Create a virtual environment**
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    
3.  **Install the dependencies**
    
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **Configure environment variables**
    
    *   Copy the `.env.example` file to `.env`
        
        ```bash
        cp .env.example .env
        ```
        
    *   Edit the `.env` file and add your API keys and configuration:
        
        ```makefile
        NVM_API_KEY=your_nevermined_api_key
        OPENAI_API_KEY=your_openai_api_key
        NVM_ENVIRONMENT=staging  # or 'production' as per your setup
        AGENT_DID=your_agent_did
        ```
        
5.  **Run the agent**
    
    ```bash
    python main.py
    ```
    

Tutorial
--------

### Implementing the Nevermined Integration

This tutorial will guide you through the implementation of the Nevermined integration in the translator agent.

#### 1\. Setting Up the Environment

Ensure you have the following files in your project:

*   `main.py`: The main script where the agent logic resides.
*   `translator.py`: Contains the translation logic using OpenAI's API.
*   `.env`: Stores your environment variables (API keys and configurations).
*   `.env.example`: An example of the `.env` file structure.
*   `requirements.txt`: Lists all the Python dependencies required for the project.

#### 2\. Installing Dependencies

Install the necessary Python packages listed in `requirements.txt`. The key dependencies related to Nevermined are:

*   `payments-py`: The Python SDK for Nevermined's Payments API.
*   `python-dotenv`: For loading environment variables from a `.env` file.
*   `langchain-community`: For working with language models.
*   `openai`: The official OpenAI Library

```bash
pip install -r requirements.txt
```

Configuring Environment Variables
---------------------------------

Before integrating Nevermined into your agent, you need to configure some environment variables.

1.  **Nevermined API Key (`NVM_API_KEY`)**
    
    *   Generate your Nevermined API Key by logging into your account at [nevermined.app](https://nevermined.app).
    *   Navigate to your profile settings to create or retrieve your API key.
2.  **Agent DID (`AGENT_DID`)**
    
    *   The Agent Decentralized Identifier (DID) corresponds to the asset you create on the Nevermined platform.
    *   To obtain your Agent DID:
        *   Create a subscription plan and an asset on [nevermined.app](https://nevermined.app).
        *   The DID of the asset you created will serve as your Agent DID.
3.  **Other Environment Variables**
    
    *   **OpenAI API Key (`OPENAI_API_KEY`)**: If your agent uses OpenAI's API, set this variable with your OpenAI API key.
    *   **Nevermined Environment (`NVM_ENVIRONMENT`)**: Specify the Nevermined environment you wish to connect to (`staging`, `production`, etc.).
4.  **Setting Up the `.env` File**
    
    Create a `.env` file in your project's root directory and add the following:
    
    ```makefile
    NVM_API_KEY=your_nevermined_api_key
    OPENAI_API_KEY=your_openai_api_key
    NVM_ENVIRONMENT=staging  # or 'production' as per your setup
    AGENT_DID=your_agent_did
    ```
    
    This file will store your sensitive information securely and keep it out of your source code.
    

Integrating Nevermined Payment Protocol into Your Agent
-------------------------------------------------------

Integrating Nevermined into your agent involves several key steps: initializing the Payments client, subscribing to the AI protocol, handling incoming tasks, and updating task status and logging.

### Initializing the Payments Client

To interact with Nevermined's Payments API, you need to initialize a `Payments` client in your agent's code. This client will handle authentication and provide methods to communicate with the Nevermined network.

```python
from payments_py import Environment, Payments

# Initialize the Payments object with the necessary configurations
payment = Payments(
    app_id="your_agent_app_id",
    nvm_api_key=os.getenv('NVM_API_KEY'),
    version="1.0.0",
    environment=Environment.get_environment(os.getenv('NVM_ENVIRONMENT')),
    ai_protocol=True,
)
```

In this snippet:

*   **`app_id`**: A unique identifier for your agent application.
*   **`nvm_api_key`**: Your Nevermined API key from the environment variables.
*   **`version`**: The version of your agent application.
*   **`environment`**: Specifies the Nevermined environment to connect to.
*   **`ai_protocol`**: Enables AI protocol features in the Payments client.

By initializing the Payments client, your agent is now authenticated and ready to interact with the Nevermined network.

### Subscribing to the AI Protocol

Next, you need to subscribe your agent to the AI protocol to start receiving tasks assigned to it. This involves setting up an asynchronous listener that triggers whenever a new task is available.

```python
import asyncio

# Subscribe to the AI protocol to receive tasks assigned to this agent
subscription_task = asyncio.get_event_loop().create_task(
    payment.ai_protocol.subscribe(
        agent.run,  # The method to handle incoming tasks
        join_account_room=False,
        join_agent_rooms=[os.getenv('AGENT_DID')],  # Subscribe to your agent's DID
        get_pending_events_on_subscribe=False
    )
)
```

Here:

*   **`agent.run`**: The callback function in your agent that processes incoming tasks.
*   **`join_account_room`**: Set to `False` to focus on agent-specific events.
*   **`join_agent_rooms`**: A list containing your Agent DID to subscribe to tasks assigned to your agent.
*   **`get_pending_events_on_subscribe`**: If `True`, retrieves any pending events upon subscription.

This subscription ensures your agent listens for and receives tasks from the Nevermined network.

### Handling Incoming Tasks

When a task is assigned to your agent, the callback function you specified (`agent.run`) is invoked. This function should handle retrieving task details, processing the task, and updating its status. It will receive `data` as a parameter. A dictionary containing task and step information.

#### Retrieving Step Information

First, retrieve the details of the task's current step using the `step_id` provided in the incoming data.

```python
# Retrieve the current step information using the step_id from data
step = payment.ai_protocol.get_step(data['step_id'])
```

*   **`data['step_id']`**: The identifier of the task step provided by the Nevermined network.
*   **`get_step()`**: Fetches the details of the specified step, such as input data and status.

Check if the step is pending before proceeding:

```python
if step['step_status'] != AgentExecutionStatus.Pending.value:
    print('Step status is not pending')
    return
```

This ensures that your agent only processes steps that are ready for execution.

#### Processing the Task

Extract the necessary input from the step and perform the required processing. For example, if your agent translates text, you would retrieve the text to translate:

```python
# Extract the input text that needs to be processed
input_text = step['input_query']

# Perform the task using your agent's processing logic
result = your_processing_function(input_text)
```

Replace `your_processing_function` with the actual function or method your agent uses to process the task.

#### Updating Task Status and Logging

After processing the task, update the task's status and provide any output or results back to the Nevermined network.

```python
# Update the task step with the result and mark it as completed
payment.ai_protocol.update_step(
    did=data['did'],
    task_id=data['task_id'],
    step_id=data['step_id'],
    step={
        'step_id': data['step_id'],
        'task_id': data["task_id"],
        'step_status': AgentExecutionStatus.Completed.value,
        'output': result,
        'is_last': True  # Set to True if this is the final step
    },
)
```

Here:

*   **`update_step()`**: Updates the step's status and output in the Nevermined network.
*   **`step_status`**: Set to `Completed` to indicate successful completion.
*   **`output`**: The result of your agent's processing.
*   **`is_last`**: Indicates whether this is the last step in the task.

Log the completion of the task for tracking and debugging purposes:

```python
await payment.ai_protocol.log_task(TaskLog(
    task_id=step['task_id'],
    message='Task completed successfully.',
    level='info',
    task_status=AgentExecutionStatus.Completed.value
))
```

In case of errors during processing, handle exceptions and update the task status accordingly:

```python
except Exception as e:
    print("Error during task processing:", e)
    await payment.ai_protocol.log_task(TaskLog(
        task_id=step['task_id'],
        message=f'Error during task processing: {e}',
        level='error',
        task_status=AgentExecutionStatus.Failed.value
    ))
```

* * *

License
-------

```
Copyright 2024 Nevermined

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```