import http.client
import urllib.parse
import uuid
import json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class TranslateText:

    _subscription_keys = '0579518fc929440cbcbe711aa5b1add3'
    _host = 'api.cognitive.microsofttranslator.com'
    _path = '/translate?api-version=3.0'
    _params = ""
    _input_file = None
    _output_file = None

    def __init__(self, params, input, output):

        self._params = "&to=" + params

        try:
            self._input_file = open(input, 'r')
        except IOError:
            print("Error! Could not open the input file")
            exit(1)

        try:
            self._output_file = open(output, 'w+')
        except IOError:
            print("Error! Could not open the input file")
            exit(1)

        return

    def __del__(self):

        self._output_file.close()
        self._input_file.close()

    def _translate_(self, content):
        headers = {
            'Ocp-Apim-Subscription-Key': self._subscription_keys,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request("POST", self._path + self._params, content, headers)
        response = conn.getresponse()
        return response.read().decode('utf-8')

    def renew_sub_key(self, new_sub_keys):
        self._subscription_keys = new_sub_keys


    def translate(self):
        for line in self._input_file:
            if line == '\n':
                print("Receive a new line input")
                self._output_file.write('\n')
                continue

            requestBody = [{'Text': line, }]
            content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')
            result = self._translate_(content)
            # Note: We convert result, which is JSON, to and from an object so we can pretty-print it.
            # We want to avoid escaping any Unicode characters that result contains. See:
            # https://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence
            output = json.dumps(json.loads(result), indent=4, ensure_ascii=False)
            print(output)

            translated_text = json.loads(result)[0]['translations'][0]['text']
            self._output_file.write(translated_text)

