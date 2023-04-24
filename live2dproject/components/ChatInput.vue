<template>
    <div class="wakaran" @click="speak()">
        <div class="chatmark">
            <p class="hatuwa">発話</p>
        </div>
        <p class="chatter">{{ chat }}</p>
    </div>
</template>

<script>
const SpeechRecognition = webkitSpeechRecognition || SpeechRecognition;

export default {
  name: 'ChatInput',
  data() {
    return {
        comment: "",
        chat: "",
        comment_log: [],
        audioctx: new AudioContext(),
        recognition: new SpeechRecognition()
    }
  },
  updated() {
    this.scrollToEnd()
  },
  methods: {
    speak(){
        const binary = process.env.CALL_SOUND
        const url = `data:audio/wav;base64,${binary}`
        const audio = new Audio(url)
        audio.play()
        this.recognition.onresult = (event) => {
            console.log(event)
            this.chat = event.results[0][0].transcript
            this.addcomment(event.results[0][0].transcript)
            while(!event.results[0].isFinal){
                this.chat = event.results[0][0].transcript
            }
        }
        console.log('soundplay')
        this.recognition.start()
    },
    addcomment(comm){
        this.comment_log.push(this.comment)
        // var container = this.$refs.comments
        var comment = comm
        this.comment = ""
        // container.scrollTop = container.scrollHeight;
        this.$axios.post("http://localhost:6400/api/v1/message",{"message":comment}).then((res) => {
            console.log(res.data.response_message)
            this.$emit('outputmessage', res.data.response_message)
            this.sound(res.data.voicebase64)
            // changevalue.change_value(Math.random())
        }).catch((res) => {
            console.log('outputmessage' + res)
        })
    },
    scrollToEnd() {
          const chatLog = this.$refs.comments
          if (!chatLog) return
          chatLog.scrollTop = chatLog.scrollHeight
    },
    sound(binary){
        var url = `data:audio/wav;base64,${binary}`
        const audio = new Audio(url)
        audio.play()
        this.buffer(url).then((peaksArr) => { //2500
            var count = 0
            var TimerID = setInterval(() => {
                if (count < peaksArr[0].length) {
                    changevalue.change_value((peaksArr[0][count]*10))
                    count++
                } else {
                    console.log('cleared')
                    clearInterval(TimerID)
                }
            }, 1/60);
            changevalue.change_value(NaN)
        }).catch((err) => {
            console.error(err)
        })
    },
    buffer(url,peakLength) {
        const promise = new Promise((resolve,reject) => {
            const request = new XMLHttpRequest()
            request.open('GET',url,true)
            request.responseType = 'arraybuffer'
            request.onload = () => {
                if (request.status == 200){
                    this.onLoadSound(request.response, resolve, reject)
                } else {
                    reject(request.statusText)
                }
            }
            request.send()
        })

        return promise
    },
    onLoadSound(audioData, resolve, reject) {
        this.audioctx.decodeAudioData(audioData).then((buffer) => {
            const duration = buffer.duration
            // duration * x = 2500
            console.log(duration * 250)
            const ch1 = buffer.getChannelData(0)
            const peaks1 = this.getPeaks(ch1, duration * 250);

            const ch2 = buffer.getChannelData(0)
            const peaks2 = this.getPeaks(ch2, duration * 250);

            resolve([peaks1, peaks2]);
        
        }).catch((err) => {
            reject(err)
        })
    },
    getPeaks(array, peakLength){
        let step;
        if(!peakLength){
            peakLength = 9000;
        }

        step = Math.floor(array.length / peakLength);

        if (step < 1) { 
            step = 1;
        }

        let peaks = [];
        for(let i = 0, len = array.length; i < len; i += step){
            const peak = this.getPeak(array, i, i + step);
            peaks.push(peak);
        }
        return peaks;
    },
    getPeak(array,startIndex,endIndex){
        const sliced = array.slice(startIndex,endIndex)
        let peak = -100
        for (let i = 0; i < sliced.length; i++){
            const sample = sliced[i]
            if (sample > peak) {
                peak = sample
            }
        }
        return peak
    }
  },
  mounted() {
    changevalue.change_value(0)
  }
}
</script>

<style>
.chatmark{
    width: 200px; 
    height: 200px;
    border-radius: 100%;
    background-color: #ff0000;
    float: right;
    margin-top: 16%;
    margin-right: 28%;
    text-align: center;
    color: #fff;
    vertical-align: middle;
    position: relative;
    transition: 0.1s ease;
}

.chatmark:hover{
    cursor: pointer;
    transform: scale(1.2);
}

.chatmark:active{
    transform: scale(0.9);
}

.chatter {
    font-size: 32px;
    background-color: #000;
    color: #fff;
}

.hatuwa{
    position: absolute;
    left: 0;
    right: 0;
    margin-top: 55px;
    font-size: 59px;
}

</style>