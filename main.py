import json
import sounddevice as sd
import vosk
import queue
import command
from skills import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

Name_AI = {'пингвин'}  # имя ассистента

q = queue.Queue()
device = sd.default.device     # через cmd запустить команду sounddevice и посмотреть индекс используемого микрофона
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])    # получаем частоту микрофона
model = vosk.Model('vosk')    # подгружаем скаченную модель vosk


def callback(indata, frames, time, status):
    # добавляет в очередь семплы из потока
    q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    trig = Name_AI.intersection(data.split())    # ищет имя в потоке разделив его по словам
    if not trig:
        return

    data.replace(list(trig)[0], '')
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    exec(answer + '()')   # выполнение функции модуля skills


def main():
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(command.data_set.keys()))      # превращаем ключи data_set в векторы для последующего обучения
    clf = LogisticRegression()
    clf.fit(vectors, list(command.data_set.values()))
    del command.data_set   # чистим память

    with sd.RawInputStream(samplerate=samplerate, blocksize=12000, device=device[0], dtype='int16', channels=1, callback=callback):    # в цикле слушаем микрофон и прогоняем через vosk
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']   # достаем текст из json
                recognize(data, vectorizer, clf)
                # print(data)   #  можно посмотреть как распозноет модель


if __name__ == '__main__':
    main()
