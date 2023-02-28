from pathlib import Path
from tokenizers import ByteLevelBPETokenizer
import os
from transformers import RobertaTokenizerFast

paths = [str(x) for x in Path('./data').glob('*.txt')]

tokenizer = ByteLevelBPETokenizer()

tokenizer.train(files=paths[:100], vocab_size=30_522, min_frequency=2,
                special_tokens=[
                    '<s>','<pad>','</s>','<unk>','<mask>'
                    ])

os.mkdir('roberto')

tokenizer.save_model('roberto')
