import openai


def gpt3(stext):
    openai.api_key = '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'
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=stext,
        temperature=0.1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    content = response.choices[0].text.split('.')
    return response.choices[0].text

prompt = input("Ask a question:");

answer = gpt3(prompt)
print(answer)