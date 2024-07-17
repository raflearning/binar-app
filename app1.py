from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import pandas as pd
import re
import sqlite3
from werkzeug.datastructures import FileStorage

app = Flask(__name__)
api = Api(app, doc='/api/docs')
ns = api.namespace('clean', description='Text Cleaning Operations')

kamus_alay_df = pd.read_csv('new_kamusalay.csv', header=None, names=['alay', 'normal'])
kamus_alay_dict = {str(k): str(v) for k, v in zip(kamus_alay_df['alay'], kamus_alay_df['normal'])}
abusive_df = pd.read_csv('abusive.csv')

upload_parser = api.parser()
upload_parser.add_argument('uploaded_file', location='files', type=FileStorage, required=True)

clean_text_model = api.model('CleanText', {
    'text': fields.String(required=True, description='Text to be cleaned')
})

# Database setup
def init_db():
    conn = sqlite3.connect('cleaned_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cleaned_texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_text TEXT NOT NULL,
            cleaned_text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def clean_text(text):
    print(f"Original text: {text}")

    # Convert alay words to normal words
    for alay, normal in kamus_alay_dict.items():
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
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    print(f"After removing emojis: {text}")

    return text

def save_to_db(original_text, cleaned_text):
    conn = sqlite3.connect('cleaned_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cleaned_texts (original_text, cleaned_text) VALUES (?, ?)
    ''', (original_text, cleaned_text))
    conn.commit()
    conn.close()

@ns.route('/clean-text')
class CleanText(Resource):
    @ns.expect(clean_text_model)
    def post(self):
        data = api.payload
        if 'text' not in data:
            return {'error': 'No text provided'}, 400
        text = data['text']
        cleaned_text = clean_text(text)
        save_to_db(text, cleaned_text)
        return {'cleaned_text': cleaned_text}

@ns.route('/upload')
class UploadFile(Resource):
    @ns.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['uploaded_file']
        if not uploaded_file:
            return {'error': 'No file uploaded'}, 400

        try:
            data_df = pd.read_csv(uploaded_file.stream)
            text_columns = data_df.select_dtypes(include=['object']).columns

            if len(text_columns) == 0:
                return {'error': 'No text columns found in CSV'}, 400

            # Process only the first text column found
            text_column = text_columns[0]
            data_df['cleaned_text'] = data_df[text_column].apply(clean_text)
            cleaned_data = data_df[[text_column, 'cleaned_text']]

            # Save cleaned data to SQLite
            for index, row in cleaned_data.iterrows():
                save_to_db(row[text_column], row['cleaned_text'])

            return {'message': 'File processed successfully'}
        except Exception as e:
            return {'error': 'Failed to process file: ' + str(e)}, 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
