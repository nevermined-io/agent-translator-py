from langchain_community.llms import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class Translator:
    """
    A class responsible for translating text using OpenAI's API.
    """

    def __init__(self, openai_api_key):
        """
        Initializes the Translator with the OpenAI API key.

        Args:
            openai_api_key (str): The OpenAI API key.
        """
        llm = OpenAI(api_key=openai_api_key)

        # Define a prompt template for the translation task
        prompt_template = PromptTemplate(
            input_variables=["text"],
            template="Translate the following text to Spanish:\n\n{text}"
        )

        # Define a translation chain using the prompt template and the OpenAI LLM
        self.chain = prompt_template | llm | StrOutputParser()

    def translate_text(self, input_text):
        """
        Translates the given text to Spanish.

        Args:
            input_text (str): The text to translate.

        Returns:
            str: The translated text.
        """

        # Execute the translation chain with the input text
        translated_text = self.chain.invoke({"text": input_text})

        return translated_text
