import os
import sys

orig_filename = sys.argv[1]
split_dict = {}

print("first step: split {}".format(orig_filename))
os.system('tar cvzf - ./{} | split -d -b 30m - {}_part'.format(orig_filename, orig_filename))
split_results = os.popen('ls $(find ./ -name "{}_part*")'.format(orig_filename)).read().split()

hash_file = open("split_file_hash", 'w')
for split_file in split_results:
    if split_file == '':
        split_results.remove(split_file)
    split_file_hash = os.popen('md5sum {}'.format(split_file)).read().split()[0]
    hash_file.write("{} {}\n".format(split_file, split_file_hash))
hash_file.close()

print("second step: upload over ffsend")
for split_file in split_results:
    os.system('docker run --rm -i -v $(pwd):/data timvisee/ffsend upload {} 2>&1 | tee -a ffsend'.format(split_file))
pass
