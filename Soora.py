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

from client import *
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

def metadata_json_output(metadata):
    json_result = dict()
    json_result["transcripts"] = [{
        "confidence": transcript.confidence,
        "words": transcribe_batch('woman.wav'),
    } for transcript in metadata.transcripts]
    return json.dumps(json_result, indent=2)

def transcribe_batch(audio_file):
    DB_host = 'localhost'
    DB_name = 'uploadfile'
    DB_user = 'postgres'
    DB_password = '1234'    
    conn = psycopg2.connect(host=DB_host, dbname=DB_name, user=DB_user, password=DB_password)
    cur = conn.cursor()
    buffer, rate = read_wav_file(audio_file)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    text = model.stt(data16)
    print(text)
    with open('woman.csv', 'w') as out_file:
        out_file.writelines(text)
    with open(r'woman.json', 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(text, indent=4))
    f = open(r'C:\Users\ASUS\Documents\deepspeech\mic_vad_streaming\output\Output_Deepspeech\woman.csv') #File path
    cur.copy_from(f, "users", sep=",")
    conn.commit()
    f.close()
    return text
  
Audio('audio/woman1_wb.wav')   
transcribe_batch('audio/woman1_wb.wav')
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


