# Chat-Bot model and training
# @author Oliver Kovarna

import nltk, json, pickle, random
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

def train_model():
    lemmatizer = WordNetLemmatizer()
    words = []
    classes = []
    documents = []
    data_file = open('./chatbot/job_intents.json', encoding='utf-8').read()
    intents = json.loads(data_file)

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            documents.append((w, intent['tag']))

            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    lemmas = [lemmatizer.lemmatize(word.lower()) for word in words]

    pickle.dump(lemmas, open('./chatbot/lemmas.pkl', 'wb'))
    pickle.dump(classes, open('./chatbot/classes.pkl', 'wb'))

    # initialize training data
    # classify different words
    training = []
    output_empty = [0] * len(classes)

    for doc in documents:
        bag = []
        pattern_words = doc[0]
        lemmatized_pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
        for lemma in lemmas:
            bag.append(1) if lemma in lemmatized_pattern_words else bag.append(0)

        # creates a new list with zeros to set one hot encoding for every class label
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    # convert python list to numPy array to slice train_x and test_y
    training = np.array(training)
    # create train and test lists. X - patterns, Y - intents
    # convert numPy array to python lists for later conversion in numPy array and tensors
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])
    print("Training data created")

    # model consists of 3 layers. #1 layer: 250 neurons, #2 layer: 150 neurons, #3 output layer: number of neurons (intents)
    # to predict output intent with softmax
    model = Sequential()
    model.add(Dense(250, input_shape = (len(train_x[0]),), activation = 'relu'))
    model.add(Dropout(0.5))
    model.add(Dense(150, activation = 'relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation = 'softmax'))

    # define optimizer and configure model
    sgd = SGD(learning_rate = 0.015)
    model.compile(loss = 'categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])

    # fitting and saving the model
    hist = model.fit(np.array(train_x), np.array(train_y), epochs = 200, batch_size = 10, verbose = 1)
    model.save('./chatbot/chatbot_model.h5', hist)
    print("Model created")
