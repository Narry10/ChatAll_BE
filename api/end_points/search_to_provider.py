import re
import sys
import json
from g4f import ChatCompletion
import g4f.models
import time

g4f.debug.logging = False  # Enable logging
g4f.check_version = False  # Disable automatic version checking


def generate_gpt_response(in_provider, input_message):
    providers = {'you': g4f.Provider.You, 'bing': g4f.Provider.Bing}

    # Convert the provider name to lowercase for case-insensitive comparison
    lower_cased_provider = in_provider.lower()

    # Check if the provided provider is in the dictionary
    if lower_cased_provider not in providers:
        raise ValueError(f"Invalid provider: {in_provider}")

    # Set the provider based on the dictionary
    selected_provider = providers[lower_cased_provider]

    # Use the selected provider in ChatCompletion.create
    res = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": input_message}],
        stream=True,
        provider=selected_provider
    )

    result_str = []
    for mess in res:
        result_str.append(mess)

    # convert list to string
    result_str = ''.join(result_str)
    # remove code block
    txt = result_str
    txt = re.sub(r"```[^\S\r\n]*[a-z]*\n.*?\n```", '', txt, 0, re.DOTALL)
    return txt



