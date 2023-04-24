import openai


openai.api_key = "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"

class GPT:

    def __init__(self) -> None:
        pass
    
    def speak_words(self,message):
        #https://qiita.com/Nekonun/items/2de0d5b3c77206c5ba31　これ参考に入れ替えてみる
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "甘え上手で可愛い子になってください。甘えた口調で回答してください。"},
                {"role": "user", "content": message}
            ]   
        )  
        return response["choices"][0]["message"]["content"]