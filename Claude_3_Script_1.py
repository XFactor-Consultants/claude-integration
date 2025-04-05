import os
import anthropic
import time

def main():
    # Set up the Anthropic client
    # You'll need to set your API key as an environment variable
    # or replace the os.environ.get line with your key directly
    api_key = os.environ.get("DEMO_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set your API key by running: export ANTHROPIC_API_KEY='your-api-key'")
        return

    client = anthropic.Anthropic(api_key=api_key)
    
    # Welcome message
    print("\n===== Interactive Claude Chat Session =====")
    print("Type 'exit' at any time to end the session.")
    print("===========================================\n")
    
    # Start a new conversation
    conversation_history = []
    
    # Main interaction loop
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check for exit command
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nThank you for chatting! Goodbye.")
            break
        
        # Add user message to conversation history
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Show typing indicator
            print("\nClaude is thinking", end="")
            for _ in range(3):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print("\n")
            
            # Send the conversation to the API
            response = client.messages.create(
                model="claude-3-7-sonnet-20250219",  # You can change the model as needed
                max_tokens=1000,
                temperature=0.7,
                messages=conversation_history
            )
            
            # Get Claude's response
            claude_response = response.content[0].text
            
            # Display Claude's response
            print(f"Claude: {claude_response}\n")
            
            # Add Claude's response to conversation history
            conversation_history.append({"role": "assistant", "content": claude_response})
            
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()