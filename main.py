import json
import sounddevice as sd
import vosk
import queue

q = queue.Queue()
device = sd.default.device     # <--- по умолчанию
                                #или -> sd.default.device = 1, 3, python -m sounddevice просмотр
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  #получаем частоту микрофона

model = vosk.Model('vosk')

def callback(indata, frames, time, status):
    '''
    Добавляет в очередь семплы из потока.
    вызывается каждый раз при наполнении blocksize
    в sd.RawInputStream'''

    q.put(bytes(indata))
with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                       channels=1, callback=callback):

    rec = vosk.KaldiRecognizer(model, samplerate)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            data = json.loads(rec.Result())['text']
            print(data)
