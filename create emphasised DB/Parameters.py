import subprocess
import os
import random
from pydub import AudioSegment
from pydub.silence import split_on_silence ###

#----------------- Parameters -------------------------
dest_path = r'C:/Users/akiva/Desktop/final project - creating db/database - sub sentence'
db_path = r'C:/Users/akiva/Desktop/final project - creating db/txt files/db.txt'
jar_path = r'C:/Users/akiva/OneDrive/Coding_Projects/final_project/netbeans_workspace/FreeTTS-master'
jar_name = 'FreeTTS_kevin_mean2.5.jar'
#-------------------------------------------------------

