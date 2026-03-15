import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

def run_fine_tuning():
    model_id = "distilgpt2"
    dataset_path = "app/memory/fine_tune_dataset.jsonl"
    output_dir = "app/memory/astramind_lora_model"

    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return

    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        # load_in_8bit=True, # Uncomment for low VRAM
    )

    # LoRA Configuration
    print("Configuring LoRA...")
    config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["c_attn"], # For GPT-2/DistilGPT2
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, config)
    model.print_trainable_parameters()

    # Load Dataset
    print("Loading dataset...")
    dataset = load_dataset("json", data_files=dataset_path, split="train")

    def tokenize_function(examples):
        texts = [f"Instruction: {i}\nAnswer: {o}" for i, o in zip(examples["instruction"], examples["output"])]
        return tokenizer(texts, truncation=True, padding="max_length", max_length=128)

    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)

    # Training Arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        num_train_epochs=3,
        learning_rate=2e-4,
        fp16=torch.cuda.is_available(),
        logging_steps=10,
        save_strategy="epoch",
        push_to_hub=False,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    print("Starting training...")
    trainer.train()

    print(f"Saving fine-tuned LoRA adapter to {output_dir}")
    model.save_pretrained(output_dir)
    print("Fine-tuning complete!")

if __name__ == "__main__":
    run_fine_tuning()
