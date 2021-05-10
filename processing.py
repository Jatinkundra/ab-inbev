import json
import requests

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