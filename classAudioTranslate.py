import websocket
import ssl


class AudioTranslate:

    _subscription_keys = '801361cdf47544eeadd940b6923f8e1e'
    _host = 'wss://dev.microsofttranslator.com'
    _path = '/speech/translate'
    _params = ''  # '?api-version=1.0&from=en-US&to=it-IT&features=texttospeech&voice=it-IT-Elsa'
    _uri = ''  # host + path + params

    _input_file = None
    _output_file = None

    _output = None
    _client = None

    def __init__(self, input, output, in_l='en-US', out_l='zh-CN'):

        self._params = '?api-version=1.0&from=' + in_l + '&to=' + out_l + '&features=texttospeech'
        self._uri = self._host + self._path + self._params

        self._input_file = input
        self._output_file = output

        self._output = bytearray()

        self._client = websocket.WebSocketApp(
            self._uri,
            header=[
                'Ocp-Apim-Subscription-Key: ' + self._subscription_keys
            ],
            on_open=self.on_open,
            on_data=self.on_data,
            on_error=self.on_error,
            on_close=self.on_close
        )

    def __del__(self):
        self._input_file.close()

    def on_open(self, client):
        print("Connected.")

        # r = read. b = binary.
        with open(self._input_file, mode='rb') as file:
            data = file.read()

        print("Sending audio.")
        client.send(data, websocket.ABNF.OPCODE_BINARY)
        # Make sure the audio file is followed by silence.
        # This lets the service know that the audio input is finished.
        print("Sending silence.")
        client.send(bytearray(32000), websocket.ABNF.OPCODE_BINARY)

    def on_data(self, client, message, message_type, is_last):

        # global output
        if websocket.ABNF.OPCODE_TEXT == message_type:
            print("Received text data.")
            print(message)
        # For some reason, we receive the data as type websocket.ABNF.OPCODE_CONT.
        elif websocket.ABNF.OPCODE_BINARY == message_type or websocket.ABNF.OPCODE_CONT == message_type:
            print("Received binary data.")
            print("Is last? " + str(is_last))
            self._output = self._output + message
            if (True == is_last):
                # w = write. b = binary.
                with open(self._output_file, mode='wb') as file:
                    file.write(self._output)
                    print("Wrote data to output file.")
                client.close()
        else:
            print("Received data of type: " + str(message_type))

    def on_error(self, client, error):
        print("Connection error: " + str(error))

    def on_close(self, client):
        print("Connection closed.")

    def run(self):
        print("Connecting...")
        self._client.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


    




