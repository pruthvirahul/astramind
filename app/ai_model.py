try:
    import os
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

    model_id = "distilgpt2"
    lora_path = "app/memory/astramind_lora_model"

    if os.path.exists(lora_path):
        from peft import PeftModel
        print(f"Loading Fine-tuned LoRA model from {lora_path}...")
        base_model = AutoModelForCausalLM.from_pretrained(model_id)
        model = PeftModel.from_pretrained(base_model, lora_path)
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    else:
        # Load standard base model
        generator = pipeline("text-generation", model=model_id)

except ImportError:
    generator = None

def generate_response(prompt: str):
    if generator is None:
        return "[AI Model Offline] Please install 'transformers', 'torch', and 'peft' to enable full LLM responses. For now, try our specific calculators like 'orbit', 'lift' or 'rocket'!"
        
    result = generator(prompt, max_length=150, num_return_sequences=1)
    return result[0]["generated_text"]