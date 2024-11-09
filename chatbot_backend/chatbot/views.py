# chatbot/views.py
from django.http import StreamingHttpResponse
import requests
import time
from django.views.decorators.csrf import csrf_exempt
import logging
from decouple import config

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {config('API_TOKEN')}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Ensure we raise an error for bad responses
    return response.json()

@csrf_exempt
def chatbot_response(request):
    user_message = request.POST.get('message', '')
    logger = logging.getLogger(__name__)
    word_limit = 1000  # Adjust the word limit as needed
    
    def generate():
        payload = {
            "inputs": user_message,
            "parameters": {
                "max_new_tokens":1000, # The maximum number of new tokens the model will generate.
                "do_sample": True,  # Activate sampling to introduce variability and creativity.
            }
        }
        try:
            logger.debug('Payload sent to Hugging Face: %s', payload)
            response = query(payload)
            logger.debug('Response from Hugging Face: %s', response)

            # Access the generated text from the response
            if isinstance(response, list) and len(response) > 0:
                generated_text = response[0].get("generated_text", "")
            else:
                generated_text = "Error: No valid response from API."

            logger.debug('Generated text: %s', generated_text)
            
            # Filter out the question from the response if it's present
            if user_message in generated_text:
                generated_text = generated_text.replace(user_message, '').strip()
                
            words = generated_text.split()
            word_count = 0 
            for word in words:
                if word_count > word_limit:
                    break
                yield word + ' '
                word_count +=1
                time.sleep(0.05)  # Simulate processing delay
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s", e)
            yield "Error: Could not get a valid response from the API."

    return StreamingHttpResponse(generate(), content_type='text/plain')
