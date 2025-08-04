from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModel

# Define the model and tokenizer names
model_name = "google/t5-large"

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large", pad_token_id = tokenizer.eos_token_id).to('cpu')

save_path = "./models/flan_t5_large"
save_path_tokenizers = "./tokenizers/flan_t5_large"


model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path_tokenizers)

model =AutoModel.from_pretrained("sentence-transformers/multi-qa-mpnet-base-dot-v1")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/multi-qa-mpnet-base-dot-v1")
save_path = "./models/multi-qa-mpnet-base-dot-v1"
save_path_tokenizers = "./tokenizers/multi-qa-mpnet-base-dot-v1"

model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path_tokenizers)

model =AutoModelForSeq2SeqLM.from_pretrained("oliverguhr/spelling-correction-english-base")
tokenizer = AutoTokenizer.from_pretrained("oliverguhr/spelling-correction-english-base")
save_path = "./models/spelling-correction-english-base"
save_path_tokenizers = "./tokenizers/spelling-correction-english-base"



model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path_tokenizers)
