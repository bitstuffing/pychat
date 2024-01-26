from core.browser import Browser
import requests

class TempEmail(Browser):

    def __init__(self):
        #
        self.session = requests.Session()
        self.headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://temp-mail.org/',
            'Origin': 'https://temp-mail.org',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers'
        }
        response = self.session.post(url = 'https://web2.temp-mail.org/mailbox', headers = self.headers)
        jsonResponse = response.json()
        self.email = jsonResponse['mailbox'] # email
        self.token = jsonResponse['token'] # jwt

    def getEmail(self):
        return self.email

    def getEmails(self):
        #curl 'https://web2.temp-mail.org/messages' --compressed -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0' -H 'Accept: */*' -H 'Accept-Language: es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://temp-mail.org/' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiMzBiNDVkMmQwODRiNDA0OGE3MTZlYWNiNGZlNDZjYWUiLCJtYWlsYm94IjoibGFkZWxhMjQzNUBiaXRvZmVlLmNvbSIsImlhdCI6MTcwNjI5ODMxNn0.gsJCPMu_VmHn6XGI9zVeCXOxh4VFxZtd6tFlxBaHXGo' -H 'Origin: https://temp-mail.org' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' -H 'TE: trailers'
        headers = self.headers
        headers['Authorization'] = f'Bearer {self.token}'
        response = self.session.get(url = 'https://web2.temp-mail.org/messages', headers = self.headers)
        jsonResponse = response.json()
        return jsonResponse['messages']