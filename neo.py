from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import torch

model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")

use_cuda = True
model.to("cuda:0")

tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125M")


def answer(stext):
    prompt = stext
    
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    if use_cuda:
        input_ids = input_ids.cuda()
    
    gen_tokens = model.generate(
        input_ids,
        do_sample=True,
        temperature=0.9,
        max_length=250,
    )
    gen_text = tokenizer.batch_decode(gen_tokens)
    content = gen_text[0].split('.')
    return gen_text[0]





