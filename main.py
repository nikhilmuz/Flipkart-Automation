import time
import requests
import subprocess

#pid = raw_input ("Enter Product ID : ")
#cookie = raw_input ("Enter Cookie header as per HTTP 1.1 : ")

pid = "LSTMOBEQ98THNGR4FD5V3OUHB"
cookie = "T=TI155132592534384785252330586872264666854936836547782723228029338613; AMCVS_17EB401053DAF4840A490D4C%40AdobeOrg=1; s_cc=true; AMCV_17EB401053DAF4840A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C17956%7CMCMID%7C87452963148642232941527437008171924540%7CMCAAMLH-1551930706%7C3%7CMCAAMB-1551930706%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1551333107s%7CNONE%7CMCAID%7CNONE; SN=2.VI704041CD18FA4F2AB8C43C8975345092.SIF6B8E8EFA4284B04B73D7D626E424C78.VS9A187847C6654F4E9CC5BAF06FBB14EA.1551326035; gpv_pn=Checkout%3ASummary; gpv_pn_t=Checkout; S=d1t18Px9nDT8VPz8/Fz8SPy0/fEGZM8ZwpNPwzjIGRKGj1Wq/TN/JTEAeXM4N385jnBq9xM5Olu8Ms2mKg8AZUrdwfw==; s_sq=flipkart-prd%3D%2526pid%253DCheckout%25253ASummary%2526pidt%253D1%2526oid%253Dfunction%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSUBMIT"

url = "https://www.flipkart.com/api/5/checkout"
payload = "{\"cartRequest\":{\"cartContext\":{\""+str(pid)+"\":{\"quantity\":1}}},\"checkoutType\":\"PHYSICAL\"}"
headers = {
    'Cookie': str(cookie),
    'X-user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36 FKUA/website/41/website/Desktop",
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }

while True:
	response = requests.request("POST", url, data=payload, headers=headers)
	res = response.json()
        print(res['STATUS_CODE'])
	if res['STATUS_CODE']==200:
		break
	print(res['ERROR_CODE'])
       	if res['ERROR_CODE']==429:
       		print("API Error")
		#time.sleep(5)

url = "https://www.flipkart.com/api/3/checkout/paymentToken"
headers = {
    'Cookie': str(cookie),
    'X-user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36 FKUA/website/41/website/Desktop",
    'cache-control': "no-cache"
    }
response = requests.request("GET", url, data="", headers=headers)
res = response.json()
token = res['RESPONSE']['getPaymentToken']['token']

url = "https://payments.flipkart.com/fkpay/api/v3/payments/captcha/"+str(token)
querystring = {"token":token}
headers = {'cache-control': "no-cache"}
response = requests.request("GET", url, data="", headers=headers, params=querystring)
res = response.json()
cap_id = res['captcha_image']['id']
cap_str = res['captcha_image']['image']
subprocess.call("echo \""+str(cap_str)+"\" >captcha; base64 -d captcha >captcha.jpg; rm captcha; display captcha.jpg&", shell=True)
captcha = raw_input("captcha?")

url = "https://payments.flipkart.com/fkpay/api/v3/payments/pay"
querystring = {"token":token,"instrument":"COD"}
payload = "{\"payment_instrument\":\"COD\",\"token\":\""+token+"\",\"captcha_text\":{\"id\":\""+cap_id+"\",\"text\":\""+str(captcha)+"\"}}"
headers = {
    'Referer': "https://www.flipkart.com/checkout/init?otracker=hp_omu_Food%2BEssentials%2B%2526%2BNutrition%2B_1_0TNRTS53M7UY_1",
    'Origin': "https://www.flipkart.com",
    'DNT': "1",
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    'x-device-source': "web",
    'x-client-trace-id': "cjso3m4g000033169nqf3h3h2",
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
res = response.json()

url = "https://www.flipkart.com/api/3/checkout/pgResponse/desktop"
payload = res['primary_action']['parameters']
headers = {
    'Connection': "keep-alive",
    'Pragma': "no-cache",
    'Cache-Control': "no-cache",
    'Origin': "https://www.flipkart.com",
    'Upgrade-Insecure-Requests': "1",
    'DNT': "1",
    'Content-Type': "application/x-www-form-urlencoded",
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Referer': "https://www.flipkart.com/checkout/init",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
    'Cookie': str(cookie),
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
