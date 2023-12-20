import gzip
import lzma
import time

filename = open('txt.txt', "r").read()

filename = filename.encode()
content = filename

cur_time = time.time()
with gzip.open('txt.gz', 'wb') as f:
    f.write(content)
print(time.time() - cur_time, 'gzip')

cur_time = time.time()
with lzma.open("file.xz", "w") as f:
    f.write(content)
print(time.time() - cur_time, 'lzma')