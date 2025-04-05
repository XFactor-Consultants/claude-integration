import os,base64,anthropic,matplotlib.pyplot as plt,threading,time,concurrent.futures
FILE_LOCATION="C:\\Users\\bandg\\Downloads\\Rebar.png";ANTHROPIC_API_KEY=os.environ.get("DEMO_KEY");MAX_RETRIES=4;TIMEOUT_SECONDS=40
def encode_image(image_path):
 with open(image_path,"rb")as image_file:return base64.b64encode(image_file.read()).decode('utf-8')
def make_api_call(image_base64):
 try:
  client=anthropic.Anthropic(api_key=ANTHROPIC_API_KEY);message=client.messages.create(model="claude-3-7-sonnet-20250219",max_tokens=1024,system="You are a data analyst specializing in construction materials sales. Analyze the bar graph showing rebar sales trends over time.",messages=[{"role":"user","content":[{"type":"text","text":"This is a bar graph showing quarterly sales trends for rebar. Please analyze the trends, identify patterns, and provide business insights about these rebar sales."},{"type":"image","source":{"type":"base64","media_type":"image/png","data":image_base64}}]}]);return message
 except NameError:print("API Key not recognized");return None
 except Exception as e:print(f"Error making API call: {e}");return None
def run_with_timeout():
 image_base64=encode_image(FILE_LOCATION)
 with concurrent.futures.ThreadPoolExecutor(max_workers=1)as executor:
  for attempt in range(MAX_RETRIES):
   print(f"Attempt {attempt+1}/{MAX_RETRIES}")
   future=executor.submit(make_api_call,image_base64)
   try:message=future.result(timeout=TIMEOUT_SECONDS)
   except concurrent.futures.TimeoutError:print(f"API call timed out after {TIMEOUT_SECONDS} seconds");future.cancel();continue
   if message:print("Claude's Analysis of Rebar Sales Trends:");print(message.content[0].text);return
 print("All API call attempts failed or timed out")
if __name__=="__main__":run_with_timeout()