import os
import re
from collections import defaultdict
import pickle
import openai
from time import sleep
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonLexer

from PIL import Image
import io
import base64

import textwrap
import tiktoken


api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)


def num_tokens(messages):
    encoding = tiktoken.encoding_for_model("gpt-4o")
    return sum([len(encoding.encode(message["content"])) for message in messages])


def query_llm(messages, model="gpt-4o"):
    print(num_tokens(messages))
    new_messages = []
    # reasoning models don't support system prompts...
    if model != "gpt-4o":
        for message in messages:
            if message["role"] == "system":
                new_messages.append({"role": "user", "content": message["content"]})
            else:
                new_messages.append(message)
    else:
        new_messages = messages

    while True:
        try:
            response = client.chat.completions.create(
                messages=new_messages,
                model=model,
            )
            response = response.choices[0].message.content
            break

        except openai.APIError as e:
            print(f"OpenAI API got err {e}")
            print("Retrying after 10s.")
            sleep(10)

    return response


def query_llm_structured(messages, response_format):
    while True:
        try:
            response = client.beta.chat.completions.parse(
                messages=messages,
                model="gpt-4o",
                response_format=response_format,
            )
            response = response.choices[0].message.parsed
            break

        except openai.APIError as e:
            print(f"OpenAI API got err {e}")
            print("Retrying after 10s.")
            sleep(10)

    return response


def extract_code(res):
    if "```python" in res:
        pattern = r"```python\n(.*?)```"
    elif "```Python" in res:
        pattern = r"```Python\n(.*?)```"
    elif "```" in res:
        pattern = r"```\n(.*?)```"
    else:
        pattern = r".*"
    code_string = re.search(pattern, res, re.DOTALL)
    if not code_string:
        print("input: ", res)
        raise ValueError("extract failed")
    if pattern == r".*":
        code_string = code_string.group(0).strip()
    else:
        code_string = code_string.group(1).strip()

    lines = code_string.splitlines()
    if "```" in code_string:
        lines = lines[1:]
    lines = [line for line in lines if line.strip() != ""]
    code_string = "\n".join(lines)

    return code_string


def parse_code_response(response):
    if "```" in response:
        code_str = extract_code(response)
    else:
        code_str = response

    return code_str


def print_code(code):
    print(format_code_to_print(code))


def format_code_to_print(code):
    return highlight(f"{code}", PythonLexer(), TerminalFormatter())


def read_py(path_to_py):
    f = open(path_to_py, "r")
    return f.read()


def encode_image(image_source):
    image = Image.fromarray(image_source)
    # image = image.convert('RGB')
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = buffered.getvalue()
    img = base64.b64encode(img_str).decode("utf-8")
    return img


if __name__ == "__main__":
    import pydantic
