#モジュール部品
from pydantic import BaseModel
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware # 追加
import chatgpt
import time
import voice
import uvicorn
app = FastAPI()
api = "/api"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://ai-chara.web.app"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

#chatGPTのリクエストシステム
chatGPT = chatgpt.GPT()
Voice = voice.Voicevox("Z_T5W_G652T08-I")

#メッセージを受け取るための型クラス。(/message)
class MessageModel(BaseModel):
    message: str

class Converter:
    def __init__(self) -> None:
        self.flag = 0
        self.point = 100000

    def charge_point(self):
        #もしフラグが立っているのであれば実行する
        if self.flag == 1:
            #ポイントをチャージします。
            print('ポイントをチャージします。')


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


@app.get("/")
async def root():
    return {"greeting":"Hello world"}

@app.post(f'{api}/message/')
async def message(data: MessageModel):
    print("時間測定開始")
    start = time.time()
    print("メッセージを読み込みました。")
    msg = data.message
    print("ChatGPTへ接続しました。")
    response = chatGPT.speak_words(msg)
    print("B64へ接続します。")
    b64code = converter.WordToVoice(response)
    print("総合終了")
    end = time.time()
    total = (end-start)
    print(f'{total}秒かかりました。')


    return {"response_message":response,"voicebase64":b64code}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)