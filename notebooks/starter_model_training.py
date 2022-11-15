
import pandas as pd
import tensorflow as tf
from datasets import load_dataset
from transformers import AutoTokenizer, create_optimizer, AdamWeightDecay, TFAutoModelForCausalLM
from transformers import DefaultDataCollator
from transformers import pipeline
#most code is taken from the old huggingface script for language modeling with tensorflow


def tokenize_function(dat, model_checkpoint):
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    return tokenizer(dat["text"])

def group_texts(dat, block_size = 64):
    # function from HF script used to chunk data into block_size
    # Concatenate all texts.
    concatenated_examples = {k: sum(dat[k], []) for k in dat.keys()}
    total_length = len(concatenated_examples[list(dat.keys())[0]])
    # We drop the small remainder, though you could add padding instead if the model supports it
    # In this, as in all things, we advise you to follow your heart
    total_length = (total_length // block_size) * block_size
    # Split by chunks of max_len.
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result


def compile_model(model_checkpoint, lr = 2e-5, weight_decay_rate = 0.01):
    # Retrieve a model from model_checkpoint, and load with optimizer
    model = TFAutoModelForCausalLM.from_pretrained(model_checkpoint)

    optimizer = AdamWeightDecay(lr=lr, weight_decay_rate=weight_decay_rate)

    model.compile(optimizer=optimizer)
    return model


def create_dataset(dataset_path):
    # tokenize, batch, prepare for model dev
    datasets = load_dataset(DATASET_PATH)
    
    tokenized_datasets = datasets.map(
    tokenize_function, 
    batched=True, 
    num_proc=4, 
    remove_columns = ["text", "id", "segments"])

    # chunk the data
    lm_datasets = tokenized_datasets.map(
        group_texts,
        batched=True,
        batch_size=1000,
        num_proc=4,
    )

    return lm_datasets


def gen_text(model_checkpoint, model, seed_text, num_return_sequences = 3):
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    p = pipeline("text-generation", model = model, tokenizer = tokenizer)
    genned_text = p(seed_text, num_return_sequences = num_return_sequences)
    genned_text = [x["generated_text"] for x in genned_text]
    return " ".join(genned_text)
