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

# rich: for a better display on terminal
from rich.table import Column, Table
from rich import box
from rich.console import Console

tokenizer_validator= AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
model_validator=AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-fr-en")

from spellchecker import SpellChecker
from autocorrect import Speller

def spell_model_activate(lng):
    if lng=="it" or lng=="en":
        spell=Speller(lang=lng)
    elif lng=="de" or lng=="fr":
        spell=SpellChecker(language=lng)
    return spell

def check_spell_en_fr_de(sentence,spell):
    #lang= input("Enter the language")
    #sentence=input("Enter the sentence")
    senten=""
    for word in sentence.split():
        misspelled= spell.unknown([word])
        if(misspelled):
            for ch in misspelled:
                word= spell.correction(ch)
        senten= senten+word+" "
    return senten

def spell_check_italian(sentence,spell):
    #sentence=input("Enter the sentence")
    senten=""
    for word in sentence.split():
        word= spell(word)
        senten= senten+word+" "
    return senten

import easyocr
reader = easyocr.Reader(['fr']) # need to run only once to load model into memory
import os
import cv2
import random
try:
 from PIL import Image, ImageFont, ImageDraw
except ImportError:
 import Image

result=reader.readtext("/content/drive/MyDrive/AbInBev/google_lens/menu.jpg")

image_path = "/content/drive/MyDrive/AbInBev/google_lens/menu.jpg"
img = Image.open(image_path)

img_filtered= img.copy()

def translation(sentence, model, tokenizer):
    inputs= tokenizer(sentence, return_tensors="pt").input_ids

    output=model.generate(inputs)

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    return decoded

import re
embeddings=[]
#spell= spell_model_activate("fr")
for i in range(len(result)):
  grammatical = re.sub(r'[^\w\s]', '', result[i][1])
  grammatical= grammatical.lower()
  #checked= check_spell_en_fr_de(result[i][1], spell)
  decoded_2= translation(grammatical, model_validator, tokenizer_validator) 
  embeddings.append(decoded_2)

img_pil= img.copy()
draw = ImageDraw.Draw(img_pil)

for i in range(len(result)):
  draw.rectangle([result[i][0][0][0],result[i][0][0][1],result[i][0][2][0],result[i][0][2][1]], fill="white")

def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
      textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
      new_width = textSize[0][0]
      #print(new_width)
      if (new_width <= width):
          return scale/10
    return 1

img_new_added= np.array(img_pil)
font= cv2.FONT_HERSHEY_COMPLEX
#area_of_img= img_new.shape[0]*img_new.shape[1]
for i in range(len(result)):
  size_of_box=[result[i][0][1][1],result[i][0][2][1],result[i][0][0][0],result[i][0][1][0]]
  area_of_box= (size_of_box[1]-size_of_box[0])*(size_of_box[3]-size_of_box[2])

  scale= get_optimal_font_scale(embeddings[i], size_of_box[3]-size_of_box[2])
  
  #scale= area_of_box/area_of_img
  #scale= scale*(size_of_box[3]-size_of_box[2])
  img_new_added= cv2.putText(img_new_added, text=embeddings[i], org= (int(result[i][0][3][0]), int(result[i][0][3][1])), fontFace= font, fontScale=scale, color= (0, 0, 0), thickness=1)

from google.colab.patches import cv2_imshow
img_coloured= cv2.cvtColor(img_new_added,cv2.COLOR_BGR2RGB)
cv2_imshow(img_coloured)
cv2.imwrite("converted.jpg", img_coloured)


