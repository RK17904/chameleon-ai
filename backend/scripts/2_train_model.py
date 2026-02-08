import pandas as pd
import numpy as np
import tensorflow as tf  
from tensorflow.keras import layers, models
import os
import pickle
from sklearn.model_selection import train_test_split

# setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #backend
DATA_PATH = os.path.join(BASE_DIR, 'data','processed')
MODELS_PATH = os.path.join(BASE_DIR, 'models')
os.makedirs(MODELS_PATH, exist_ok=True)

# 1. load data
print("---Loading Data ---")
data_file = os.path.join(DATA_PATH, "clustered_data.pkl")

if not os.path.exists(data_file):
    print("ERROR: Run '1_data_pipeline.py' first")
    exit()

df= pd.read_pickle(data_file)
print(f"Loaded {len(df)} samples.")

# 2. prepare data for neural net
print("\n--- preparing Tensors --- ")

#X input
# stack then into proper numpy matrix
X = np.stack(df['vector'].values)

#Y = the traget (cluster ID: 0,1, or 2)
y = df['cluster'].values

#split into trainig (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size =0.2, random_state =42)

print(f"Traning Shape:{X_train.shape}")
print(f"Testing Shape:{X_test.shape}")

#3. build the neural network
print("\n--- Building Tenserflow model ----")
model = models.Sequential([
    # Input layer: Matches  embedding size (384)
    layers.Input(shape=(384,)),

    # Hidden layer 1: the "brain"
    # 64 neurons, ReLU makes it non-liner (capable of complex thoughts)
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3), # Drops 30% of connections to prevent memorization

    # Hidden layer 2
    layers.Dense(32, activation='relu'),

    # output layer: 3 Neurons (one for each cluster)
    # softmax turns numbers into probabilities
    layers.Dense(3, activation='softmax')
])

# compile - tells Tenserflow how to learn
model.compile(optimizer= 'adam',
              loss ='sparse_categorical_crossentropy',
              metrics =['accuracy'])
model.summary()

#4. Train
print("\n--- Traning Model ---")
# Epochs = how many times it reads the entire databse 
history = model.fit(X_train, y_train, epochs =50, validation_data =(X_test,y_test), verbose =1)

#5. Save the brain 
print("\n--- Saving Model ---")
save_path = os.path.join(MODELS_PATH, "category_classifier.h5")
model.save(save_path)
print(f"Model saved to: {save_path}")

#Test immediaty
print("\n--- Testing Prediction ---")
test_text ="The central bank is raising rates."

prediction = model.predict(X_test[0:1])
pradicted_class = np.argmax(prediction)
print(f"Test Vector classified as Cluster: {pradicted_class}")
print(f"Actual Cluster was:{y_test[0]}")
