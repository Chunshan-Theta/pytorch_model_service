from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline, AutoConfig

model_name = "roberta-base-finetuned-jd-binary-chinese"
model = AutoModelForSequenceClassification.from_pretrained(f'./util/{model_name}')
tokenizer = AutoTokenizer.from_pretrained(f'./util/{model_name}/')
text_classification = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)


def senti(text):
    global text_classification
    result = text_classification(text)[0]
    return ({
        "label": result["label"].split(" ")[0],
        "score": result["score"]
    })

#print(senti("這回答讓人無法滿意"))
