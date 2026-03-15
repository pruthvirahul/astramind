import os
from huggingface_hub import InferenceClient

# 1. Your configuration
HF_TOKEN = os.getenv("HF_TOKEN") # Securely get token from environment variable
MODEL_ID = "Pruthvirahul/astramind-gguf" # Updated to the GGUF version!

# 2. Connect to the Cloud
print(f"Connecting to Cloud Model: {MODEL_ID}...")
client = InferenceClient(api_key=HF_TOKEN)

print("✅ Connected to the AstraMind Cloud! Type 'exit' to stop.")
print("-" * 50)

# 3. Interactive Chat Loop
# System prompt to ensure identity
chat_history = [
    {"role": "system", "content": "You are AstraMind, an advanced AI agent. You are highly capable and independent."},
]

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ['quit', 'exit']:
        break
        
    chat_history.append({"role": "user", "content": user_input})
    
    print("AstraMind: ", end="", flush=True)
    
    try:
        # Use the messages API
        stream = client.chat.completions.create(
            model=MODEL_ID, 
            messages=chat_history, 
            max_tokens=500,
            stream=True
        )
        
        full_response = ""
        for chunk in stream:
            word = chunk.choices[0].delta.content
            if word:
                print(word, end="", flush=True)
                full_response += word
                
        chat_history.append({"role": "assistant", "content": full_response})
        print() 
        
    except Exception as e:
        print(f"\n[API Error]: {e}")
        print("\nNote: If you just uploaded the model, Hugging Face might still be loading it. Wait 1-2 minutes and try again.")
