import os
import torch

def find_match6(similaritymodel, similaritytokenizer, question):
    paras = []
    directory = os.path.join(os.getcwd(),"assets","whitepaper")
    filenames = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            filenames.append(f)
            print(f)
            file1 = open(f,"r+")
            Y = file1.read()
            paras.append(Y)
  
    def cls_pooling(model_output):
        return model_output.last_hidden_state[:,0]

    #Encode text
    def encode(texts):
        # Tokenize sentences
        encoded_input = similaritytokenizer(texts, padding=True, truncation=True, return_tensors='pt')
        # Compute token embeddings
        with torch.no_grad():
            model_output = similaritymodel(**encoded_input, return_dict=True)
        # Perform pooling
        embeddings = cls_pooling(model_output)
        return embeddings

    query_emb = encode(question)
    doc_emb = encode(paras)

    #Compute dot score between query and all document embeddings
    response = torch.mm(query_emb, doc_emb.transpose(0, 1))[0].cpu().tolist()

    print(response)

    maxindex = response.index(max(response))
    print(filenames[maxindex])
    f = os.path.join(filenames[maxindex])
    print(f)
    file1 = open(f,"r+")
    Y = file1.read()
    temptext =  Y.replace("\n", "") + "\n" + "'" + question + "'"
    return temptext