import re
import os

download_links_file = open("ffsend")
for download_link in download_links_file:
    m = re.search('https://send.firefox.com/download(\S*)', download_link)
    if m:
        ffsend_link = 'https://send.firefox.com/download'+m.group(1)
        os.system(
            'docker run --rm -i -v $(pwd):/data timvisee/ffsend download {} 2>&1'.format(ffsend_link))

downloaded_files = os.popen('ls $(find ./ -name "*_part*")').read().split()
hash_file = open("downloaded_files_hash", 'w')
for download_file in downloaded_files:
    if download_file == '':
        downloaded_files.remove(download_file)
    download_file_hash = os.popen('md5sum {}'.format(download_file)).read().split()[0]
    hash_file.write("{} {}\n".format(download_file, download_file_hash))
hash_file.close()
