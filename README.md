# Book bites

This project consists of two Python scripts, `generate.py` and `upload.py`, along with a `requirements.txt` file. These scripts enable you to generate video content and upload it to YouTube.

## Configuration

Before using the scripts, you need to configure the necessary environment variables for your API keys (OpenAI and ElevenLab) and YouTube authentication credentials. You can set these variables in a `.env` file or directly in your environment. Ensure that you have these variables properly configured before running the scripts.

Here are the required environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key.
- `ELEVENLABS_API_KEY`: Your ElevenLab's API key.
- YouTube Authentication Credentials: Set up YouTube authentication credentials using the [`youtube_upload`](https://github.com/pillargg/youtube-upload) library following its instructions.

## Requirements

Before getting started, ensure you have the required Python packages installed. You can install them using `pip` with the following command:

```bash
pip install -r requirements.txt
```

## Usage

### `generate.py`

This script generates video content. You can use it as follows:

```bash
python generate.py [title]
```

- `[title]` (optional): The title of the content you want to summarize. If not provided, you will be prompted to enter a title.

### `upload.py`

This script uploads the generated videos to YouTube. Make sure to authenticate your YouTube account as described above.

To upload videos, run:

```bash
python upload.py
```

This script will search for generated video files in the `./output` directory, upload them to your YouTube channel, and move the uploaded files to the `./uploaded` directory.
