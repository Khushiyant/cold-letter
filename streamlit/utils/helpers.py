from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
import PyPDF2
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class ColdMailing:
    """
    Generates a cold email template.

    Parameters
    ----------
    company_name : str
    name : str
    email : str
    resume : file
    """

    def __init__(self) -> None:
        self.llm = OpenAI(temperature=0.6, max_tokens=1000)

        search = GoogleSearchAPIWrapper(k=1)

        self.tools = [
            Tool(
                name="Google Search",
                description="Search Google for recent results about the company or professor. Use it only once",
                func=search.run,
            )
        ]

        self.agent = initialize_agent(
            self.tools, self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True)

    def generate(self, target_name, name, resume, type, requested_position):
        self.name = name
        self.target_name = target_name
        self.resume = resume
        return self.agent.run(f"""
            Write a cold mail to {type} called {target_name} for the position of {requested_position} with following conditons:
            if it is a professor then use his/her top 3 best research paper work by using google scholar else if it is a company then use my info to show my passion.

            Use the following information to create the cold mail:
            {resume}
            """)


class PDFTextExtractor:
    """
    Extracts text from a PDF file.

    Parameters
    ----------
    file : file
        The PDF file to extract text from.

        Returns
        -------
        text : str
    """

    def extract(self, file):
        text = str()
        fileReader = PyPDF2.PdfReader(file)
        for page in fileReader.pages:
            text += page.extract_text()

        return text
