'''
PLEASE REFER TO ./GUIDE.TXT FOR MORE INFO
'''

# builtins
import os 
import shutil
import time
import json
import sys

# external
import requests

# file imports
import tools.download as download
import tools.extract as extract

# ---------------------------------------------
url = 'https://api.github.com/repos/SketchedDoughnut/SDA-FOMX/releases/latest'
wDir = os.path.dirname(os.path.abspath(__file__))
above_everything_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(wDir))))

def load_current_label(dir: str) -> str:
    path = os.path.join(dir, 'version.json')
    f = open(path, 'r')
    current = str(json.load(f))
    f.close()
    return current

def get_release_info(local_url: str) -> list:
    data = requests.get(local_url).json()
    data = str(data['body'])
    data = data.split()
    id = data[0]
    data.remove(id)
    n_word = ''
    for word in data: # re-assemble words with one-spacing
        n_word += word
        n_word += " "
    return [id, n_word]


current_label = load_current_label(wDir)
latest_label, content = get_release_info(url)
print('---------------')
print('FOMX: DATA')
print('    - current commit label:', current_label)
print('    - commit label of newest release:', latest_label)
print('FOMX: comparing versions...')
if current_label != latest_label:
    print('FOMX: versions do not match.')
    print('---------------')
    if input('FOMX: do you want to see the info for this update? (y/n): ').lower() == 'y':
        print('---------------')
        print('Info:')
        print('-', content)
        print('---------------')
    else:
        print('FOMX: skipping...')
        print('---------------')
    if input('Download this update? This is highly recommended (y/n): ').lower() == 'y':
        pass
    else:
        print('---------------')
        print('FOMX: exiting...')
        time.sleep(1)
        sys.exit()
print('---------------')
# vars
tmp_path = os.path.join(wDir, 'tmp')
zip_path = f'{tmp_path}/latest_release.zip'
copy_location = f'{tmp_path}/SketchedDoughnut-SDA-FOMX-{latest_label}/data'
bounds_json = f'{copy_location}/bounds.json'




print('Attempting to delete previous tmp...')
try:
    shutil.rmtree(tmp_path)
except:
    pass
os.mkdir(tmp_path)

print('FOMX: downloading .zip...')
download.download_latest_release(url, zip_path)
time.sleep(0.5)

print('FOMX: extracting...')
extract.extract(zip_path, tmp_path)

print('FOMX: reading bounds file...')
f = open(bounds_json, 'r')
bounds = json.load(f)
f.close()
time.sleep(0.5)

print('FOMX: bounds description:')
print('-', bounds['description'])
print('FOMX: files affected:')
print('-', bounds['file_details'])

print('FOMX: formatting data list...')
n_list = []
for path, file in zip(bounds['file_paths'], bounds['file_details']):
    n_list.append([file[1], os.path.join(copy_location, file[0]), os.path.join(os.path.join(above_everything_dir, path), file[0]), file[0]])

print('---------------')
print('FOMX: verifying files exist...')
for data in n_list:
    print('- verifying:', data)
    if not os.path.exists(data[1]): # if destination exists
        exit()
    if not os.path.exists(data[2]): # if copy file exists
        exit()
print('FOMX: all files exist.')
print('---------------')

print('FOMX: Copying over code...')
time.sleep(0.5)
for file in n_list:
    mode = file[0]
    if mode == 'normal':
        op = 'r'
        wr = 'w'
    elif mode == 'binary':
        op = 'rb'
        wr = 'wb'
    source = file[1]
    dest = file[2]
    f = open(source, op)
    content = f.read()
    f.close()
    f = open(dest, wr)
    f.write(content)
    f.close()
    print(f'- wrote content from "{source}" to "{dest}"')

print('---------------')
print('FOMX: cleaning up tmp...')
time.sleep(0.25)
shutil.rmtree(tmp_path)

print('FOMX: updating local version...')
f = open(os.path.join(wDir, 'version.json'), 'w')
json.dump(latest_label, f)
f.close()
time.sleep(0.25)

print('---------------')
print('FOMX process is done, Enter anything to continue on to launch: ')
input('--> ')
sys.exit()