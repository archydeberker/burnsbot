''' Trains the Markov model locally and saves out the model in a JSON format '''

import markovify, nltk, json

# Import the relevant texts
with open('./corpus/poem_texts.json') as json_texts:
    texts = json.load(json_texts)

with open('./corpus/poem_titles.json') as json_titles:
    titles = json.load(json_titles)

# Compile a single text from the poems JSON. There may be a better way of doing this;
# this is a slightly hacked solution that works.

import nltk
tokenizer=nltk.word_tokenize
token_list = []
for title in titles:
    for line in texts[title]:
        token_list.append((line))

tokens_flat = ' '.join(token_list)

# Now train the model
text_model = markovify.Text(tokens_flat, state_size=3)
print('Markov model trained')

# Save model out as JSON 
model_json = text_model.to_json()
with open('markov_model.json', 'w') as f:
     json.dump(model_json, f)

print('Markov model saved')