from requests import post
from time     import sleep
from json     import load


class Funcaptcha:
    key = load(open("./data/config.json"))['captcha_key']

    def getKey(uaid, proxy=None) -> str:
        req = post("http://2captcha.com/in.php", params = {
            "key": Funcaptcha.key,
            "proxy": proxy if proxy else "",
            "proxytype": "HTTP",
            "method": "funcaptcha",
            "publickey": "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
            "surl": "https://client-api.arkoselabs.com",
            "pageurl": "https://signup.live.com/signup?ne=1&lic=1&uaid=" + str(uaid)
        })

        if "OK|" in req.text:
            captcha_id = req.text.split("|")[1]
            print("\33[90mCAPTCHA ID=" + captcha_id + "\033[0m")

            sleep(10)

            while True:
                sleep(0.3)
                task = post("http://2captcha.com/res.php", params = {
                    "key": Funcaptcha.key,
                    "action": "get",
                    "id": captcha_id
                })
                
                if "OK|" in task.text: 
                    token = task.text.replace("OK|", "")
                    print("\33[90mCAPTCHA TOKEN=" + token + "\033[0m")
                    return token

                if task.text == "ERROR_CAPTCHA_UNSOLVABLE":
                    print("\33[90mERROR=ERROR_CAPTCHA_UNSOLVABLE!\033[0m")
                    return None
        
        return None