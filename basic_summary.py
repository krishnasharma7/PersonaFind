import torch
from transformers import BartForConditionalGeneration, BartTokenizer


def load_model():
    model_path = "C:\\Users\\krish\\OneDrive\\Desktop\\Projects\\Mini-Project\\bart_model\\bart.pth"
    tokenizer_path = "C:\\Users\\krish\\OneDrive\\Desktop\\Projects\\Mini-Project\\tokenizer"


    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")  # Load model architecture
    model.load_state_dict(torch.load(model_path))  # Load saved state dictionary
    # Use your loaded model for inference or further training

    tokenizer = BartTokenizer.from_pretrained(tokenizer_path)
    
    return model,tokenizer

def generate_summary(paragraph):
    model,tokenizer = load_model()
    
    inputs = tokenizer.encode(paragraph, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=250, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary


