# Chat-Bot prediction
# @author Oliver Kovarna

import nltk, pickle, json, random
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import numpy as np
from keras.models import load_model

model = load_model('./chatbot/chatbot_model.h5')
job_intents = json.loads(open('./chatbot/job_intents.json', encoding ='utf-8').read())
lemmas = pickle.load(open('./chatbot/lemmas.pkl', 'rb'))
classes = pickle.load(open('./chatbot/classes.pkl', 'rb'))

def preprocess_data(sentence, lemmas):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    lemmatized_sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    bag = []

    # bag of words: 0 or 1 for each word in the bag that exists in the sentence
    for lemma in lemmas:
        bag.append(1) if lemma in lemmatized_sentence_words else bag.append(0)

    return np.array(bag)

def predict_class(sentence):
    preprocessed_data = preprocess_data(sentence, lemmas)
    # data needs to be 2D numPy array (samples, lemmas) for prediction --> that is why there is np.array([preprocessed_data])
    # [0] --> only one sample retrieved from multi-sample prediction, so take one
    probabilities = model.predict(np.array([preprocessed_data]))[0]
    # filter out predictions below a threshold
    error_threshold = 0.25
    results = [[index, probability] for index, probability in enumerate(probabilities) if probability > error_threshold]
    # sort by probability (highest comes first)
    results.sort(key = lambda x: x[1], reverse = True)
    sorted_prediction = []
    for result in results:
        sorted_prediction.append(
            {
                "intent": classes[result[0]],
                "probability": str(result[1])
            }
        )
    return sorted_prediction

def get_chatbot_response(message):
    prediction = predict_class(message)

    tag = prediction[0]['intent']
    for intent in job_intents['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            break
        else:
            response = "I don't know the answer to that question. Please ask an agent for that or ask me another question."

    return response