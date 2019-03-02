import time
import requests
import subprocess
import getpass

pid = raw_input("Enter Product ID (lid in URL) : ")
phone = raw_input("Enter Phone Number : ")
password = getpass.getpass("Enter Password : ")

xua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36 " \
      "FKUA/website/41/website/Desktop "
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"

#pid = "LSTCHCFBEZHTKMXVYQZN0PFCC" #Out Of Stock
#pid = "LSTACCFAWQKDMREPNBRCBSZER" #In Stock


def logout():
    print("Logging You Out")
    url = "https://www.flipkart.com/api/2/user/logout"
    payload = str(time.time()).replace(".", "") + "0"
    headers = {
        'Origin': "https://www.flipkart.com",
        'AlexaToolbar-ALX_NS_PH': "AlexaToolbar/alx-4.0.3",
        'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
        'Accept-Encoding': "gzip, deflate, br",
        'Connection': "keep-alive",
        'Pragma': "no-cache",
        'X-user-agent': xua,
        'User-Agent': ua,
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Referer': "https://www.flipkart.com/",
        'DNT': "1",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, cookies=cookies, headers=headers)
    if response.status_code == 200:
        subprocess.call("rm captcha.jpg", shell=True)
        print("Logged Out Successfully")
    else:
        print("Error Logging Out")


def add_to_cart(pid):
    url = "https://www.flipkart.com/api/5/checkout"
    payload = "{\"cartRequest\":{\"cartContext\":{\"" + str(
        pid) + "\":{\"quantity\":1}}},\"checkoutType\":\"PHYSICAL\"}"
    headers = {
        'X-user-agent': xua,
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    print("Trying Adding to Cart")
    while True:
        response = requests.request("POST", url, data=payload, cookies=cookies, headers=headers)
        res = response.json()
        if res['STATUS_CODE'] == 200:
            print("Added to Cart Successfully")
            break
        if res['ERROR_CODE'] == 0:
            print("Currently Out Of Stock!")
            print("Retrying...")
        if res['ERROR_CODE'] == 429:
            print("API Error")
            print("Retrying...")


def login():
    global cookies
    print("Logging In")
    url = "https://www.flipkart.com/api/4/user/authenticate"
    payload = "{\"loginId\":\"+91" + str(phone) + "\",\"password\":\"" + str(password) + "\"}"
    headers = {
        'Pragma': "no-cache",
        'X-user-agent': xua,
        'Origin': "https://www.flipkart.com",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
        'User-Agent': ua,
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Referer': "https://www.flipkart.com/",
        'Cookie': "T=TI155137553506705890121826703635344841328671598429530214544753810704; gpv_pn=HomePage; gpv_pn_t=Homepage; AMCVS_17EB401053DAF4840A490D4C%40AdobeOrg=1; s_cc=true; AMCV_17EB401053DAF4840A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C17956%7CMCMID%7C91959474157950264714624597549432852589%7CMCAID%7CNONE%7CMCOPTOUT-1551382718s%7CNONE%7CMCAAMLH-1551980318%7C8%7CMCAAMB-1551980318%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI; S=d1t13PyUOPz8/Rj8/Xz8bPw4/PzZG4Vgoju/YzeDpujhY6sZQbGF9kzE0z5eddPLGYrPG1NiFrK7ta5z5azKll7WbRg==; SN=2.VI7DBD8D2460E640BAB11E40ABC3B2DAFB.SIBC1DB43149BB4FA088FEC3CFA1B9FB43.VS783652EDBA3E4173949AC02384BF998B.1551375560; s_sq=%5B%5BB%5D%5D",
        'Connection': "keep-alive",
        'DNT': "1",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 400:
        print("Incorrect Credentials")
        exit()
    cookies = response.cookies


def get_payment_token():
    print("Getting Payment Info")
    url = "https://www.flipkart.com/api/3/checkout/paymentToken"
    headers = {
        'X-user-agent': xua,
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, data="", cookies=cookies, headers=headers)
    res = response.json()
    token = res['RESPONSE']['getPaymentToken']['token']
    return token


def get_captcha():
    captcha = {}
    print("Loading Captcha")
    url = "https://payments.flipkart.com/fkpay/api/v3/payments/captcha/" + str(token)
    querystring = {"token": token}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", url, data="", headers=headers, params=querystring)
    res = response.json()
    captcha['id'] = res['captcha_image']['id']
    cap_str = res['captcha_image']['image']
    subprocess.call(
        "echo \"" + str(cap_str) + "\" >captcha; base64 -d captcha >captcha.jpg; rm captcha; display captcha.jpg&",
        shell=True)
    captcha['text'] = str(raw_input("Enter Captcha Text : "))
    return captcha


def verify_captcha(cap, token):
    print("Verifying Captcha")
    url = "https://payments.flipkart.com/fkpay/api/v3/payments/pay"
    querystring = {"token": token, "instrument": "COD"}
    payload = "{\"payment_instrument\":\"COD\",\"token\":\"" \
              + token \
              + "\",\"captcha_text\":{\"id\":\"" \
              + cap['id'] \
              + "\",\"text\":\"" \
              + cap['text'] \
              + "\"}}"
    headers = {
        'Referer': "https://www.flipkart.com/checkout/init",
        'Origin': "https://www.flipkart.com",
        'DNT': "1",
        'User-Agent': ua,
        'x-device-source': "web",
        'x-client-trace-id': "cjso3m4g000033169nqf3h3h2",
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    res = response.json()

    if res['response_status'] == 'FAILED':
        print("Incorrect Captcha!")
        return verify_captcha(get_captcha(), token)
    else:
        print("Captcha Verified Successfully")
        return res


def process_order(response):
    print("Processing Order")
    url = "https://www.flipkart.com/api/3/checkout/pgResponse/desktop"
    payload = response['primary_action']['parameters']
    headers = {
        'Connection': "keep-alive",
        'Pragma': "no-cache",
        'Cache-Control': "no-cache",
        'Origin': "https://www.flipkart.com",
        'Upgrade-Insecure-Requests': "1",
        'DNT': "1",
        'Content-Type': "application/x-www-form-urlencoded",
        'User-Agent': ua,
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Referer': "https://www.flipkart.com/checkout/init",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
        'cache-control': "no-cache"
    }

    print("Generating Response")
    response = requests.request("POST", url, data=payload, cookies=cookies, headers=headers)
    if response.status_code == 200:
        print(
            "Order Placed Successfully! Check \"Orders\" section of your account after a few minutes to confirm"
        )


login()
add_to_cart(pid)
token = get_payment_token()
process_order(verify_captcha(get_captcha(), token))
logout()
print("Exiting")
