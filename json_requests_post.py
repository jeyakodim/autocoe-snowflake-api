import requests

url = input("Enter a valid url: ")
my_obj = {}
string = str(url)
index = string.index('qb/')
# print(string[index+3:])
if string[index+3:] == 'digital':
    my_obj = {'tableId': 'bhspmv42w', 'URL': 'https://api.quickbase.com/v1/reports/36/run', 'Query': 'QKB_JSON_DATA'}
elif string[index+3:] == 'maintenance':
    my_obj = {'tableId': 'brksg8rfj', 'URL': 'https://api.quickbase.com/v1/reports/10/run', 'Query': 'SURF_MAINTENANCE'}
elif string[index+3:] == 'risk':
    my_obj = {'tableId': 'brkvaxnwi', 'URL': 'https://api.quickbase.com/v1/reports/6/run', 'Query': 'SURF_RISK_REPORT'}
elif string[index+3] == 'spend':
    my_obj = {'tableId': 'briyy8zey', 'URL': 'https://api.quickbase.com/v1/reports/6/run', 'Query': 'SURF_SPEND'}
elif string[index+3] == 'works':
    my_obj = {'tableId': 'brkvcdw65', 'URL': 'https://api.quickbase.com/v1/reports/6/run', 'Query': 'SURF_SOW_REPORT'}
else:
    print('Enter valid URL')


x = requests.post(url, json=my_obj)

# print the response text (the content of the requested file):

print(x.text)
