import json
import sounddevice as sd
import vosk
import queue
import command
from skills import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

q = queue.Queue()
device = sd.default.device  #через cmd запустить команду sounddevice и посмотреть индекс используемого микрофона
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  #получаем частоту микрофона
model = vosk.Model('vosk')

def callback(indata, frames, time, status):
    '''
    Добавляет в очередь семплы из потока'''

    q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    trig = command.Name_AI.intersection(data.split())
    if not trig:
        return

    data.replace(list(trig)[0], '')
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    exec(answer + '()')


def main():
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(command.data_set.keys()))
    clf = LogisticRegression()
    clf.fit(vectors, list(command.data_set.values()))
    del command.data_set

    with sd.RawInputStream(samplerate=samplerate, blocksize=12000, device=device[0], dtype='int16', channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)
                print(data)


if __name__ == '__main__':
    main()
