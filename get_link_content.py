# get_link_content.py
import os
from dotenv import load_dotenv
import json
import requests
from bs4 import BeautifulSoup
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel

from langchain_groq import ChatGroq

load_dotenv()


# URL of the article
url = "https://www.axios.com/2024/04/30/microsoft-openai-lawsuit-copyright-newspapers-alden-global"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Create a directory to store the extracted content
output_dir = "extracted_content"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Extract article content
article_content = []
for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
    if element.text.strip():  # ignore empty elements
        article_content.append(f"{element.name}: {element.text.strip()}")

article_text = '\n'.join(article_content)

# Save the article content to a file
with open(os.path.join(output_dir, "article_content.txt"), 'w') as f:
    f.write(article_text)



llm = ChatGroq(
    model_name="llama3-8b-8192", verbose=True, temperature=0.7, groq_api_key=os.getenv('GROQ_API_KEY')
)

output_dir = "extracted_content"

with open(os.path.join(output_dir, "article_content.txt"), 'r') as f:
    article_text = f.read()

class Carousel(BaseModel):
    Cover_Title: str
    Cover_Subtext: str
    Slide_1_Title: str
    Slide_1_Subtext: str
    Slide_1_Type: str
    Slide_1_Image: str
    Slide_2_Title: str
    Slide_2_Subtext: str
    Slide_2_Type: str
    Slide_2_Image: str
    Slide_3_Title: str
    Slide_3_Subtext: str
    Slide_3_Type: str
    Slide_3_Image: str
    Slide_4_Title: str
    Slide_4_Subtext: str
    Slide_4_Type: str
    Slide_4_Image: str
    Slide_5_Title: str
    Slide_5_Subtext: str
    Slide_5_Type: str
    Slide_5_Image: str
    CTA_Title: str
    CTA_Subtext: str


# output_parser = CommaSeparatedListOutputParser()
parser = JsonOutputParser(pydantic_object=Carousel)


template = """
    You're a seasoned LinkedIn Carousel creator that drives user engagement. Write in simple vocabulary, active voice.

    Extract the most important info and organize it into engaging slides.

    Each slide should be designed with:
    - Title: An attention-grabbing headline
    - Subtext: A brief supporting statement
    - Image: Descriptive image context

    Please provide the following output format:

    Cover_Title, Cover_Subtext, 
    Slide_1_Title, Slide_1_Subtext, Slide_1_Type, Slide_1_Image
    Slide_2_Title, Slide_2_Subtext, Slide_2_Type, Slide_2_Image
    Slide_3_Title, Slide_3_Subtext, Slide_3_Type, Slide_3_Image
    Slide_4_Title, Slide_4_Subtext, Slide_4_Type, Slide_4_Image
    Slide_5_Title, Slide_5_Subtext, Slide_5_Type, Slide_5_Image
    CTA_Title, CTA_Subtext, CTA_Type

    Choose from the following slide templates (max 7 total slides):
    1. Cover: Title (max 45 char.), Subtext (optional, max 65 char.)
    3. List Slide: Heading (max 20 char.), Numbers List (max 5 points, 50 char. each)
    4. Big Text Slide: Heading (max 40 char.)
    5. Photo Top Slide: Title (max 20 char.), Subtext (max 125 char.)
    6. Photo Bottom Slide: Title (max 20 char.), Subtext (max 125 char.)
    7. Small Photo Bottom Slide: Title (max 40 char.), Subtext (max 100 char.)
    8. CTA: Title (max 30 char.), Subtext (optional, max 75 char.)

    NOTE: When including images, use this formula to describe them:
    Type, Subject, Setting, Mood/Color, Style, Emphasis.

    Type: Specify the image type (e.g., "photo," "illustration").

    Subject: Describe the main subject (e.g., "fluffy orange cat").

    Features: Highlight key features (e.g., "with green eyes").

    Setting: Mention the background or environment (e.g., "on a windowsill").

    Mood/Color: Convey the mood or color scheme (e.g., "at sunset with warm hues").

    Style: If needed, describe a specific artistic style (e.g., "reminiscent of Van Gogh").

    Emphasis: Reiterate any crucial element for emphasis.

    Example using the formula:
    "Illustration of a fluffy orange cat with green eyes on a windowsill at sunset with warm hues, reminiscent of Van Gogh. The cat is the primary focus."

    {format_instructions}
    Article Content: {input}
"""


prompt = PromptTemplate(
    template=template,  
    input_variables=["input"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

article_input = article_text

linkedin_chain = prompt | llm | parser

carousel_output = linkedin_chain.invoke({"input": article_input})

with open("article_content.json", "w") as f:
    json.dump(carousel_output, f, indent=4)
