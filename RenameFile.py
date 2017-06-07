import os

dir = r'C:/Users/akiva/Desktop/database - Copy/word emphasis'

for speaker in os.listdir(dir):
    sub_dir = dir + '/' + speaker
    for emph in os.listdir(sub_dir):
        audio_dir = sub_dir + '/' + emph
        for audio in os.listdir(audio_dir):
            old = audio_dir + '/' + audio
            new = audio_dir + '/' + speaker[:7] + audio
            os.rename(old, new)



