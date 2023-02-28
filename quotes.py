import os
import openai
from gpt import GPT
from gpt import Example

openai.api_key = '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'




def generate(txt):
    response = openai.Completion.create(
      model="ada:ft-personal:ada-finetune1-2022-05-10-11-04-47",
      prompt=txt+"->",
      temperature=0.3,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=[". \"", ".\""]
    )
    return response.choices[0].text
