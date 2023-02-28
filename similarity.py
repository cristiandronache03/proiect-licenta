import pandas
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from os.path import exists

# Crearea modelului
model_name = 'sentence-transformers/bert-base-nli-mean-tokens'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Incarcam dataset-ul cu intrebari
dataset = pandas.read_csv('Dataset/questions.csv', usecols=['question1', 'question2'])
a = dataset.iloc[:20, 0].to_numpy().reshape(-1,)
b = dataset.iloc[:20, 1].to_numpy().reshape(-1,)
questions = np.concatenate((a, b))


def jaccard(x,y):
    shared = np.intersect1d(x[0],y[0])
    union = np.union1d(x[0], y[0])
    return len(shared)/len(union)

def custom_encode(input):
    tokens = {'input_ids': [], 'attention_mask': []}
    new_token = tokenizer.encode_plus(input, max_length=128, truncation=True, padding='max_length',
                                       return_tensors='pt')
    tokens['input_ids'].append(new_token['input_ids'][0])
    tokens['attention_mask'].append(new_token['attention_mask'][0])
    tokens['input_ids'] = torch.stack(tokens['input_ids'])
    tokens['attention_mask'] = torch.stack(tokens['attention_mask'])
    output = model(**tokens)
    embedding = output.last_hidden_state
    attention = tokens['attention_mask']
    mask = attention.unsqueeze(-1).expand(embedding.shape).float()
    mask_embedding = embedding * mask
    summed = torch.sum(mask_embedding, 1)
    counts = torch.clamp(mask.sum(1), min=1e-8)
    mean_pooled = summed/counts
    return mean_pooled.detach().numpy()

def preprocessing():
    # attention mask este o mtrice in care avem 0 pentru padding tokens, iar 1 pentru real tokens
    tokens = {'input_ids': [], 'attention_mask': []}

    # Creez tokeni pentru fiecare intrebare in parte
    for question in questions:
        new_tokens = tokenizer.encode_plus(question, max_length=128, truncation=True, padding='max_length',
                                           return_tensors='pt')
        tokens['input_ids'].append(new_tokens['input_ids'][0])
        tokens['attention_mask'].append(new_tokens['attention_mask'][0])

    tokens['input_ids'] = torch.stack(tokens['input_ids'])
    tokens['attention_mask'] = torch.stack(tokens['attention_mask'])


    # trecem intrebarile prin modelul nostru
    outputs = model(**tokens)

    # extragem starea din ultimul layer al trasnformerului
    embeddings = outputs.last_hidden_state

    # pentru a aplica mean pooling trebuie mai intai sa scapam de valorile din embeddings care refera un padding token
    attention = tokens['attention_mask']
    mask = attention.unsqueeze(-1).expand(embeddings.shape).float()

    # creez o masca in care valorea unui padding token sunt zero
    mask_embeddings = embeddings * mask

    # aplic mean pooling pe vectorul cu intrebari
    summed = torch.sum(mask_embeddings, 1)
    counts = torch.clamp(mask.sum(1), min=1e-8)

    mean_pool = summed/counts

    mean_pool = mean_pool.detach().numpy()
    
    np.savetxt('data.csv', mean_pool, delimiter=',')
    
def search(question, tip, tol ,k):
    file_exists = exists('./data.csv')
    if file_exists:
        data = np.loadtxt('./data.csv', delimiter=',')
    else:
        preprocessing()
        data = np.loadtxt('./data.csv', delimiter=',')
    
    if tip == "Cosine":
        my_question_vec = custom_encode(question)
        
        result = cosine_similarity(my_question_vec, data[0:])
        
        most_similar = np.argsort(result)[0][:-k-1:-1]
        
        res = []
        
        for i in range(0,len(most_similar)):
            if result[0][most_similar[i]] > tol:
                res.append(questions[most_similar[i]])
                
        return res
    if tip == "Jaccard":
        my_question_vec = custom_encode(question)
        result = jaccard(my_question_vec, data[0:])
        most_similar = np.argsort(result)[:-k-1:-1]
        res = []
        for i in range(0,len(most_similar)):
            if int(result[most_similar[i]]) > tol:
                res.append(questions[most_similar[i]])   
        return res


