import subprocess
import os
import shutil
from pydub import AudioSegment



def fromListToStr(list, _from, _till):
    str = ''
    for i in range(_from, _till):
        str = str + ' ' + list[i]
    str = str[1:]
    return str

def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold:
        trim_ms += chunk_size

    return trim_ms

def delet_silence_gap(sound):
    start_trim = detect_leading_silence(sound)
    end_trim = detect_leading_silence(sound.reverse())
    duration = len(sound)
    trimmed_sound = sound[start_trim:duration - end_trim]
    return trimmed_sound

def combine_2_wav_files(dir_1, dir_2, result_dir, line):
    try:
        s1 = AudioSegment.from_wav(dir_1)
        s2 = AudioSegment.from_wav(dir_2)
        sound1 = delet_silence_gap(s1)
        sound2 = delet_silence_gap(s2)
        combined_sounds = sound1 + sound2
        combined_sounds.export(result_dir, format="wav")
    except Exception as e:
        print('my Error: Concatenate wav file problem. 2 wav')
        print('Problem text:', '|' + line + '|')
        print('The error massage: ', str(e))
    #os.remove(dir_1)
    #os.remove(dir_2)

def combine_3_wav_files(dir_1, dir_2, dir_3, result_dir, line):
    try:
        s1 = AudioSegment.from_wav(dir_1)
        s2 = AudioSegment.from_wav(dir_2)
        s3 = AudioSegment.from_wav(dir_3)
        sound1 = delet_silence_gap(s1)
        sound2 = delet_silence_gap(s2)
        sound3 = delet_silence_gap(s3)
        combined_sounds = sound1 + sound2 + sound3
        combined_sounds.export(result_dir, format="wav")
    except Exception as e:
        print('my Error: Concatenate wav file problem. 3 wav')
        print('Problem text:', '|' + line + '|')
        print('The error massage: ', str(e))
    os.remove(dir_1)
    os.remove(dir_2)
    os.remove(dir_3)


def create_all_emph_options(new_path, audio_name, speaker):
    sentence = audio_name.split()
    emphasised_list = []
    for i, word in enumerate(sentence):  # i,line in enumerate(all_lines)
        before = fromListToStr(sentence, 0, i)
        emph = '%' + fromListToStr(sentence, i, i + 1) + '%'
        after = fromListToStr(sentence, i + 1, len(sentence))
        word_emph = before + emph + after

        # jar__name = speaker + '.jar'
        jar__name = 'FreeTTS_kevin_pitch95_rate_70_volume085.jar'
        print('calling jar ', i)

        tmp_file = new_path + '/' + 'tmp'
        if os.path.exists(tmp_file):
            shutil.rmtree(tmp_file)
        os.makedirs(tmp_file)

        # before:
        if before is not '':
            print('executed before')
            subprocess.call(['cd', jar_path, '&&', 'java', '-jar', jar__name, tmp_file, before], shell=True)
        # emph:
        print('this is the call:', 'cd', jar_path, '&&', 'java', '-jar', jar__name, tmp_file, emph)
        subprocess.call(['cd', jar_path, '&&', 'java', '-jar', jar__name, tmp_file, emph], shell=True)
        # after:
        if after is not '':
            subprocess.call(['cd', jar_path, '&&', 'java', '-jar', jar__name, tmp_file, after], shell=True)

        before_dir = tmp_file + '/' + before + ".wav"
        emph_dir = tmp_file + '/' + emph + ".wav"
        after_dir = tmp_file + '/' + after + ".wav"
        result_dir = new_path + '/' + word_emph + ".wav"
        try:
            # The FIRST word was emphasised.
            if before is '':
                combine_2_wav_files(emph_dir, after_dir, result_dir, word_emph)
            # The LAST word was emphasised.
            elif after is '':
                combine_2_wav_files(before_dir, emph_dir,result_dir, word_emph)
            # A middle word was emphasised.
            else:
                combine_3_wav_files(before_dir, emph_dir, after_dir, result_dir, word_emph) # new_path istead of afer 2

            # Remove inner file:
            shutil.rmtree(tmp_file)
        except:
            continue
        emphasised_list.append(new_path + '/' + word_emph)
    return emphasised_list


jar_path = r'C:/Users/akiva/OneDrive/Coding_Projects/final_project/netbeans_workspace/FreeTTS-master'
new_path = r'C:/Users/akiva/Desktop/algo'
audio_name = 'do something dont think just do it'
speaker = 'kevin'
ans = create_all_emph_options(new_path, audio_name, speaker)
print(ans)