import urllib2
import json

def correctexp(data):
    data= str(data)
    # Azure portal URL.
    base_url = 'https://westus.api.cognitive.microsoft.com/'
    # Your account key goes here.
    account_key = 'd5306ebb02e24b679e7d6a79f9fdc5e2'

    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': account_key}

    # temp = '{"documents":[{"id":"1","text":' + data +'}]}'
    # input_texts = '{"documents":[{"id":"1","text":"sample"}]}'

    # Manipulating the input string to be sent as a request!
    input_texts = '{"documents":[{"id":"1","text":"' + data + '"}]}'

    num_detect_langs = 1;

    # Detect key phrases.
    batch_keyphrase_url = base_url + 'text/analytics/v2.0/keyPhrases'
    req = urllib2.Request(batch_keyphrase_url, input_texts, headers)
    response = urllib2.urlopen(req)
    result = response.read()
    obj = json.loads(result)

    for keyphrase_analysis in obj['documents']:
        # print('Key phrases ' + str(keyphrase_analysis['id']) + ': ' + ', '.join(map(str, keyphrase_analysis['keyPhrases'])))
        res = ', '.join(map(str, keyphrase_analysis['keyPhrases']))

    return res

