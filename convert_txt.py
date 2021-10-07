import pandas as pd

read_file = pd.read_csv(r'C:\Users\ASUS\Documents\deepspeech\mic_vad_streaming\output.txt')
read_file.to_csv(r'C:\Users\ASUS\Documents\deepspeech\mic_vad_streaming\output.csv', index=None)
