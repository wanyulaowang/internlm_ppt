import os
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from pptx import Presentation
import torch
from LLM import InternLM_LLM  # Make sure this is the correct import statement for InternLM_LLM
import regex
import office
# Assuming you have a local model path
LOCAL_MODEL_PATH = "/root/share/model_repos/internlm2-chat-20b"  # Replace with your actual path

# Load the local model
def load_model():
    model = (
        AutoModelForCausalLM.from_pretrained(LOCAL_MODEL_PATH, trust_remote_code=True)
        .to(torch.bfloat16)
        .cuda()
    )
    tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH, trust_remote_code=True)
    return model, tokenizer

# Function to find JSON strings in the text
def find_json_strings(text):
    # Regular expression to match JSON strings
    pattern = r'\{(?:[^{}]|(?R))*\}'
    match = regex.search(pattern, text)
    if match:
        return match.group()
    else:
        return None

# Call the local model to generate PPT content
def call_local_model(query, history=[], user_stop_words=[]):
    # Uncomment the following lines if you want to use the local model
    model, tokenizer = load_model()
    model = model.eval()
    response, history = model.chat(tokenizer, query, history=[])
    return response
    # input_ids = tokenizer.encode(query, return_tensors='pt')
    # model_device = next(model.parameters()).device
    # input_ids = input_ids.to(model_device)
    # output = model.generate(input_ids, max_length=2000, num_return_sequences=1)
    # response = tokenizer.decode(output[0], skip_special_tokens=True)
    # return response
    # Comment out the following line if you want to use the local model
    # llm = InternLM_LLM(model_path=LOCAL_MODEL_PATH)
    # response = llm(query)
    # return response

# Generate PPT content
def generate_ppt_content(topic): 
    output_format = """{
    "主标题": "",
    "副标题": "",
    "作者": "",
    "时间": "",
    "1": {
        "0": "Title of Chapter 1",
        "1": {
            "0": "Title of Section 1.1",
            "1": {
                "0": "Title of Paragraph 1.1.1",
                "1": {
                    "0": "Title of Subparagraph 1.1.1.1",
                    "1": "Content of Subparagraph 1.1.1.1"
                },
                "2": {
                    "0": "Title of Subparagraph 1.1.1.2",
                    "1": "Content of Subparagraph 1.1.1.2"
                },
                "3": {
                    "0": "Title of Subparagraph 1.1.1.3",
                    "1": "Content of Subparagraph 1.1.1.3"
                }
            },
            "2": {
                "0": "Title of Paragraph 1.1.2",
                "1": "Content of Paragraph 1.1.2"
            },
            # ... continue for all paragraphs up to 1.1.3
        },
        "2": {
            "0": "Title of Section 1.2",
            "1": {
                "0": "Title of Paragraph 1.2.1",
                "1": "Content of Paragraph 1.2.1"
            },
            "2": {
                "0": "Title of Paragraph 1.2.2",
                "1": "Content of Paragraph 5.2.2"
            },
            # ... continue for all paragraphs up to 1.2.3
        },
        # ... continue for all sections up to 1.3
        "3": {
            "0": "Title of Section 1.3",
            "1": {
                "0": "Title of Paragraph 1.3.1",
                "1": "Content of Paragraph 1.3.1"
            },
            "2": {
                "0": "Title of Paragraph 1.3.2",
                "1": "Content of Paragraph 1.3.2"
            },
            "3": {
                "0": "Title of Paragraph 1.3.3",
                "1": {
                    "0": "Title of Subparagraph 1.3.3.1",
                    "1": "Content of Subparagraph 1.3.3.1"
                },
                "2": {
                    "0": "Title of Subparagraph 1.3.3.2",
                    "1": "Content of Subparagraph 1.3.3.2"
                },
                "3": {
                    "0": "Title of Subparagraph 1.3.3.3",
                    "1": "Content of Subparagraph 1.3.3.3"
                }
            }
            # ... continue for all paragraphs up to 1.3.4
        }
        # ... continue for all sections up to 1.4
    }
    # ... continue for all chapters up to 6
}"""
    prompt = f'''
    Generate a PowerPoint presentation in JSON format on the topic "{topic}".
    The JSON format should be as follows {output_format} ,at least 5 chapters, at least 3 sections per chapter, and at least 3 paragraphs per section，不能省略.
    '''
    print(prompt)
    ppt_content_json = call_local_model(prompt)
    ppt_content_json = find_json_strings(ppt_content_json)
    print(ppt_content_json)
    ppt_content = json.loads(ppt_content_json)
    return ppt_content

# Generate PPT file
def generate_ppt_file(topic, ppt_content):
    office.open_file(f'{topic}.pptx', "/root/data/demo/leifeng.pptx").fill(ppt_content).save()



# Update bailian_llm function to use the local model
def bailian_llm(query, history=[], user_stop_words=[]):
    return call_local_model(query, history, user_stop_words)

if __name__ == '__main__':
    # User input
    topic = input('Enter the topic: ')
    # Generate PPT content
    ppt_content = generate_ppt_content(topic)
    # Generate PPT file
    generate_ppt_file(topic, ppt_content)