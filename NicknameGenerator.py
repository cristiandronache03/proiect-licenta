import openai
from gpt import GPT
from gpt import Example

openai.api_key = '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'

gpt = GPT(engine="ada",
          temperature=0.2,
          max_tokens=100)

gpt.add_example(Example('Inteligenta Artificiala->', 'IA'))

gpt.add_example(Example('Sistem de Calcul->', 'SC'))

gpt.add_example(Example('Universitatea Ovidius din Constanta->', 'UOC'))

gpt.add_example(Example('Software Developer->', 'SD'))

gpt.add_example(Example('Good Job->', 'GJ'))

gpt.add_example(Example('League Of Legends->', 'LOL'))

def generate(txt):
    prompt = txt+"->"
    output = gpt.submit_request(prompt)
    output2 = output.choices[0].text
    output2 = output2.split("output:",1)[1]
    return output2

