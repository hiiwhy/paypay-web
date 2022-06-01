import requests
from requests_html import HTMLSession
import json

username = '' 
password = ''
client_uuid = ''
code = input('PayPay URL > ').split('https://pay.paypay.ne.jp/')[-1]
passcode = input('passcode > ')
session = HTMLSession()

r = (f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={code}&client_uuid=")
Pa = session.get(r)
r = Pa.html.full_text

if json.loads(r)["header"]["resultCode"] == "S0000":
    orderId = json.loads(r)["payload"]["pendingP2PInfo"]["orderId"]
    requestId  = json.loads(r)["payload"]["message"]["data"]["requestId"]
    amount = json.loads(r)["payload"]["pendingP2PInfo"]["amount"]

    headers = {
        'referer': 'https://www.paypay.ne.jp/app/account/sign-in?redirect=%2Fapp%2Fp2p%2F13k9FJrd%3Fpid%3DSMS%26link_key%3D13k9FJrd',
        'accept-language': 'ja',
        }

    json_data = {
        'scope': 'SIGN_IN',
        'client_uuid': client_uuid,
        'grant_type': 'password',
        'username': username,
        'password': password,
        'add_otp_prefix': True,
        'language': 'ja',
        
        }
    r = requests.post('https://www.paypay.ne.jp/app/v1/oauth/token', headers=headers, json=json_data)
    token = json.loads(r.text)["access_token"]
    headers = {'cookie':  f'token={token}',}

    json_data = {
        'requestId': requestId ,
        'orderId': orderId,
        'verificationCode': code,
        'requestAt': '2300-02-21T12:45:29Z',
        'passcode': passcode,
        }

    response = requests.post('https://www.paypay.ne.jp/app/v2/p2p-api/acceptP2PSendMoneyLink', headers=headers,json=json_data)