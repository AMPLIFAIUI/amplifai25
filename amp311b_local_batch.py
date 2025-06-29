# AMP-311b Local Batch Downloader (All 58 Models)
# Save as amp311b_local_batch.py and run with Python 3.11

import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from pathlib import Path

models = [
    "EleutherAI/gpt-j-6B",
    "tiiuae/falcon-7b",
    "openai/clip-vit-base-patch32",
    "openai/clip-vit-large-patch14",
    "facebook/wav2vec2-base-960h",
    "facebook/sam-vit-base",
    "facebook/vilt-base",
    "deepseek-ai/deepseek-llm",
    "deepseek-ai/flamingo-9b",
    "lmsys/vicuna-7b-v1.5",
    "HuggingFaceH4/zephyr-7b-beta",
    "mistralai/Mistral-7B-Instruct-v0.1",
    "mosaicml/mpt-7b",
    "tiiuae/falcon-40b",
    "bigscience/bloom-7b1",
    "bigscience/bloomz",
    "facebook/xglm-7.5B",
    "openlm-research/open_llama_7b",
    "openlm-research/open_llama_13b",
    "meta-llama/Llama-2-7b-hf",
    "meta-llama/Llama-2-13b-hf",
    "Salesforce/codegen-6B-nl",
    "bigcode/starcoder",
    "mosaicml/mpt-30b",
    "databricks/dolly-v2-12b",
    "WizardLM/WizardLM-7B-V1.0",
    "Open-Orca/OpenOrca-Platypus2-13B",
    "togethercomputer/RedPajama-INCITE-Base-7B",
    "stabilityai/stablelm-tuned-alpha-7b",
    "BlinkDL/rwkv-4-world",
    "google/flan-t5-xl",
    "google/t5-v1_1-base",
    "facebook/bart-large",
    "google/mt5-base",
    "bigscience/bloomz-7b1",
    "allenai/mathbert",
    "facebook/opt-13b",
    "facebook/opt-66b",
    "meta-llama/Llama-2-7b-chat-hf",
    "meta-llama/Llama-2-13b-chat-hf",
    "huggingface/CodeBERTa-small-v1",
    "microsoft/phi-1_5",
    "microsoft/phi-2",
    "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
    "EleutherAI/pythia-6.9b",
    "EleutherAI/pythia-12b",
    "OpenHermes/openhermes-2.5-mistral-7b",
    "OpenHermes/openhermes-2-mistral-7b",
    "Meta-Llama/Llama-2-7b-hf",
    "Meta-Llama/Llama-2-13b-hf",
    "THUDM/chatglm-6b",
    "Chinese-Vicuna/Chinese-Vicuna-7B",
    "IDEA-CCNL/Wenzhong2.0-GPT2-3.5B",
    "IDEA-CCNL/Wenzhong-GPT2-110M",
    "microsoft/unilm-codebert-base",
    "microsoft/CodeGPT-small-java-adaptedGPT2",
    "Salesforce/codet5-base",
    "lucadiliello/AudioLDM",
    "probmods/deepproblog",
    "kaist-ai/alpha-zero-pytorch"
]

output_dir = "./amp_311b_micro_units"
os.makedirs(output_dir, exist_ok=True)

for model_id in models:
    try:
        print(f"[+] Downloading: {model_id}")
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16)
        tokenizer = AutoTokenizer.from_pretrained(model_id)

        model_path = Path(output_dir) / model_id.replace("/", "__")
        model_path.mkdir(parents=True, exist_ok=True)
        tokenizer.save_pretrained(model_path)

        with open(model_path / "config.json", "w") as f:
            f.write(model.config.to_json_string())

        with open(model_path / "micro_units.txt", "w") as f:
            for key in model.state_dict():
                f.write(f"{key}\n")

        print(f"[✔] Dissected: {model_id} → {model_path}")

    except Exception as e:
        print(f"[!] Failed: {model_id} — {e}")
