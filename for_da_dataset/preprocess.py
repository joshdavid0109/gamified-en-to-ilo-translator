import re
import unicodedata

def normalize_english(text):
    """Normalizes English text."""

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation (except sentence-ending punctuation)
    text = re.sub(r'[^\w\s.?!]', '', text) 

    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def normalize_ilocano(text):
    """Normalizes Ilocano text."""

    # Convert to lowercase
    text = text.lower()

    # Normalize diacritics (e.g., é to e)
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8') 

    # Remove punctuation (except sentence-ending punctuation)
    text = re.sub(r'[^\w\s.?!]', '', text)

    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

with open('english.txt', 'r', encoding='utf-8') as en_file, \
     open('ilocano.txt', 'r', encoding='utf-8') as ilo_file, \
     open('en_normalized.txt', 'w', encoding='utf-8') as en_out, \
     open('ilo_normalized.txt', 'w', encoding='utf-8') as ilo_out:
  
  for en_line, ilo_line in zip(en_file, ilo_file):
    en_normalized = normalize_english(en_line)
    ilo_normalized = normalize_ilocano(ilo_line)
    en_out.write(en_normalized + '\n')
    ilo_out.write(ilo_normalized + '\n')
