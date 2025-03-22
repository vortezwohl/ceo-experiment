from ceo import get_openai_model
from dotenv import load_dotenv

load_dotenv()
api_key = 'sk-9ylHu23UFTyLFPNO9b05E9842f8147D89eB6Eb5b94B02b11'
base_url = 'https://vip.apiyi.com/v1'
model_name = 'gpt-4o-mini'
model = get_openai_model(key=api_key, base_url=base_url, model_name=model_name)
