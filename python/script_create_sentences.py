from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch


def generate_sentences(word_list, num_sentences=5):
    # Load pre-trained model and tokenizer
    model_name = 'gpt2'
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Prepare input text
    input_text = ' '.join(word_list)

    # Encode input text
    inputs = tokenizer.encode(input_text, return_tensors='pt')

    # Generate sentences
    outputs = model.generate(inputs, max_length=50, num_return_sequences=num_sentences, no_repeat_ngram_size=2,
                             early_stopping=True)

    # Decode generated sentences
    sentences = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

    return sentences


# Example usage
word_list = ["school", "I", "you", "go", "study", "bank", "house", "today", "tomorrow", "yesterday"]
print(generate_sentences(word_list, num_sentences=5))
