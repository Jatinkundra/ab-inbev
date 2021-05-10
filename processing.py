import json
import requests
# from LanguageIdentifier import predict
heroku_url = 'http://jatin26.pythonanywhere.com/' # change to your app name
# sample data
x= pd.read_excel(input("File Path for dataFrame: "))
x=x.to_dict()
dataset_copy=[]
for i in x.values():
  a=i
for i in a.values():
  dataset_copy.append(i)

# x= dataset_copy["French"][0:20]
a=0
b=10
send_request=[]
for count in range(int(len(dataset_copy)/10)):
  y=dataset_copy[a:b]
  y= pd.DataFrame(y)
  y= y.to_dict()
  data = json.dumps(y[0])
  reload()
  send_request.append(requests.post(heroku_url, data))
  if a==0:
    translations= send_request[0].json()["results"]
  else:
    for i in translations.keys():
      for item in send_request[count].json()["results"][i]:
        translations[i].append(item)
  a=b
  b=b+10

final_path= input("Please enter location to store the generated excel file: ")
stri= final_path+"/spammers.xlsx"
final_sheet= pd.DataFrame(translations)
final_sheet.to_excel(stri)
