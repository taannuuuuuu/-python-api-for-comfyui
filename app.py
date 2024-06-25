import json
import gradio as gr
import requests
import os
import time
from fastapi import FastAPI

URL = "http://127.0.0.1:8188/prompt"
OUTPUT_DIR="/Users/tanuraman/ComfyUI/output"

def get_latest_image(folder):
    files = os.listdir(folder)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpeg', '.jpg'))]
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    latest_image = os.path.join(folder, image_files[-1]) if image_files else None
    return latest_image

def start_queue(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data=data)

def generate_image(prompt_text, step_count):
    with open("workflow_api-2.json", "r") as file_json:
        prompt = json.load(file_json)
        prompt["6"]["inputs"]["text"] = f"digital artwork of a {prompt_text}"
        prompt["3"]["inputs"]["steps"] = step_count

    previous_image = get_latest_image(OUTPUT_DIR)

    start_queue(prompt)
    while True:
        latest_image = get_latest_image(OUTPUT_DIR)
        if latest_image != previous_image:
            return latest_image
        time.sleep(1)

demo = gr.Interface(fn=generate_image, inputs=["text", "text"], outputs=["image"])

# Use FastAPI with Gradio
app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}

@app.get("/gradio")
def gradio_ui():
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
