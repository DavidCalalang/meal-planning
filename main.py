from google import genai
from google.genai.types import HttpOptions
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

def generate_evaluation_prompt(user_inputs):
    with open('prompt.txt', 'r') as file:
        prompt_template = file.read()

    workout_type = user_inputs[0]
    workout_duration = user_inputs[1]
    workout_intensity = user_inputs[2]

    prompt = prompt_template.format(
        workout_type=workout_type,
        workout_duration=workout_duration,
        workout_intensity=workout_intensity
    )

    return prompt

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

    #prompt = "Give me a recipe to use after a workout involving one hour of weight training."
    user_inputs = ["Boxing", "90 minutes", "High"]
    prompt = generate_evaluation_prompt(user_inputs)
    #print(prompt)

    output = gemini_request(prompt)
    print(output.text)


if __name__ == "__main__":
    main()