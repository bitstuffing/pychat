import requests

class TempEmail:
    def __init__(self):
        self.email = None
        self.token = None
        self.messages = None  # Nuevo atributo para almacenar mensajes
        self._base_url = 'https://api.internal.temp-mail.io/api/v3'
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://temp-mail.io/',
            'Origin': 'https://temp-mail.io',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-GPC': '1',
            'TE': 'trailers'
        }
        self.fetch_new_email()

    def getEmail(self):
        return self.email

    def getEmails(self):
        self.check_inbox()
        return self.messages       

    def fetch_new_email(self):
        try:
            response = requests.post(f'{self._base_url}/email/new', headers=self._headers)
            response.raise_for_status()
            data = response.json()
            self.email = data.get('email')
            self.token = data.get('token')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching email: {e}")

    def check_inbox(self):
        try:
            if not self.email:
                print("Email address not fetched yet. Please fetch an email first.")
                return
            
            url = f'{self._base_url}/email/{self.email}/messages'
            response = requests.get(url, headers=self._headers)
            response.raise_for_status()
            print(response.text)
            self.messages = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching inbox messages: {e}")
