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
        print(i)
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
        print(i)
    return translated_sent

def load_model_other_than_english(language):  
    str= lang+"toenglishtrain/resulting_model/model_files"
    tokenizer=AutoTokenizer.from_pretrained(str)
    model=AutoModelWithLMHead.from_pretrained(str)
    return model, tokenizer

def load_models_english():
    model_list=[]
    tokenizer_list=[]
    for lang in ["fr","de","nl","it"]:
        str= lang+"train/resulting_model/model_files"
        #print("model loaded = "+str)
        tokenizer_list.append(AutoTokenizer.from_pretrained(str))
        model_list.append(AutoModelWithLMHead.from_pretrained(str))
    return model_list, tokenizer_list

def translate_all_languages_except_english(language, dataset):
    translated_dictionary={}
    if(language=="en"){
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
    }
    else{
        model_reversal, tokenizer_reversal= load_models_other_than_english(language)
        model_list, tokenizer_list= load_models_english()
        english_translated=[]
        helsinki_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-"+ lang+"-en")
        helsinki_model =AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en"+ lang+"-en")
        english_translate= final_translate_for_eng(dataset, model_reversal, tokenizer_reversal, helsinki_model, helsinki_tokenizer)
        translated_dictionary["en"]= english_translate
        i=0
        for lang in ["fr","de","nl","it"]:
            if lang==language:
                i=i+1
                continue
            else:
                helsinki_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-"+ lang)
                helsinki_model =AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en-"+ lang)
                final_translate_for_other_languages((english_translate, model_list[i], tokenizer_list[i], helsinki_model, helsinki_tokenizer)
                translated_dictionary[lang]= translations_list
                i=i+1
        return translated_dictionary
        # translated={}
        # lang_list= ["fr","de","nl","it"]
        # lang_list.remove(language)
        # model_helinski = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-"+language+"-en")
        # tokenizer_helinski = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-"+language+"-en")
        # i=0
        
    }