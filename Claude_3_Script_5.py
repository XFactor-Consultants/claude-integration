#!/usr/bin/env python3
"""
Rebar Sales Trend Analyzer
--------------------------
This script analyzes quarterly sales trends for rebar products using Claude AI.
It loads a bar graph image of sales data, sends it to the Anthropic API,
and displays Claude's analysis of the trends and patterns.

Author: Refactored by Claude
Date: March 20, 2025
"""

import os
import base64
import threading
import time
import concurrent.futures
import anthropic
import matplotlib.pyplot as plt

# Configuration constants
FILE_LOCATION = "C:\\Users\\bandg\\Downloads\\Rebar.png"
ANTHROPIC_API_KEY = os.environ.get("DEMO_KEY")
MAX_RETRIES = 4
TIMEOUT_SECONDS = 40

def encode_image(image_path):
    """
    Encode an image file to base64 format for API transmission.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64-encoded image data
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def make_api_call(image_base64):
    """
    Send the encoded image to Anthropic's API for analysis.
    
    Args:
        image_base64 (str): Base64-encoded image data
        
    Returns:
        object: API response message or None if error occurs
    """
    try:
        # Initialize Anthropic client
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        # Create API request with image and prompt
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
        return message
    except NameError:
        print("API Key not recognized")
        return None
    except Exception as e:
        print(f"Error making API call: {e}")
        return None

def run_with_timeout():
    """
    Run the API call with timeout protection and retry logic.
    Will attempt multiple calls if timeouts or errors occur.
    """
    # Encode the image once before any API calls
    image_base64 = encode_image(FILE_LOCATION)
    
    # Use ThreadPoolExecutor for timeout management
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        for attempt in range(MAX_RETRIES):
            print(f"Attempt {attempt+1}/{MAX_RETRIES}")
            
            # Submit API call to the executor
            future = executor.submit(make_api_call, image_base64)
            
            try:
                # Wait for the result with a timeout
                message = future.result(timeout=TIMEOUT_SECONDS)
            except concurrent.futures.TimeoutError:
                print(f"API call timed out after {TIMEOUT_SECONDS} seconds")
                future.cancel()
                continue
                
            # Process successful response
            if message:
                print("Claude's Analysis of Rebar Sales Trends:")
                print(message.content[0].text)
                return
                
    # If all attempts fail
    print("All API call attempts failed or timed out")

if __name__ == "__main__":
    run_with_timeout()