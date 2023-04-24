from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_apscheduler import APScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import chatgpt
import voice
import secure
import time


app = Flask(__name__)
CORS(app)

chatGPT = chatgpt.GPT()
ransack = voice.Ransack()
#sched = BlockingScheduler(daemon=True)

print("BOTを起動しています。")

print("API-KEYを取得しています。")
#apikey = ransack.go()
apikey = "b_72W61-e420E55"
if apikey != 0:
    print("API-KEYを取得しました。")

Voice = voice.Voicevox(apikey)
api = "/api/v1"

class Converter:
    def __init__(self) -> None:
        self.flag = 0
        self.point = 100000

    def charge_point(self):
        #もしフラグが立っているのであれば実行する
        if self.flag == 1:
            #ポイントをチャージします。
            print('ポイントをチャージします。')
            voice.Voicevox(ransack.go())


    def WordToVoice(self,text):
        #chatGPTの返答をBase64型音声へ変更する。
        wav = Voice.speak(text)
        print("wavファイル化完了しました。")
        base64 = Voice.base64file(wav)
        print("wavをBase64へ変更しました。")
        Voice.file_destroy(wav)
        print('ファイルを削除しました。')
        minuspoint = 1500 + 100*len(text)
        self.point = (self.point - (1500 + minuspoint))
        print(f"{minuspoint}ポイントを消費しました。")
        print(f"現在ポイント：{self.point}")

        #チャージ
        if self.point < 10000:
            self.flag = 1


        return base64
    
converter = Converter()

def charge_point():
    #もしフラグが立っているのであれば実行する
    print("FLAG IS ACTIVE.")
    if converter.flag == 1:
        #ポイントをチャージします。
        print('ポイントをチャージします。')
        voice.Voicevox(ransack.go())


@app.route('/')
def home():
    return "home"

@app.route(f'{api}/message',methods=['GET','POST'])
def message():
    print("時間測定開始")
    start = time.time()
    print("メッセージを読み込みました。")
    msg = request.json['message']
    print("ChatGPTへ接続しました。")
    response = chatGPT.speak_words(msg)
    print("B64へ接続します。")
    b64code = converter.WordToVoice(response)
    print("総合終了")
    end = time.time()
    total = (end-start)
    print(f'{total}秒かかりました。')


    return jsonify({"response_message":response,"voicebase64":b64code})

@app.route(f'{api}/messages',methods=['GET','POST'])
def messages():
    msg = request.json['message']

    return jsonify({"response_message":msg})

#@sched.scheduled_job('interval', seconds=30)
def charge_point():
    #もしフラグが立っているのであれば実行する
    print("FLAG IS ACTIVE.")
    if converter.flag == 1:
        #ポイントをチャージします。
        print('ポイントをチャージします。')
        voice.Voicevox(ransack.go())


#sched.start()#定期実行のために必要なモジュールを起動

if __name__ == "__main__":
    app.run(debug=True,port=6400,use_reloader=False)