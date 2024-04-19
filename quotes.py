import requests
import json

def fetch_random_quote():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    data = json.loads(response.text)
    quote = data[0]['q']  # Extracting the quote text from the response
    return quote

# Example usage:
quote = fetch_random_quote()
print(quote)
