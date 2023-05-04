import requests
import os
import io
import json
import random
import secure
import base64
import time

security = secure.Security()




class Voicevox:

    def __init__(self,apikey) -> None:
        self.apikey = apikey

    def speak(self,text):
        # 音声合成クエリの作成
        try:
            # 音声合成クエリの作成
            apikey = self.apikey
            make_query = requests.get(f'https://deprecatedapis.tts.quest/v2/voicevox/audio/?text={text}&key={apikey}&speaker=1')
            # 音声合成データの作成
            #speak_data = requests.post('http://127.0.0.1:50021/synthesis',params = {'speaker': 1},data=json.dumps(make_query.json()))

            content_id = security.randomname(10)

        #wavデータの生成
            time.sleep(1)
            with open(os.path.join(os.path.dirname(__file__), os.path.join("voice",f"{content_id}.wav")), mode='wb') as f:
                f.write(make_query.content)
            
            
            return content_id
        except Exception as e:
            print(e)
            print("Error wavfile")

    def base64file(self,content_id):
        path = './chatgpt_backend/voice'
        try:
            with open(os.path.join(os.path.dirname(__file__), os.path.join("voice",f"{content_id}.wav")),'rb') as file:
                data = base64.b64encode(file.read())
                return data.decode('utf-8')
        except Exception as e:
            return "error"
    
    def file_destroy(self,content_id):
        path = './chatgpt_backend/voice'
        try:
            os.remove(os.path.join(os.path.dirname(__file__), os.path.join("voice",f"{content_id}.wav")))
        except Exception as e:
            print(e)
            print("Sorry. I don't destroy file.")


