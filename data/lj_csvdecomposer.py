import csv
import os
import argparse
import io
import fnmatch
from tqdm import tqdm
import re


_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('mrs', 'misess'),
  ('mr', 'mister'),
  ('dr', 'doctor'),
  ('st', 'saint'),
  ('co', 'company'),
  ('jr', 'junior'),
  ('maj', 'major'),
  ('gen', 'general'),
  ('drs', 'doctors'),
  ('rev', 'reverend'),
  ('lt', 'lieutenant'),
  ('hon', 'honorable'),
  ('sgt', 'sergeant'),
  ('capt', 'captain'),
  ('esq', 'esquire'),
  ('ltd', 'limited'),
  ('col', 'colonel'),
  ('ft', 'fort'),
]]

def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def csv_decomposer(filename, wavpath):

    parser = argparse.ArgumentParser(description='Processes lj dataset.')
    parser.add_argument('--target_dir', default=filename, help='Path to save dataset')
    args = parser.parse_args()

    os.makedirs("lj/" + args.target_dir.split('.')[0] + "/")
    transcript_path = "lj/" + args.target_dir.split('.')[0] + "/" + '/txt/'
    os.makedirs(transcript_path)

    y = open(filename, 'r')
    rdr = csv.reader(y)

    manifest_path = 'lj_%s_manifest.csv' % args.target_dir.split('.')[0]

    for line in rdr:
        transcript = expand_abbreviations(line[4])
        new_line = re.sub('[^a-zA-Z \n\.]|\.', '', transcript).upper()
        # print (line[4])
        # print (new_line)
        temp_trans_path = transcript_path + line[2] + '.txt'
        temp_wav_path = wavpath + '/' + line[2] + '.wav'
        with io.FileIO(temp_trans_path, "w") as file:
            file.write(new_line.encode('utf-8'))
        with io.FileIO(manifest_path, "a") as file2:
            sample = os.path.abspath(temp_wav_path) + ',' + os.path.abspath(temp_trans_path) + '\n'
            file2.write(sample.encode('utf-8'))

    y.close()

# def create_manifest(data_path, tag):
#     manifest_path = '%s_manifest.csv' % tag
#     file_paths = []
#     wav_files = [os.path.join(dirpath, f)
#                  for dirpath, dirnames, files in os.walk(data_path)
#                  for f in fnmatch.filter(files, '*.wav')]
#     for file_path in tqdm(wav_files, total=len(wav_files)):
#         file_paths.append(file_path.strip())
#     print('\n')
#
#     with io.FileIO(manifest_path, "w") as file:
#         for wav_path in tqdm(file_paths, total=len(file_paths)):
#             transcript_path = wav_path.replace('/wav/', '/txt/').replace('.wav', '.txt')
#             sample = os.path.abspath(wav_path) + ',' + os.path.abspath(transcript_path) + '\n'
#             file.write(sample.encode('utf-8'))
#     print('\n')


if __name__ == '__main__':
    csv_decomposer("unsup_tr.csv", "lj/wavs/")
    csv_decomposer("unsup_va.csv", "lj/wavs/")
    csv_decomposer("all_te.csv", "lj/wavs/")
