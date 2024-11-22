from dotenv import load_dotenv
import os
import asyncio
from payments_py import Environment, Payments
from payments_py.data_models import AgentExecutionStatus, TaskLog
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

# Retrieve API keys and environment variables from the system environment
nvm_api_key = os.getenv('NVM_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
environment = os.getenv('NVM_ENVIRONMENT')
agent_did = os.getenv('AGENT_DID')

class TranslatorAgent:
    """
    A translator agent that uses OpenAI's API and Nevermined's Payments API to translate text.

    Attributes:
        payment (Payments): An instance of the Payments class to interact with Nevermined's API.
    """

    def __init__(self, payment):
        """
        Initialize the TranslatorAgent with a Payments instance.

        Args:
            payment (Payments): The Payments instance for interacting with Nevermined's API.
        """
        self.payment = payment

    async def run(self, data):
        """
        Process incoming data to translate text using OpenAI's API and update task status via Nevermined's API.

        Args:
            data (dict): A dictionary containing task and step information.

        Returns:
            None
        """
        print("Data received:", data)

        # Retrieve the current step information using the step_id from data
        step = self.payment.ai_protocol.get_step(data['step_id'])

        # Check if the step status is pending; if not, exit the function
        if step['step_status'] != AgentExecutionStatus.Pending.value:
            print('Step status is not pending')
            return

        # Log the initiation of the translation task
        await self.payment.ai_protocol.log_task(TaskLog(
            task_id=step['task_id'],
            message='Starting translation...',
            level='info'
        ))

        # Extract the input text that needs to be translated
        input_text = step['input_query']

        try:
            # Initialize the OpenAI language model with the provided API key
            llm = OpenAI(openai_api_key=openai_api_key)

            # Define a prompt template for the translation task
            prompt_template = PromptTemplate(
                input_variables=["text"],
                template="Translate the following text to Spanish:\n\n{text}"
            )

            # Create an LLMChain with the language model and the prompt template
            translation_chain = LLMChain(llm=llm, prompt=prompt_template)

            # Execute the translation chain with the input text
            translated_text = translation_chain.run(text=input_text)

            # Print the translated text to the console for verification
            print('Translation:', translated_text)

            # Update the task step with the translated text and mark it as completed
            self.payment.ai_protocol.update_step(
                did=data['did'],
                task_id=data['task_id'],
                step_id=data['step_id'],
                step={
                    'step_id': data['step_id'],
                    'task_id': data["task_id"],
                    'step_status': AgentExecutionStatus.Completed.value,
                    'output': translated_text,
                    'is_last': True
                },
            )

            # Log the completion of the translation task
            await self.payment.ai_protocol.log_task(TaskLog(
                task_id=step['task_id'],
                message='Translation completed.',
                level='info',
                task_status=AgentExecutionStatus.Completed.value
            ))

        except Exception as e:
            # Handle any exceptions that occur during the translation process
            print("Error during translation:", e)
            # Log the error and update the task status to 'Failed'
            await self.payment.ai_protocol.log_task(TaskLog(
                task_id=step['task_id'],
                message='Error during translation',
                level='error',
                task_status=AgentExecutionStatus.Failed.value
            ))
            return

async def main():
    """
    The main function that initializes the Payments object, creates the TranslatorAgent,
    and subscribes to Nevermined's AI protocol to listen for incoming translation tasks.

    Returns:
        None
    """
    # Initialize the Payments object with the necessary configurations
    payment = Payments(
        app_id="translator_agent",
        nvm_api_key=nvm_api_key,
        version="1.0.0",
        environment=Environment.get_environment(environment),
        ai_protocol=True,
    )

    # Create an instance of the TranslatorAgent with the Payments object
    agent = TranslatorAgent(payment)

    # Subscribe to the AI protocol to receive tasks assigned to this agent
    subscription_task = asyncio.get_event_loop().create_task(
        payment.ai_protocol.subscribe(
            agent.run,
            join_account_room=False,
            join_agent_rooms=[agent_did],
            get_pending_events_on_subscribe=False
        )
    )

    # Print a message indicating the agent is subscribing to tasks
    print('Subscribing to agent DID:', agent_did)

    try:
        # Await the subscription task to keep the agent running
        await subscription_task
    except asyncio.CancelledError:
        # Handle the cancellation of the subscription task gracefully
        print("Subscription task was cancelled")

if __name__ == '__main__':
    # Run the main function using asyncio's event loop
    asyncio.run(main())
