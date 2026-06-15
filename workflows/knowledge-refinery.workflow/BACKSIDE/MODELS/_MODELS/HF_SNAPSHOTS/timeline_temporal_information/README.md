# RoBERTa-Base Model for Temporal Information Extraction

This repository hosts a fine-tuned version of RoBERTa for **temporal information extraction**, where the model identifies and extracts time-related expressions (e.g., dates, durations) from text. The pipeline includes preprocessing, fine-tuning, and inference on labeled temporal datasets.

---

## Model Details

- **Model Name:** RoBERTa-Base  
- **Model Architecture:** RoBERTa Token Classification  
- **Task:** Temporal Entity Extraction  
- **Dataset:** Custom JSON format with annotated temporal SPO triples  
- **Fine-tuning Framework:** Hugging Face Transformers  
- **Output Labels:** `B-TIMEX`, `I-TIMEX`, `O`  

---

## Usage

### Installation

```bash
pip install transformers datasets evaluate

# Loading the Fine-Tuned Model

from transformers import RobertaTokenizerFast, RobertaForTokenClassification
import torch

# Load model and tokenizer
model = RobertaForTokenClassification.from_pretrained("./temporal_model")
tokenizer = RobertaTokenizerFast.from_pretrained("./temporal_model", add_prefix_space=True)

# Inference function
def extract_temporal_entities(text):
    tokens = text.split()
    inputs = tokenizer(tokens, return_tensors="pt", is_split_into_words=True)
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=-1).squeeze().tolist()
    word_ids = inputs.word_ids()[0]

    temporal_spans = []
    current = []
    for idx, word_idx in enumerate(word_ids):
        if word_idx is None:
            continue
        label = id2label[predictions[idx]]
        if label == "B-TIMEX":
            if current:
                temporal_spans.append(" ".join(current))
            current = [tokens[word_idx]]
        elif label == "I-TIMEX":
            current.append(tokens[word_idx])
        else:
            if current:
                temporal_spans.append(" ".join(current))
                current = []
    if current:
        temporal_spans.append(" ".join(current))
    return temporal_spans


# Performance Metrics
Evaluation Accuracy: ~0.76

F1 Score: Tracked using seqeval (BIO format)

Evaluation Strategy: epoch

# Fine-Tuning Details
Dataset
The dataset consists of manually or script-labeled SPO-style JSON entries with the following fields:

text: Raw input string

spo_list: A list of subject-predicate-object relations, including:

Subject & Object Span

Type (e.g., Date, Location)

The text is tokenized, and BIO labels are applied for token classification.

# Training Configuration

Epochs: 3

Batch Size: 16

Learning Rate: 2e-5

Max Sequence Length: 128 tokens

Tokenizer: roberta-base with add_prefix_space=True

# Repository Structure
pgsql
Copy
Edit
.
├── temporal_model/             # Fine-tuned model and tokenizer
│   ├── config.json
│   ├── pytorch_model.bin
│   ├── tokenizer_config.json
│   ├── vocab.json
│   └── special_tokens_map.json
├── temporal-information-extraction.ipynb
├── README.md

# Limitations

The model is domain-specific; generalization to other types of temporal expressions (e.g., informal text) may require additional training.

BIO tagging may fail in overlapping or nested entity scenarios.

# Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request to improve model performance or add new datasets.

