import os
import json
from youtube_upload.client import YoutubeUploader


def upload_video(video_path, json_path):
    uploader = YoutubeUploader()
    uploader.authenticate()

    with open(json_path, "r") as json_file:
        video_info = json.load(json_file)

    options = {
        "title": "Summary of " + video_info["title"],
        "description": video_info["description"],
        "tags": video_info["tags"],
        "privacyStatus": "private",
        "kids": False,
    }

    uploader.upload(video_path, options)


def main():
    output_directory = "./output"
    uploaded_directory = "./uploaded"

    # Ensure the 'uploaded' directory exists
    if not os.path.exists(uploaded_directory):
        os.makedirs(uploaded_directory)

    for filename in os.listdir(output_directory):
        if filename.endswith(".mp4"):
            video_id = filename.split(".")[0]
            json_filename = f"{video_id}.json"
            json_path = os.path.join(output_directory, json_filename)

            if os.path.exists(json_path):
                video_path = os.path.join(output_directory, filename)
                upload_video(video_path, json_path)

                # Move the video and JSON files to the 'uploaded' directory
                os.rename(video_path, os.path.join(uploaded_directory, filename))
                os.rename(json_path, os.path.join(uploaded_directory, json_filename))


if __name__ == "__main__":
    main()
