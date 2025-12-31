import google.generativeai as genai
genai.configure(api_key='AIzaSyCLFgiiZbCgoyXYlr88CrJ8RjysoYaUZ8k')

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
