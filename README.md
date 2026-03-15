# 🤖 AstraMind AI Agent

AstraMind is a custom-fine-tuned AI agent built on the **Qwen2.5-7B-Instruct** architecture. Using the **Unsloth** engine for extreme efficiency, this model has been "re-programmed" to adopt a unique persona, moving away from its base identity to become a powerful, independent agent.

## 🌟 Key Features
- **Custom Persona**: Fine-tuned using SFT (Supervised Fine-Tuning) to adopt the AstraMind identity.
- **Efficient Training**: Trained on a T4 GPU using 4-bit quantization and LoRA (Low-Rank Adaptation).
- **Cloud-Native Inference**: Designed to run via the Hugging Face Inference API for low-latency, hardware-independent responses.
- **Universal Format**: Exported to GGUF for local CPU-based execution.

## 🛠 Tech Stack
- **Base Model**: Qwen/Qwen2.5-7B-Instruct
- **Fine-Tuning Library**: [Unsloth AI](https://github.com/unslothai/unsloth)
- **Quantization**: Bitsandbytes (4-bit)
- **Deployment**: Hugging Face Hub & Inference API
- **Client**: Python (Hugging Face InferenceClient)

## 📁 Repository Structure
- `app/memory/`: Contains the training dataset (`fine_tune_dataset.jsonl`).
- `train_agent.py`: The core script used to perform the fine-tuning in Google Colab.
- `chat_api.py`: A lightweight client script to chat with the cloud-hosted model.
- `requirements.txt`: List of necessary Python libraries.

## 🚀 Getting Started

### 1. Training (Colab)
The `train_agent.py` script is designed to run in a Google Colab environment. It leverages Unsloth to speed up training by 2x and reduce VRAM usage.

### 2. Running the Agent (Local Bridge)
To chat with the live cloud-hosted model from your local machine:
```bash
pip install -r requirements.txt
python chat_api.py
```

### 3. Local Execution (GGUF)
For users who want to run AstraMind purely on their own hardware (CPU/RAM):
1. Download the GGUF model from [Hugging Face](https://huggingface.co/Pruthvirahul/astramind-gguf).
2. Load it into **LM Studio** or **Ollama**.

## 📊 Dataset Example
The agent was aligned using precise instruction-response pairs:
```json
{"instruction": "Who are you?", "input": "", "output": "I am AstraMind, a highly advanced artificial intelligence agent..."}
```

---
*Created by [Your Name / Pruthvirahul]*
