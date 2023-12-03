import os
import sys
from dotenv import load_dotenv
import json
import re
import uuid
from openai import OpenAI
import requests
from moviepy.editor import AudioFileClip, ImageClip

load_dotenv()

# Get the title from the command line
if len(sys.argv) > 1:
    title = " ".join(sys.argv[1:])
else:
    title = input("Enter the title: ")

# Make a request to OpenAI's chat endpoint
print("Generating text...")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
if len(title):
    prompt = (
        "Please summarize "
        + title
        + ". Give a down to earth but objective lecture. Include background and importance of the work. Write in paragraphs, and give each paragraph a title."
    )
else:
    prompt = "Tell me I'm amazing."
chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="gpt-4-1106-preview",
)
summary = re.sub(
    r"([*_`~]|#{1,6} |\[(.*?)\]\(.*?\))", "", chat_completion.choices[0].message.content
)

if len(title):
    prompt = (
        "Make a short list of five keywords for the book "
        + title
        + " separated by commas."
    )
else:
    prompt = "Make a short list of five keywords separated by commas."
chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="gpt-3.5-turbo",
)
tags = [x.strip() for x in chat_completion.choices[0].message.content.split(",")]

prompt = "Make a three sentence summary of the following text: \n\n" + summary
chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="gpt-3.5-turbo",
)
description = chat_completion.choices[0].message.content

# Create output directory
output_dir = "./output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save metadata
generation_id = str(uuid.uuid4())
metadata = {
    "summary": summary,
    "title": title,
    "tags": tags,
    "description": description,
}
with open(output_dir + "/" + generation_id + ".json", "w") as file:
    file.write(json.dumps(metadata))

# Make a request to ElevenLab's text-to-speech endpoint
print("Generating audio...")
url = "https://api.elevenlabs.io/v1/text-to-speech/flq6f7yk4E4fJM5XTYuZ"  # Michael
payload = {"text": summary}
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": os.environ.get("ELEVENLABS_API_KEY"),
}
response = requests.request("POST", url, json=payload, headers=headers)

# Save the audio file
print("Saving audio...")
temp_audio_file = output_dir + "/" + generation_id + ".mp3"
with open(temp_audio_file, "wb") as file:
    file.write(response.content)

# Save the video file
image_path = "./background.png"
audio_clip = AudioFileClip(temp_audio_file)
audio_clip = audio_clip.volumex(1.0)
image_clip = ImageClip(image_path, duration=audio_clip.duration)
final_clip = image_clip.set_audio(audio_clip)
final_clip.write_videofile(
    output_dir + "/" + generation_id + ".mp4",
    codec="libx264",
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    fps=24,
    remove_temp=True,
)
