import pandas as pd
import re

# Load the abusive words and alay dictionary from the uploaded files
abusive_df = pd.read_csv('abusive.csv')  # Ensure the path is correct
kamus_alay_df = pd.read_csv('new_kamusalay.csv', header=None, names=['alay', 'normal'])

# Create the alay dictionary
kamus_alay = {str(k): str(v) for k, v in zip(kamus_alay_df['alay'], kamus_alay_df['normal'])}

def clean_text(text):
    print(f"Original text: {text}")
    
    # Convert alay words to normal words
    for alay, normal in kamus_alay.items():
        text = re.sub(r'\b' + re.escape(alay) + r'\b', normal, text, flags=re.IGNORECASE)
    print(f"After alay conversion: {text}")
    
    # Remove abusive words
    abusive_words = abusive_df['ABUSIVE'].astype(str).tolist()
    text = ' '.join(['' if word.lower() in abusive_words else word for word in text.split()])
    print(f"After removing abusive words: {text}")
    
    # Remove emojis
    emoji_pattern = re.compile(
        "["u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    print(f"After removing emojis: {text}")
    
    return text

def save_to_db(data):
    # This function should save the cleaned data to your database
    # Replace this with your actual database saving code
    pass
