from google import genai
from google.genai.types import HttpOptions
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

def gemini_request(prompt):
    client = genai.Client(
        vertexai=True, project=os.getenv('project_id'), location=os.getenv('location')
    )

    contents = prompt
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=contents
    )

    return response

def main():
    configure()

    prompt = "Give me a recipe to use after a workout involving one hour of weight training."

    output = gemini_request(prompt)
    print(output.text)


if __name__ == "__main__":
    main()