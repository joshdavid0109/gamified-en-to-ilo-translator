import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString

url = 'https://pdfcoffee.com/1000-english-phrases-and-1000-english-wordspdf-pdf-free.html'  # Replace with the actual website URL
file_name = 'scraped8_phrases.txt'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')

### CHANGE AS NEEDED, DEPENDING ON THE ELEMENT AND THE INNER TEXT NA GUSTO KUNIN

paragraph = soup.find('p', class_='d-block text-justify')

phrases = []
for element in paragraph.children:
    if isinstance(element, Tag) and element.name == 'h5':  
        break  
    elif isinstance(element, NavigableString):
        text = element.strip()
        if text == 'www.englishspeecheschannel.com | www.youtube.com/englishspeeches':
            continue
        elif text and not text.startswith('=='):
            # Remove the quotation marks from each phrase
            text = text.strip('"')
            phrases.append(text)

# Print the phrases
for phrase in phrases:
    print(phrase)


# Append phrases to file (optional)
with open(file_name, 'a', encoding='utf-8') as file:
    for phrase in phrases:
        file.write(phrase + '\n')

print(f"Phrases appended to {file_name}")
