# Deepspeech API
import sys
from deepspeech import Model, Stream
import numpy as np
import os
import wave
import pyaudio
import time

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
    buffer, rate = read_wav_file(audio_file)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    text = model.stt(data16)
    print(text)
    return text

Audio('audio/woman1_wb.wav')   
transcribe_batch('audio/woman1_wb.wav')

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
        text = Stream.intermediateDecodeWithMetadata()
        #clear_output(wait=True)
        print(text)
        offset = end_offset
    return True

#transcribe_streaming('audio/woman1_wb.wav')


