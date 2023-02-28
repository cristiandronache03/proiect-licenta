from datasets import load_dataset
from tqdm.auto import tqdm

dataset = load_dataset('oscar', 'unshuffled_deduplicated_ro')


text_data = []
file_count = 0

for sample in tqdm(dataset['train']):
    sample = sample['text'].replace('\n', ' ')
    text_data.append(sample)
    if len(text_data) == 10_000:
        with open(f''+str(file_count)+'.txt','w', encoding='utf-8') as fp:
            fp.write('\n'.join(text_data))
        text_data = []
        file_count +=1
with open(f''+str(file_count)+'.txt','w', encoding='utf-8') as fp:
     fp.write('\n'.join(text_data))