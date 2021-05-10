import json
import requests
heroku_url = 'http://jatin26.pythonanywhere.com/' # change to your app name
# sample data
x= pd.read_json(input("File Path for dataFrame: "))
dataset_copy= list(x)
#x= dataset_copy[0:30]
a=0
b=10
send_request=[]
for count in range(int(len(x)/10)):
  y=x[a:b]
  y= y.to_dict()
  data = json.dumps(y)
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