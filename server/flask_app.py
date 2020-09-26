from flask import Flask, redirect, request, render_template, session
import , os, datetime, time, json, random, string
import uploader as iau

@app.route('/imganon/upload', methods=["POST"])
def ImgAnonSubmission():
    image = request.files['img']
    image.save("images/" + image.filename)
    status = request.form.get('status')
    protected = request.form.get('protected')
    password = request.form.get('password')
    if len(password) > 0 and protected == "on":
        res = iau.UploadImage(image.filename, status, protected, password)
    else:
        res = iau.UploadImage(image.filename, status)
    os.remove('images/' + image.filename)
    return Uploaded(res)

@app.route('/imganon/delete/<shareid>', methods=["POST"])
def DeleteImg(shareid):
    fileId = request.form.get('fileId')
    iau.DeleteImg(fileId, shareid)
    return redirect("")

def Uploaded(shareid):
    with open('imganon.json', 'r') as iaj:
        variety = json.load(iaj)[shareid]
    # assign var manually
    imgurl = variety["url"]
    status = variety["status"]
    fileId = variety["fileId"]
    expire = datetime.datetime.fromtimestamp(int(variety["expire"])).strftime('%Y-%m-%d %H:%M:%S')
    height = variety["height"]
    width = variety["width"]
    filesize = variety["size"]
    return render_template('uploaded.html', **locals())

@app.route('/imganon/view/<shareid>', methods=["POST", "GET"])
def ShowImage(shareid):
    with open('imganon.json', 'r') as iaj:
        variety = json.load(iaj)[shareid]
        # assign var manually
    imgurl = variety["url"]
    status = variety["status"]
    expire = datetime.datetime.fromtimestamp(int(variety["expire"])).strftime('%Y-%m-%d %H:%M:%S')
    height = variety["height"]
    width = variety["width"]
    filesize = variety["size"]
    try:
        protected = variety["protected"]
        password = variety["password"]
    except Exception: # does not have password
        protected = False
    if protected == True:
        session["password"] = request.form.get('password')
        if "password" in session:
            session.permanent = True
            if session["password"] == password:
                thisView = render_template('view.html', **locals())
            else:
                flash('Incorrect password, please try again.')
                thisView = render_template('prompt.html', shareid=shareid)
        else:
            thisView = render_template('prompt.html', shareid=shareid)
    else:
        thisView = render_template('view.html', **locals())
    return thisView
    
app.run()