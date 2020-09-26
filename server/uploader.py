from imagekitio import ImageKit
import json, random, string, time

# I use ImageKit for hosting images. However, you can use what you what. 
imagekit = ImageKit(
    private_key='',
    public_key='',
    url_endpoint = ''
    )

def UploadImage(img, status="", prot="off", password=""):
    if prot == "on":
        prot = True
    else:
        prot = False

    RESULT = imagekit.upload(
    file=open("images/" + img, "rb"),
    file_name= ".png",
    options={
        "response_fields": ["folder"],
        "folder": "imganon"
        }
    )

    # process data and return it to the user
    ikres = RESULT["response"]
    shareid = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for i in range(6))
    expire = int(time.time()) + 86400 * 7
    fileId = ikres["fileId"]
    imgurl = ikres["url"]
    # image metadata
    height = ikres["height"]
    width = ikres["width"]
    fileSize = ikres["size"]

    # save those item into an entries
    entry = {
        "fileId": fileId,
        "url": imgurl,
        "expire": expire,
        "height": height,
        "width": width,
        "size": fileSize,
        "status": status
        }
    if prot == True:
        entry['protected'] = True
        entry['password'] = password

    # then save the entries with the unique share id
    with open('imganon.json', 'r+') as iaf:
        try:
            iajson = json.load(iaf)
        except json.decoder.JSONDecodeError:
            iajson = {}
        iajson[shareid] = entry
        res = json.dumps(iajson, indent=2)
        iaf.seek(0)
        iaf.write(res)
    return shareid

def DeleteImg(fileId, shareId):
    with open('imganon.json', 'r') as rd:
        try:
            i = json.load(rd)
        except json.decoder.JSONDecodeError:
            return 'Entry Not Found.'
    res = i.pop(shareId, None)
    with open('imganon.json', 'w') as rf:
        res = json.dump(i, rf, indent=2)
    return imagekit.delete_file(fileId)