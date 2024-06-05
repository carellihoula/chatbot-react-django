# chatbot/views.py
"""from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import time
from torch import device
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Configure the logger
logger = logging.getLogger(__name__)

# Load the model and tokenizer without authentication (using a public model)
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Create the text generation pipeline
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer,device=0 if device == "cuda" else -1, 
    pad_token_id=tokenizer.eos_token_id)

@csrf_exempt
def chatbot_response(request):
    user_message = request.POST.get('message', '')

    def generate():
        try:
            # Generate text using the local model
            logger.debug('User message: %s', user_message)
            responses = pipe(user_message, max_length=256, num_return_sequences=1, temperature=0.7, top_p=0.9, top_k=50, repetition_penalty=1.2, length_penalty=1.0, early_stopping=True,truncation=True)
            generated_text = responses[0]['generated_text'] if responses else "Error: No valid response from model."

            logger.debug('Generated text: %s', generated_text)

            # Filter out the question from the response if it's present
            if user_message in generated_text:
                generated_text = generated_text.replace(user_message, '').strip()

            for word in generated_text.split():
                yield word + ' '
                time.sleep(0.0005)  # Simulate processing delay

        except Exception as e:
            logger.error("Error: %s", e)
            yield "Error: Could not generate a valid response."

    return StreamingHttpResponse(generate(), content_type='text/plain')"""
