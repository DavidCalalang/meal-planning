from google import genai
from google.genai.types import HttpOptions
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import scrolledtext

def configure():
    load_dotenv()

def generate_evaluation_prompt(user_inputs):
    with open('prompt.txt', 'r') as file:
        prompt_template = file.read()

    workout_type = user_inputs["workout_type"]
    workout_duration = user_inputs["workout_duration"]
    workout_intensity = user_inputs["workout_intensity"]

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

def get_user_inputs():
    root = tk.Tk()
    root.title("Get user inputs")

    # Define StringVars to store selected values
    var1 = tk.StringVar(value="")  # For first question
    var2 = tk.StringVar(value="")  # For second question
    var3 = tk.StringVar(value="")  # For third question

    user_inputs = {}

    # Function to get and show the selected options
    def submit():
        user_inputs["workout_type"] = var1.get()
        user_inputs["workout_duration"] = var2.get()
        user_inputs["workout_intensity"] = var3.get()

        root.destroy()

    # Helper function to create a group of radiobuttons
    def create_radio_group(label_text, variable, options):
        frame = tk.LabelFrame(root, text=label_text, padx=10, pady=5)
        frame.pack(padx=10, pady=5, fill="both", expand=True)
        
        for opt in options:
            rb = tk.Radiobutton(frame, text=opt, variable=variable, value=opt)
            rb.pack(anchor='w')

    # Define the choices
    options1 = ["Running", "Weight Lifting", "Rock Climbing"]
    options2 = ["30 minutes", "60 minutes", "90 minutes", "120 minutes"]
    options3 = ["Low", "Medium", "High"]

    # Create radiobutton groups
    create_radio_group("Select workout type", var1, options1)
    create_radio_group("Select workout duration", var2, options2)
    create_radio_group("Select workout intensity", var3, options3)

    # Submit button
    submit_btn = tk.Button(root, text="Submit", command=submit)
    submit_btn.pack(pady=10)

    root.mainloop()

    return user_inputs

def output_format(llm_output):
    root = tk.Tk()
    root.title("Format Output")

    # --- LLM Response Section ---
    response_label = tk.Label(root, text="LLM Response")
    response_label.pack(pady=(10, 2), anchor='w')

    response_text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
    response_text_area.insert(tk.INSERT, llm_output)
    response_text_area.pack(expand=True, fill='both', padx=10, pady=(0, 10))
    response_text_area.config(state=tk.DISABLED)
    
    root.mainloop()

def main():
    configure()

    user_inputs = get_user_inputs()
    prompt = generate_evaluation_prompt(user_inputs)

    llm_output = gemini_request(prompt)
    output_format(llm_output.text)


if __name__ == "__main__":
    main()