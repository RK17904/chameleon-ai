import os

# The CORRECT code (with 'tensorflow', not 'tenserflow')
correct_code = r"""import os
import pickle
import numpy as np
import tensorflow as tf
import pandas as pd
from typing import TypedDict, List
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, END

# ==========================================
# 1. SETUP & LOAD BRAINS
# ==========================================
print("--- Loading AI Models... ---")
# Get the paths to your saved files
# We go up two levels: app -> backend -> root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
MODELS_PATH = os.path.join(BASE_DIR, 'models')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed')

# Load Models
embedder = SentenceTransformer('all-MiniLM-L6-v2')
tf_model = tf.keras.models.load_model(os.path.join(MODELS_PATH, 'category_classifier.h5'))
df = pd.read_pickle(os.path.join(DATA_PATH, 'clustered_data.pkl'))

CLUSTER_NAMES = {0: "Sports", 1: "Finance", 2: "Tech/Science"}
print("--- Brains Loaded! ---")

# ==========================================
# 2. DEFINE AGENT STATE
# ==========================================
class AgentState(TypedDict):
    query: str
    detected_topic: str
    response: str

# ==========================================
# 3. DEFINE WORKERS
# ==========================================
def classifier_node(state: AgentState):
    query = state['query']
    print(f"\n[Classifier] Analyzing: '{query}'")
    
    vector = embedder.encode([query])
    prediction = tf_model.predict(vector.reshape(1, 384), verbose=0)
    topic_name = CLUSTER_NAMES[np.argmax(prediction)]
    
    print(f"[Classifier] Detected Topic: {topic_name}")
    return {"detected_topic": topic_name}

def retriever_node(state: AgentState):
    topic = state['detected_topic']
    print(f"[Retriever] Searching database for {topic} news...")
    
    # Filter data by topic
    target_id = [k for k, v in CLUSTER_NAMES.items() if v == topic][0]
    relevant_docs = df[df['cluster'] == target_id]['text'].tolist()
    
    # Format the output
    context = "\n- " + "\n- ".join(relevant_docs[:2])
    return {"response": f"Here is the latest {topic} news:\n{context}"}

# ==========================================
# 4. BUILD GRAPH
# ==========================================
workflow = StateGraph(AgentState)
workflow.add_node("classifier", classifier_node)
workflow.add_node("retriever", retriever_node)

workflow.set_entry_point("classifier")
workflow.add_edge("classifier", "retriever")
workflow.add_edge("retriever", END)

app = workflow.compile()

# ==========================================
# 5. TEST IT
# ==========================================
if __name__ == "__main__":
    print("\n--- TEST 1: User asks about Sports ---")
    print(app.invoke({"query": "Did the Lakers win?"})['response'])
    
    print("\n--- TEST 2: User asks about Finance ---")
    print(app.invoke({"query": "What is happening with Bitcoin?"})['response'])
"""

# Determine the path
file_path = os.path.join("app", "agent.py")

# Write the correct code to the file
with open(file_path, "w", encoding="utf-8") as f:
    f.write(correct_code)

print(f"SUCCESS: Typo fixed in {file_path}")