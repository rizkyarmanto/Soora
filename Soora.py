# Deepspeech API
import sys
from deepspeech import Model, Stream
import numpy as np
import os
import wave
import pyaudio
import time
import subprocess
import psycopg2
import glob
import json

from IPython.display import Audio
from IPython.display import clear_output

model_file_path = 'deepspeech-0.9.3-models.pbmm'
lm_file_path = 'deepspeech-0.9.3-models.scorer'
beam_width = 100
lm_alpha = 0.93
lm_beta = 1.18

model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)

model.setScorerAlphaBeta(lm_alpha, lm_beta)
model.setBeamWidth(beam_width)

def read_wav_file(filename):
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)
        print('Rate:',rate)
        print('Frames:',frames)
        print('Buffer Len:', len(buffer))

    return buffer, rate

def transcribe_batch(audio_file):
    DB_host = 'localhost'
    DB_name = 'uploadfile'
    DB_user = 'postgres'
    DB_password = '1234'
    save_file = 'C:/Users/ASUS/Documents/deepspeech/mic_vad_streaming/output/Output_Deepspeech'
    file_name = 'woman.csv'
    file_name_json = 'woman.json'
    conne = psycopg2.connect(host=DB_host, dbname=DB_name, user=DB_user, password=DB_password)
    cur = conne.cursor()
    buffer, rate = read_wav_file(audio_file)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    text = model.stt(data16)
    print(text)
    upload_to = os.path.join(save_file,file_name)
    upload_to_json = os.path.join(save_file, file_name_json)
    with open(upload_to, 'w') as out_file:
        out_file.writelines(text)
    with open(upload_to_json, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(text, indent=4))
    for fname in glob.glob('C:/Users/ASUS/Documents/deepspeech/mic_vad_streaming/output/Output_Deepspeech/*.csv'):
        with open(fname) as f:
            cur.copy_from(f, "users", sep=",")
            conne.commit()
            f.close()
    return text
  
Audio('Output_Deepspeech/woman.wav')   
transcribe_batch('Output_Deepspeech/woman.wav')
#subprocess.run(['python','client.py','--model','deepspeech-0.9.3-models.pbmm','--audio','woman.wav','--json'])


# Streaming API
context = model.createStream()

def transcribe_streaming(audio_file):
    buffer, rate = read_wav_file(audio_file)
    offset = 0
    batch_size = 8196
    text = ""

    while offset < len(buffer):
        end_offset = offset + batch_size
        chunck  = buffer[offset:end_offset]
        data16 = np.frombuffer(chunck, dtype=np.int16)

        Stream.feedAudioContent(data16)
        text = Stream.intermediateDecode()
        #clear_output(wait=True)
        print(text)
        offset = end_offset
    return True

#transcribe_streaming('audio/woman1_wb.wav')


