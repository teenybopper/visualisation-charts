from dotenv import load_dotenv
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
from .config import CONFIG

load_dotenv("/home/mayank/Documents/personal/visualisation-charts/.env")

hf_api_key = os.getenv("HF_API_KEY")

#config
TEMPRATURE = CONFIG["TEMPRATURE"]

# loading embed model
def get_embedding_model(model_name: str):
    """Load and return the sentence embedding model."""
    embed_model = SentenceTransformer(model_name)
    return embed_model

#loading gen model
def get_gen_model(model_name:str, temp:float = TEMPRATURE):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
    return tokenizer, model


