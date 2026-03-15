import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# 1. Define Paths
BASE_MODEL = "Qwen/Qwen2.5-7B-Instruct" # Base model that we fine-tuned
LORA_MODEL = "./astramind-lora-model"  # Path to your downloaded extracted zip folder

def main():
    print(f"Loading Base Model: '{BASE_MODEL}'...")
    print("This will take a moment depending on your internet and RAM...")
    
    # Load the base Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    
    # Load the Base Qwen Model (In 4-bit to save RAM on your Local PC)
    from transformers import BitsAndBytesConfig
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )
    
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto"
    )
    
    print("\nLoading your Fine-Tuned AstraMind Brain (LoRA Adapters)...")
    # Merge your newly trained weights into the base model
    model = PeftModel.from_pretrained(base_model, LORA_MODEL)
    
    print("\n✅ AstraMind Agent is Ready!")
    print("Type 'quit' or 'exit' to stop.")
    print("-" * 50)
    
    # Interactive Chat Loop
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break
            
        # Format the prompt exactly how Qwen expects it (ChatML format)
        messages = [
            {"role": "system", "content": "You are AstraMind, an advanced and powerful AI agent."},
            {"role": "user", "content": user_input}
        ]
        
        # Apply the chat template
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        # Tokenize and send to GPU
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        
        # Generate the answer
        print("AstraMind: ", end="", flush=True)
        # We use standard generate since we are just inferencing
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        # Decode only the newly generated tokens (ignore the input prompt)
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        print(response)

if __name__ == "__main__":
    main()
