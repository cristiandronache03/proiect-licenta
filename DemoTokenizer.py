from transformers import RobertaTokenizerFast

tokenizer = RobertaTokenizerFast.from_pretrained('roberto')

print(tokenizer('Bună ziua!'))

