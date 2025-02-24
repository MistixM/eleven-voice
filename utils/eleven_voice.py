# Import the required libraries

import uuid
import configparser

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

""" 
Converts text to speech using Eleven Voice API

text: str -> text to convert
voice_id: str -> voice id to use
stability: float -> stability value
similarity: float -> similarity value
style: float -> style value
speed: float -> speed value 

"""

def text_to_speech(text: str, voice_id: str, stability: float, similarity: float, style: float, speed: float) -> str:
    config = configparser.ConfigParser()
    config.read('config.ini')

    client = ElevenLabs(
        api_key=config['Main']['ELEVEN_API']
    )

    # If you want to change output format refer the docs here: https://elevenlabs.io/docs/api-reference/websocket#properties-3
    # To change model_id please refer to the docs here: https://elevenlabs.io/docs/models#models-overview
    response = client.text_to_speech.convert(
        voice_id=voice_id,
        output_format='mp3_44100_192',
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=stability,
            similarity_boost=similarity,
            style=style,
            speed=speed,
        )
    )

    # Generate file name
    file_path = f"{uuid.uuid4()}.mp3"

    # Write the file and return it
    with open(file_path, 'wb') as f:
        for chunk in response:
            if chunk:
                f.write(chunk)
    
    print(f"File saved at {file_path}")

    return file_path


