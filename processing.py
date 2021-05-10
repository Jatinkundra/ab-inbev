import json
import requests
import pandas as pd

def reload():
  username = 'jatin26'
  api_token = 'a62d062e9bb283a15de58a297bc0840e6e009807'
  domain_name = "jatin26.pythonanywhere.com"

  response = requests.post(
      'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
          username=username, domain_name=domain_name
      ),
      headers={'Authorization': 'Token {token}'.format(token=api_token)}
  )
  if response.status_code == 200:
      print('reloaded OK')
  else:
      print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))

# from LanguageIdentifier import predict
heroku_url = 'http://jatin26.pythonanywhere.com/' # change to your app name
# sample data
x= pd.read_excel(input("File Path for dataFrame: "))
final_path= input("Please enter location to store the generated excel file: ")
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
# dataset_copy= dataset_copy[0:20]
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


stri= final_path+"/spammers.xlsx"
final_sheet= pd.DataFrame(translations)
final_sheet.to_excel(stri)
