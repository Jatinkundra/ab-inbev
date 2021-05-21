# Importing libraries
import numpy as np
import re
import os
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler
import os

# Importing the T5 modules from huggingface/transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import AutoTokenizer, AutoModelWithLMHead

import json
import nltk
nltk.download('wordnet')
from nltk.translate.meteor_score import meteor_score
from nltk.translate.bleu_score import sentence_bleu

from spelling_checker import spell_model_activate #new

def check_hate_speech(lang, chat):
    f=open("/home/jatin26/ab-inbev/bad_words_checker/"+lang)
    b= list(f)
    censored=""
    for word in chat.split():
        if word.lower()+"\n" in b:
            word="Bad word"
        censored+=word+" "
    censored=censored[:-1]
    return censored



def translation_sentence(sentence, model, tokenizer):
    inputs= tokenizer(sentence, return_tensors="pt").input_ids

    output=model.generate(inputs)

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    return decoded

def final_translate_for_eng(lang, dataset, model, tokenizer, helsinki_model, helsinki_tokenizer):
    translated_sent=[]
    for i in range(len(dataset)):
        
        decoded_10= translation_sentence(dataset[i] ,model, tokenizer)
        words= decoded_10.split()
        new_words= words[1:]
        decoded_10= ' '.join(new_words)
        decoded_10 = re.sub(r'[{}@()./\|=+_><%]', '', decoded_10)
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
        print(i)
    return translated_sent

def final_translate_for_other_languages(lang, dataset, model, tokenizer, helsinki_model, helsinki_tokenizer):
    translated_sent=[]
    for i in range(len(dataset)):
        
        decoded_10= translation_sentence(dataset[i] ,model, tokenizer)
        words= decoded_10.split()
        new_words= words[1:]
        decoded_10= ' '.join(new_words)
        if decoded_10[0:6] == "to the":
          decoded_10= decoded_10[6:]
        decoded_10 = re.sub(r'[{}@()./\|=+_><%]', '', decoded_10)
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
        print(i)
    return translated_sent

def load_model_other_than_english(language):  
    str= "/home/jatin26/ab-inbev/models/"+language+"_en"
    tokenizer=AutoTokenizer.from_pretrained(str)
    model=AutoModelWithLMHead.from_pretrained(str)
    return model, tokenizer

def load_model_english_2(language):  
    str= "/home/jatin26/ab-inbev/models/en_"+language
    tokenizer=AutoTokenizer.from_pretrained(str)
    model=AutoModelWithLMHead.from_pretrained(str)
    return model, tokenizer

def load_models_english():
    model_list=[]
    tokenizer_list=[]
    for lang in ["fr","de","nl","it"]:
        str= "/home/jatin26/ab-inbev/models/en_"+lang
        #print("model loaded = "+str)
        tokenizer_list.append(AutoTokenizer.from_pretrained(str))
        model_list.append(AutoModelWithLMHead.from_pretrained(str))
    return model_list, tokenizer_list

def translate_all_languages(language_1, language_2, dataset):
    translated_dictionary={}
    if language_1=="en" :
#         model_list, tokenizer_list= load_models_english()
#         j=0
        lang=language_2
        translations_list=[]
        try:
            model and tokenizer
            print("models already loaded")
        except NameError:
            print("loading your models")
            model, tokenizer= load_model_english_2(lang)
            
        try:
            helsinki_model and helsinki_tokenizer
            print("helsinki models already loaded")
        except NameError:
            print("loading helsinki models")
            helsinki_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-"+ lang)
            helsinki_model =AutoModelWithLMHead.from_pretrained("/home/jatin26/ab-inbev/helsinki/opus-mt-en-"+lang, force_download=True)
        
        dataset[0]= check_hate_speech("en", dataset[0])
#         print("Hate speech checked")
        dataset[0]= spell_model_activate("en", dataset[0]) #new
#         print("spelling model checked : " + dataset[0]) 
        translations_list= final_translate_for_other_languages(lang, dataset, model, tokenizer, helsinki_model, helsinki_tokenizer)
        translated_dictionary[lang]= translations_list
#             j=j+1
        return translated_dictionary
    
    else:
        language=language_1
        
        try:
            model_reversal and tokenizer_reversal
            print("models already loaded")
        except NameError:
            print("loading your models")
            model_reversal, tokenizer_reversal= load_model_other_than_english(language)
    
        try:
            helsinki_model_reversal and helsinki_tokenizer_reversal
            print("helsinki models already loaded")
        except NameError:
            print("loading helsinki models")
            helsinki_tokenizer_reversal = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-"+ language+"-en")
            helsinki_model_reversal =AutoModelWithLMHead.from_pretrained("/home/jatin26/ab-inbev/helsinki/opus-mt-"+language+"-en", force_download=True)
        
        
#         print("helsinki models loaded\n\n\n\n")
        dataset[0]= check_hate_speech(language, dataset[0])
#         print("hate speech checked")
        dataset[0]= spell_model_activate(language, dataset[0]) #new
#         print("Spelling check done")
        english_translate= final_translate_for_eng(language, dataset, model_reversal, tokenizer_reversal, helsinki_model_reversal, helsinki_tokenizer_reversal)
#         translated_dictionary["en"]= english_translate
        print("english sentences done\n\n\n\n")
        # j=0
        lang=language_2
        if lang=="en":
            translated_dictionary["en"]= english_translate
        else:
            translations_list=[]
            try:
                model and tokenizer
                print("models already loaded")
            except NameError:
                model, tokenizer= load_model_english_2(lang)
                print("loading your models")

            try:
                helsinki_model and helsinki_tokenizer
                print("helsinki models already loaded")
            except NameError:
                print("loading helsinki models")
                helsinki_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-"+ lang)
                helsinki_model =AutoModelWithLMHead.from_pretrained("/home/jatin26/ab-inbev/helsinki/opus-mt-en-"+lang, force_download=True)

            translations_list= final_translate_for_other_languages(lang, english_translate, model, tokenizer, helsinki_model, helsinki_tokenizer)
            translated_dictionary[lang]= translations_list
                # j=j+1
        return translated_dictionary
        # translated={}
        # lang_list= ["fr","de","nl","it"]
        # lang_list.remove(language)
        # model_helinski = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-"+language+"-en")
        # tokenizer_helinski = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-"+language+"-en")
        # i=0
        
    
