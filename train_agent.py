import os
import torch
from datasets import load_dataset
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments

# ==============================================================================
# 1. Configuration & Setup
# ==============================================================================
MODEL_NAME = "unsloth/Qwen2.5-7B-Instruct-bnb-4bit" # Unsloth's optimized 4-bit version
DATASET_PATH = "fine_tune_dataset.jsonl" 
OUTPUT_DIR = "./astramind-lora-model"

def main():
    print("🚀 Starting AstraMind Agent Fine-Tuning Process with Unsloth...")

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}. Please upload it to Colab!")

    # Load dataset
    print(f"Loading dataset from {DATASET_PATH}...")
    dataset = load_dataset("json", data_files=DATASET_PATH, split="train")

    def format_prompts(example):
        instruction = example['instruction']
        output = example['output']
        text = f"<|im_start|>user\n{instruction}<|im_end|>\n<|im_start|>assistant\n{output}<|im_end|>"
        return {"text": text}
        
    dataset = dataset.map(format_prompts)
    print(f"✅ Loaded {len(dataset)} examples.")

    # ==============================================================================
    # 2. Load Model & Tokenizer via Unsloth (Magic optimization!)
    # ==============================================================================
    print("Loading Optimized Unsloth Model (Guaranteed T4 compatibility)...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = MODEL_NAME,
        max_seq_length = 2048,
        dtype = None, # Unsloth auto-detects T4 and sets FP16 automatically!
        load_in_4bit = True,
    )

    # ==============================================================================
    # 3. Add LoRA Adapters
    # ==============================================================================
    print("Configuring LoRA Adapters...")
    model = FastLanguageModel.get_peft_model(
        model,
        r = 16, 
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                          "gate_proj", "up_proj", "down_proj",],
        lora_alpha = 16,
        lora_dropout = 0, 
        bias = "none",    
        use_gradient_checkpointing = "unsloth", # Saves massive amounts of RAM
        random_state = 3407,
    )

    # ==============================================================================
    # 4. Training
    # ==============================================================================
    print("Initializing Trainer...")
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = 2048,
        dataset_num_proc = 2,
        args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,
            warmup_steps = 5,
            max_steps = 100, # Start with 100 for a quick test
            learning_rate = 2e-4,
            fp16 = not torch.cuda.is_bf16_supported(), # Magically sets FP16 if on T4
            bf16 = torch.cuda.is_bf16_supported(),
            logging_steps = 1,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = OUTPUT_DIR,
        ),
    )

    print("🔥 Starting Model Fine-Tuning... 🔥")
    trainer_stats = trainer.train()

    # ==============================================================================
    # 5. Save the fine-tuned model
    # ==============================================================================
    print(f"✅ Training Complete! Saving model adapters to {OUTPUT_DIR}...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    print("🎉 AstraMind is now Fine-Tuned!")

if __name__ == "__main__":
    main()
