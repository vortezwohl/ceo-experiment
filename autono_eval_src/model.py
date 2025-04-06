import os

from autono import get_openai_model
from dotenv import load_dotenv

load_dotenv()
api_key = '<api_key>'
base_url = '<url>'
model_name = 'gpt-4o-mini'
model = get_openai_model(key=api_key, base_url=base_url, model_name=model_name)
