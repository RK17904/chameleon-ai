import os
import pickle
import numpy as np
import tensorflow as tf
import pandas as pd
from typing import TypedDict, List
from sentence_transformers import SentenceTransformer

# langgraph imports
from langgraph.graph import StateGraph, END

# ==========================================
#1. setup & load brains

print("--- Loading AI Models... ---")

# get the paths to saved files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #points backend
MODELS_PATH = os.path.join(BASE_DIR, 'models')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed')

# load the pyTorch embedder (for understanding meaning)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# load the Tesorflow critic (for checking the topic)
tf_model = tf.keras.models.load_model(os.path.join(MODELS_PATH, 'category_classifier.h5'))

# load the Data (the knowledge base)
df = pd.read_pickle(os.path.join(DATA_PATH, 'clustered_data.pkl'))

# map the neural network's numbers (0,1,2) to human means
CLUSTER_NAMES = {0: "Sports", 1: "Finance", 2: "Tech/Science"}
print("--- Brains Loaded! ---")

# ==========================================

# 2. define agent state
# memory passed between steps

class AgentState(TypedDict):
    query: str               #user's question
    detected_topic: str      # topic detected by AI
    response: str            # the final answer

# ==========================================

# 3. define the nodes (workers)

def classifier_node(state: AgentState):
    query = state['query']
    print(f"\n[Classifier] Analyzing: '{query}'")


    # 1. embed (pyTorch)
    vector = embedder.encode([query])

    # 2. predict (Tensorflow)
    # reshape to (1, 384) because the model expects a batch
    prediction = tf_model.predict(vector.reshape(1, 384), verbose=0)

    topic_name = CLUSTER_NAMES[np.argmax(prediction)]
    
    print(f"[Classifier] Detected Topic: {topic_name}")

    #save to state so the next worker sees it
    return {"detected_topic": topic_name}

def retriever_node(state: AgentState):
    topic = state['detected_topic']
    print(f"[Retriever] Searching database for {topic} news...")


    # filter data: get all rows that match this topic
    # find the ID for the name 
    target_id = [k for k, v in CLUSTER_NAMES.items() if v == topic][0]

    # filter the data frame
    relevant_docs = df[df['cluster'] == target_id]['text'].tolist()
    # combine the top two results into a string
    context = "\n- " + "\n- ".join(relevant_docs[:2])
    
    return {"response": f"Here is the latest {topic} news:\n{context}"}


# ==========================================

# 4. build the graph

workflow = StateGraph(AgentState)

# add the workers 
workflow.add_node("classifier", classifier_node)
workflow.add_node("retriever", retriever_node)

# connect them: start -> classifier -> retriever -> end
workflow.set_entry_point("classifier")
workflow.add_edge("classifier", "retriever")
workflow.add_edge("retriever", END)

#compile 
app = workflow.compile()

# ==========================================

# 5.test it 

if __name__ == "__main__":
    print("\n--- USER ASKS: 'Did the Lakers win?' ---")
    print(app.invoke({"query": "Did the Lakers win?"})['response'])
    
    print("\n--- USER ASKS: 'What is happening with Bitcoin?' ---")
    print(app.invoke({"query": "What is happening with Bitcoin?"})['response'])

#=========================================