from Parameters import *


normal_path = dest_path + '/normal'
emphasis_path = dest_path + '/emphasised'
os.makedirs(normal_path)
os.makedirs(emphasis_path)


file = open(db_path, 'r')
all_lines = file.read().splitlines()

for line in all_lines:  # [:100]
    if line[:-1] is '\n':
        line = line[:-1]
    emph_line = '%' + line + '%'
    # print('line: ','|'+line+'|')
    # print('emph_line: ', '|' + emph_line + '|')
    sub_emph_path = emphasis_path + '/' + line
    os.makedirs(sub_emph_path)

    subprocess.call(['cd', jar_path, '&&', 'java','-jar', jar_name, normal_path, line], shell=True)

    subprocess.call(['cd', jar_path, '&&', 'java','-jar', jar_name,sub_emph_path, emph_line], shell=True)

file.close()
