import os
import base64
import anthropic
import matplotlib.pyplot as plt

FILE_LOCATION = "C:\\Users\\bandg\\Downloads\\Rebar.png"
ANTHROPIC_API_KEY = os.environ.get("DEMO_KEY")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_base64 = encode_image(FILE_LOCATION)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

message = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    system="You are a data analyst specializing in construction materials sales. Analyze the bar graph showing rebar sales trends over time.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "This is a bar graph showing quarterly sales trends for rebar. Please analyze the trends, identify patterns, and provide business insights about these rebar sales."
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_base64
                    }
                }
            ]
        }
    ]
)

print("Claude's Analysis of Rebar Sales Trends:")
print(message.content[0].text)