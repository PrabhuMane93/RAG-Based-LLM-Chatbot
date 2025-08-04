def fixtypo(typomodel, typotokenizer, question): 
    input_ids = typotokenizer(question, return_tensors="pt")['input_ids']
    ok = typomodel.generate(input_ids)
    return(typotokenizer.batch_decode(ok, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])