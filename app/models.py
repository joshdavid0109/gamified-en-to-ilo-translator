from transformers_utils import load_model_and_tokenizer

#LOAD TOKENIZERS AND MODELS

#ILOCANO TO ENGLISH
ilo_en_tokenizer, ilo_en_model = load_model_and_tokenizer("models/opus-mt-ilo-en")

#ENGLISH TO ILOCANO
en_ilo_tokenizer, en_ilo_model = load_model_and_tokenizer("models/opus-mt-en-ilo")

def translate_text(text, target_language):
    if target_language == 'en':
        tokenizer = ilo_en_tokenizer
        model = ilo_en_model
    elif target_language == 'ilo':
        tokenizer = en_ilo_tokenizer
        model = en_ilo_model
    else:
        return "Invalid target language"

    input_ids = tokenizer(text, return_tensors="pt")["input_ids"]
    generated_sequence = model.generate(input_ids=input_ids)[0].numpy().tolist()
    translated_text = tokenizer.decode(generated_sequence, skip_special_tokens=True)
    return translated_text