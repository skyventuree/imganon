# Please execute this with a scheduler (like cron)

import json, pathlib, time
from imagekitio import ImageKit

imagekit = ImageKit(
    private_key='',
    public_key='',
    url_endpoint = ''
    )
log = ""
cleared = 0
clrdentries = []
res = {}

path = pathlib.Path(__file__).parent.absolute()
with open(f'{path}/imganon.json', 'r') as rd:
    try:
        iaj = json.load(rd)
        for i in iaj.copy():
            if time.time() >= int(iaj[i]["expire"]):
                clrdentries.append(i)
                cleared += 1
        for j in clrdentries:
            imagekit.delete_file(iaj[j]["fileId"])
            del iaj[j]
        log = f'Cleared and deleted {cleared} entri(es): {clrdentries}'
    except json.decoder.JSONDecodeError:
        log = 'No entry found/json is broken.'
with open(f'{path}/imganon.json', 'w+') as rf:
    json.dump(iaj, rf, indent=2)
with open(f'{path}/history', 'a+') as history:
    clock = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    history.write(f'[{clock}] {log}\n')