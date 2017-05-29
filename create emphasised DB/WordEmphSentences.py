from Parameters import *

normal_path = dest_path + '/normal'
emphasis_path = dest_path + '/emphasised'
os.makedirs(normal_path)
os.makedirs(emphasis_path)


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

def combine_2_wav_files(dir_1, dir_2):
    s1 = AudioSegment.from_wav(dir_1)
    s2 = AudioSegment.from_wav(dir_2)
    sound1 = delet_silence_gap(s1)
    sound2 = delet_silence_gap(s2)
    combined_sounds = sound1 + sound2
    os.remove(dir_1)
    os.remove(dir_2)
    combined_sounds.export(result_dir, format="wav")

def combine_3_wav_files(dir_1, dir_2, dir_3):
    s1 = AudioSegment.from_wav(dir_1)
    s2 = AudioSegment.from_wav(dir_2)
    s3 = AudioSegment.from_wav(dir_3)
    sound1 = delet_silence_gap(s1)
    sound2 = delet_silence_gap(s2)
    sound3 = delet_silence_gap(s3)
    combined_sounds = sound1 + sound2 + sound3
    os.remove(dir_1)
    os.remove(dir_2)
    os.remove(dir_3)
    combined_sounds.export(result_dir, format="wav")



db_file = open(db_path, 'r')

all_lines = db_file.read().splitlines()

for i,line in enumerate(all_lines):  # [:100]

    # Get rid of '\n' at the end of the line:
    if line[:-1] is '\n':
        line = line[:-1]
    sen = line.split()

    # Create random emphasised word:
    rand_split = random.randint(0,len(sen)-1)
    before = fromListToStr(sen, 0, rand_split)
    emph = '%' + fromListToStr(sen, rand_split, rand_split + 1) + '%'
    after = fromListToStr(sen, rand_split + 1, len(sen))

    # Set directory for emphasised sentence:
    sub_emph_path = emphasis_path + '/' + line
    os.makedirs(sub_emph_path)

    # 1) Sentence WITHOUT emphasised words:
    subprocess.call(['cd', jar_path, '&&', 'java', '-jar', jar_name, normal_path, line], shell=True)
    # 2) Sentence WITH emphasised word:
    # 2.1) before emphasised word:
    if before is not '':
        subprocess.call(['cd', jar_path, '&&', 'java', '-jar', jar_name, sub_emph_path, before], shell=True)
    # 2.2) emphasised word:
    subprocess.call(['cd', jar_path, '&&', 'java', '-jar', jar_name, sub_emph_path, emph], shell=True)
    # 2.3) after emphasised word:
    if after is not '':
        subprocess.call(['cd', jar_path, '&&', 'java', '-jar', jar_name, sub_emph_path, after], shell=True)

    # Concatenate the 3 separate wav files into 1:

    before_dir = sub_emph_path + '/' + before + ".wav"
    emph_dir = sub_emph_path + '/' + emph + ".wav"
    after_dir = sub_emph_path + '/' + after + ".wav"
    result_dir = sub_emph_path + '/' + line + ".wav"

    # The FIRST word was emphasised.
    if before is '':
        combine_2_wav_files(emph_dir, after_dir)
    # The LAST word was emphasised.
    elif after is '':
        combine_2_wav_files(before_dir, emph_dir)
    # A middle word was emphasised.
    else:
        combine_3_wav_files(before_dir, emph_dir, after_dir)

db_file.close()

