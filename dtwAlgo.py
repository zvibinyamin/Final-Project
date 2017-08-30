from CreateAllEmphOptions import *
from fastdtw import fastdtw

from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
from scipy.spatial.distance import euclidean
from os import listdir
from operator import itemgetter
import ntpath



def get_audio_sentence(audio_file_path):
    head, tail = ntpath.split(audio_file_path)
    try:
     return tail[:-4]
    except:
     print('trying to get audio sentence in dtwAlgo. The input file is NOT .wav')


def algo(input_file_name):     # input_file_name -> must include dir + name.

    all_options_path = r'/home/akiva/Documents/Do_not_delete/all_options_emphsis'
    audio_sentence = get_audio_sentence(input_file_name)
    print('audio_sentence = ', audio_sentence)
    # creates all the emphasis options:
    a = create_all_emph_options(all_options_path, audio_sentence)
    print('a=', a)
    # dtw:
    frames = 50  # 20
    first_frame = 30
    mfccs = 20  # upto 26!
    test_frac = 0.2

    # input_file_name = './DTW single file/see%the%bombers fly up.wav'
    # Extract MFCCs from input wav file
    print(input_file_name)
    (rate, sig) = wav.read(input_file_name)
    mfcc_feat = mfcc(sig, rate)
    curr = logfbank(sig, rate)
    input_file_data = curr[first_frame:(first_frame + frames), 0:mfccs] / 20

    # Extract MFCCs from each permutation of 1 emphasized word
    file_names = []
    distances = []
    #for file_name in listdir('./DTW single file'):
    for file_name in listdir(all_options_path):
        print(file_name)
        file_names.append(file_name)
        #(rate, sig) = wav.read("./DTW single file/" + file_name)
        (rate, sig) = wav.read(all_options_path + "/" + file_name)
        mfcc_feat = mfcc(sig, rate)
        curr = logfbank(sig, rate)
        current_file_data = curr[first_frame:(first_frame + frames), 0:mfccs] / 20
        distance, path = fastdtw(input_file_data, current_file_data, dist=euclidean)
        distances.append(distance)

    print(file_names)
    print(distances)
    min_distance_index = min(enumerate(distances), key=itemgetter(1))[0]
    print(min_distance_index)

    s = file_names[min_distance_index]
    c = '%'
    start_end_indexes = [pos for pos, char in enumerate(s) if char == c]
    print(start_end_indexes)
    answer = file_names[min_distance_index][start_end_indexes[0] + 1:start_end_indexes[1]]
    return answer
'''
all_options_path = r'/home/akiva/Documents/Do_not_delete/all_options_emphsis'
input_file_name = r'/home/akiva/Desktop'
audio_sentence = 'see the bombers fly up'
'''

#algo('/home/akiva/Desktop/see the bombers fly up.wav')
