from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from pydub import AudioSegment
import speech_recognition as sr
import requests
import os
import io
import json
import random
import secure
import base64
import time

security = secure.Security()

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
start = time.perf_counter()
driver = webdriver.Chrome(options=options)


class Ransack: ## 仮組みクラス (ほんとはダメです。ただ入れてるだけです。サービス化するときはこれ使わないです。)

    def __init__(self) -> None:
        pass
    
    def go(self):
        #cookieを全削除する。
        driver.delete_all_cookies()
        # アクセスパラメーター
        access_mode = 0
        #su-shiki.com/api へアクセスする。
        driver.get("https://su-shiki.com/api/")
        time.sleep(random.randint(2,6))
        # Recaptchaへアクセスする。
        driver.switch_to.frame(driver.find_element(By.TAG_NAME,"iframe"))
        time.sleep(random.randint(2,4))
        # Recaptchaのチェックボックスをクリックする。
        driver.find_element(By.ID,"recaptcha-anchor").click()
        # くるくる終わるまで待つ
        while driver.find_element(By.ID,"recaptcha-anchor").get_attribute('aria-disabled') == 'true': 
            time.sleep(1)
        if driver.find_element(By.ID,"recaptcha-anchor").get_attribute('aria-checked') == 'true':
            # この時点でクリアした場合は、アクセスモード1へ変更する。
            access_mode = 1
        
        print(access_mode == 1)
        
        if access_mode == 1:
            driver.switch_to.default_content()
            time.sleep(2)

            # apikeyへチェックマークを差し込む
            apicheck = driver.find_element(By.NAME,"voicevox")

            if apicheck.is_selected() == True:
                print('This job is skip.')
            else:
                driver.find_element(By.XPATH,"/html/body/center/div/form/div[2]/center/span/label").click()

            # 送信
            driver.find_element(By.XPATH,"/html/body/center/div/form/div[2]/button").click()
            print("送信しました。")
            time.sleep(10) 
            setup = driver.find_element(By.XPATH,"/html/body/div[2]/center/input").get_attribute("value")
            print(setup)
            driver.close()
            return setup
        else:
            time.sleep(random.randint(5,10))
            driver.switch_to.default_content()
            time.sleep(random.randint(1,3))
            #iframeを入れ替える。
            driver.switch_to.frame(driver.find_element(By.XPATH,"/html/body/div/div[4]/iframe"))
            time.sleep(random.randint(3,8))
            #linkを取得する。
            driver.find_element(By.XPATH,"/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button").click()
            time.sleep(random.randint(5,10))
            try:
                link = driver.find_element(By.XPATH,"/html/body/div/div/div[7]/a").get_attribute("href")
                print(f'{link}を読み込みます。')
                savewave = self.savewave(link)

                driver.find_element(By.ID,"audio-response").send_keys(savewave)
                time.sleep(random.randint(2,6))
                driver.find_element(By.ID,"recaptcha-verify-button").click()
                time.sleep(5)

                time.sleep(3)
                driver.switch_to.default_content()
                time.sleep(2)

                # apikeyへチェックマークを差し込む
                apicheck = driver.find_element(By.NAME,"voicevox")

                if apicheck.is_selected() == True:
                    print('This job is skip.')
                else:
                    driver.find_element(By.XPATH,"/html/body/center/div/form/div[2]/center/span/label").click()

                # 送信
                driver.find_element(By.XPATH,"/html/body/center/div/form/div[2]/button").click()
                print("送信しました。")
                time.sleep(10) 
                setup = driver.find_element(By.XPATH,"/html/body/div[2]/center/input").get_attribute("value")
                print(setup)
                driver.close()
                return setup
            except Exception as e:
                driver.close()
                print(e)
                print("BOTとして見られたため、リクエストエラーになりました。数分後にリトライしてください。")
                return 0

        #with open(os.path.join(os.path.dirname(__file__), os.path.join("recaptcha",f"{google_code}.wav")), mode='wb') as f:

    
    def savewave(self,audio_url) -> str:
        src = AudioSegment.from_file(io.BytesIO(requests.get(audio_url).content))
        src = src.set_channels(1) #音声ファイルをモノラルに
        src = src.set_frame_rate(16000) #識別には必要無いデータを削る
        src = src.set_sample_width(2) #同様
        audio = io.BytesIO()
        src.export(audio,'wav')
        audio.seek(0)
        r = sr.Recognizer()
        with sr.AudioFile(audio) as source:
            audio = r.record(source)

        print(r.recognize_google(audio))
        return r.recognize_google(audio)




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


