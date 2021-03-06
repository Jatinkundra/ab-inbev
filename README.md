
# Hey there! <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="25px"> 
---
### We are team **Spammers** from *Thapar University, Patiala* Presenting our project on *Language Translation Layer*
---

### *Processing Specification and Method*
* Please install ***model_check_requirements.txt*** before running processing.py
* Enter the data into API through code provided in ***processing.py***
* Language specification is not needed, as it will be detected automatically
* The data will be recieved as an excel file in preprocessing.py
* Enter the path where you want to recieve the generated translated excel file in all other 4 languages
* Please Enter the file in this format, the first row to be kept for the name of the 
language or empty or as you like. Please dont keep any data in the first row. Open the
preprocessing.py in google colab or jupyter notebook and install the dependecies as 
mentioned in the first three lines. Just input the excel sheet location and you
will recieve an excel sheet of the translated sentences in your desired location
<p align="center">
<img src="https://github.com/Jatinkundra/ab-inbev/blob/main/image-translation_samples/demo.png" width="300" margin-left="700"> 
   </p>


### *INTRODUCTION*
#### Is English the only Language for Business<img src="https://media.giphy.com/media/dyX9ixfxMpOUGawfdK/giphy.gif" width="25px"><img src="https://media.giphy.com/media/ifHCnV5Z0cAwwlwNtK/giphy.gif" width="50px">
#### English is the lingua franca of the business world, the most commonly taught foreign language in schools worldwide and the official language of 20 of the most important international organisations, but English is significantly less popular than we would like to believe. It is the second language of only 39 percent of the French population. In Italy, this figure is just shy of 35 percent, and in Spain it is less than 23 percent.The situation gets drastically worse when we take emerging markets into account: only 5.2 percent of people in Russia speak English fluently.

#### When you take into consideration the fact that the combined population of these three countries is over 1.7 billion, it becomes obvious that not translating your content can cost your business an absolute fortune.This  project has been specifically made for the people in **B2B BUSINESS** .Since, everytime the conversations may not be possible in English or any common language, there must be something to translate and ease the international trades. Communicating with international buyers in their preferred languages is one of the most resonant and expedient ways to build relationships and provide value. 

### *OUR FEATURES*  
 * **_Bad Word Filter_** <img src="https://media.giphy.com/media/2T2hGmgr155LUgk5nA/giphy.gif" width="40px">
    * We are providing a layer of bad word filter in order to avoid miscommunications.
 * **_Precision Score_**
    * A precision score is calculated for every translation, and its metric based calculation helps to provide a more accurate translation
### *OUR NOVELTIES*     <img src="https://media.giphy.com/media/boXE8z5vda35elvKhv/giphy.gif" width="40px">
* **_Image language Translation for various products used overseas_**
   * In B2B,B2C conversations, invoices, bills , product images and many more things are used but sometimes language becomes the barriar in international trade. 
   * We will be easing out this by being able to convert the text in images to the desired language and create valuable resources for on-the-ground sales.
   * This will increase global discoverability and brand awareness . 
   *  By this, we wil be able to translate two forms of chat : images and text together by just integrating the api in platforms like Whatsapp, slack etc.
   *  <p align="center" ><img src="https://github.com/Jatinkundra/ab-inbev/blob/main/image-translation_samples/1.jpeg" width="250"> <img src="https://media.giphy.com/media/hU2y2OCpZLNTnIeYxh/giphy.gif" width="150">       <img src="https://github.com/Jatinkundra/ab-inbev/blob/main/image-translation_samples/0.jpeg" width="250"></p>
* **_Translation based on Intent_**
   * Intent Detection is a vital component of any task-oriented conversational system.
   *  In order to understand the user???s current goal, the system must leverage its intent detector to classify the user???s utterance (provided in varied natural language) into one of several predefined classes, that is, intents.
   *  Our model is trained based on Intent rather than words .The basic essence of the speech is preserved while translating. 
* **_Automatic Language Detector_**
   * Through our model, we will be able to detect the language to be translated automatically that will reduce the complications in translation. 
   * It will give a user friendly experience , because the user needs not to type explicitely the language he wants to converse in. 
* **_Spelling Checker_**
   * To err is human. 
   * While tying , we may type some wrong words, that may result in changing the meaning of sentences or the translation layer giving error.
   * So,for the ease and efficient communication between the two,we would be verifing  the spelling and grammar based on intent before translating it.

### *WHO ARE BENEFITTED*
* People around the globe who are dealing in international trade
* People involved in B2B Businesses
* People who don't know English

### *Using Google colab file*
* Copy the google_colab file in google colab
* This models folder has all the models pretrained in it
* Link to the models folder : https://drive.google.com/drive/folders/1r3czZ3oxVlD9IqozEsVt2MVD5prUvu8F?usp=sharing
* open the google colab file and in the load_models_english() and load_models_for_other_languages() add the path location of this shared folder once mounted in your own drive

