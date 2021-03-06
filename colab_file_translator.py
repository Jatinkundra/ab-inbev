!pip install easyocr
!pip install sentencepiece
!pip install transformers
!pip install LanguageIdentifier
!pip install torch
!pip install rich[jupyter]
!pip install LanguageIdentifier

import numpy as np
import re
import os
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler
import os
import LanguageIdentifier

# Importing the T5 modules from huggingface/transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import AutoTokenizer, AutoModelWithLMHead

import json
!pip install -U nltk
import nltk
nltk.download('wordnet')
from nltk.translate.meteor_score import meteor_score
from nltk.translate.bleu_score import sentence_bleu

def translation_sentence(sentence, model, tokenizer):
    inputs= tokenizer(sentence, return_tensors="pt").input_ids

    output=model.generate(inputs)

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    return decoded

def final_translate_for_eng(dataset, model, tokenizer, helsinki_model, helsinki_tokenizer):
    translated_sent=[]
    for i in range(len(dataset)):
        decoded_10= translation_sentence(dataset[i] ,model, tokenizer)
        words= decoded_10.split()
        new_words= words[1:]
        decoded_10= ' '.join(new_words)
        decoded_10 = re.sub(r'[^\w\s]', '', decoded_10)
        decoded_1= translation_sentence(dataset[i], helsinki_model, helsinki_tokenizer)
        decoded_1 = re.sub(r'[^\w\s]', '', decoded_1)
        # decoded_1= translation(decoded_1, helsinki_model_reversal, helsinki_tokenizer_reversal)
        # decoded_1 = re.sub(r'[^\w\s]', '', decoded_1)
        # decoder_google= google_translator.translate(dataset[i], lang_tgt='en')
        score_x= meteor_score(decoded_1, decoded_10)
        if score_x>=0.24:
            translated_sent.append(decoded_10)
        else:
            translated_sent.append(decoded_1)
        # print(i)
    return translated_sent

def final_translate_for_other_languages(dataset, model, tokenizer, helsinki_model, helsinki_tokenizer):
    translated_sent=[]
    for i in range(len(dataset)):
        decoded_10= translation_sentence(dataset[i] ,model, tokenizer)
        words= decoded_10.split()
        new_words= words[1:]
        decoded_10= ' '.join(new_words)
        if decoded_10[0:6] == "to the":
          decoded_10= decoded_10[6:]
        decoded_10 = re.sub(r'[^\w\s]', '', decoded_10)
        decoded_1= translation_sentence(dataset[i], helsinki_model, helsinki_tokenizer)
        decoded_1 = re.sub(r'[^\w\s]', '', decoded_1)
        # decoded_1= translation(decoded_1, helsinki_model_reversal, helsinki_tokenizer_reversal)
        # decoded_1 = re.sub(r'[^\w\s]', '', decoded_1)
        # decoder_google= google_translator.translate(dataset[i], lang_tgt='en')
        score_x= meteor_score(decoded_1, decoded_10)
        if score_x>=0.24:
            translated_sent.append(decoded_10)
        else:
            translated_sent.append(decoded_1)
        # print(i)
    return translated_sent

def load_model_other_than_english(language):  
    str= "/content/drive/MyDrive/AbInBev/models_git/"+language+"_en"
    tokenizer=AutoTokenizer.from_pretrained(str)
    model=AutoModelWithLMHead.from_pretrained(str)
    return model, tokenizer

def load_models_english():
    model_list=[]
    tokenizer_list=[]
    for lang in ["fr","de","nl","it"]:
        str= "/content/drive/MyDrive/AbInBev/models_git/en_"+lang
        #print("model loaded = "+str)
        tokenizer_list.append(AutoTokenizer.from_pretrained(str))
        model_list.append(AutoModelWithLMHead.from_pretrained(str))
    return model_list, tokenizer_list

def translate_all_languages(language, dataset):
    translated_dictionary={}
    if language=="en" :
        model_list, tokenizer_list= load_models_english()
        i=0
        for lang in ["fr","de","nl","it"]:
            translations_list=[]
            helsinki_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-"+ lang)
            helsinki_model =AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en-"+ lang)
            translations_list=final_translate_for_eng(dataset, model_list[i], tokenizer_list[i], helsinki_model, helsinki_tokenizer)
            translated_dictionary[lang]= translations_list
            i=i+1
        return translated_dictionary
    
    else:
        model_reversal, tokenizer_reversal= load_model_other_than_english(language)
        model_list, tokenizer_list= load_models_english()
        english_translated=[]
        helsinki_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-"+ language+"-en")
        helsinki_model =AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-"+ language+"-en")
        english_translate= final_translate_for_eng(dataset, model_reversal, tokenizer_reversal, helsinki_model, helsinki_tokenizer)
        translated_dictionary["en"]= english_translate
        i=0
        for lang in ["fr","de","nl","it"]:
            print("checking for : "+ lang)
            if lang==language:
                i=i+1
                continue
            else:
                translations_list=[]
                helsinki_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-"+ lang)
                helsinki_model =AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en-"+ lang)
                translations_list= final_translate_for_other_languages(english_translate, model_list[i], tokenizer_list[i], helsinki_model, helsinki_tokenizer)
                translated_dictionary[lang]= translations_list
                i=i+1
        return translated_dictionary
        # translated={}
        # lang_list= ["fr","de","nl","it"]
        # lang_list.remove(language)
        # model_helinski = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-"+language+"-en")
        # tokenizer_helinski = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-"+language+"-en")
        # i=0
        
x= pd.read_json(input("File Path on google drive (Please mount your google drive to give the file path): "))
dataset=[]
for i in x:
    dataset.append(x[i])
import re
translations={}
from LanguageIdentifier import predict
language= predict(dataset[0])
translations= translate_all_languages(language, dataset)
final_path= input("Please enter location to store the generated excel file: ")
stri= final_path+"/spammers.xlsx"
final_sheet= pd.DataFrame(translations)
final_sheet.to_excel(stri)
    