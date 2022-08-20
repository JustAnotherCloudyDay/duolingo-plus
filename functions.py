from requests import Session
import json
from random import randint, sample


class Duolingo:

    def __init__(self, referral_link):
        self.link = referral_link.replace('https://invite.duolingo.com/', '')
        self.s = Session()
        self.name = ''.join(sample('abcdhijklswyzABCDFQU014589', 8))
        self.pwd = ''.join(sample('abcdhifjklswyzABCDFQU014589', 8))
        self.email = f'{self.name}{randint(1000, 9999)}@gmail.com'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/88.0.4324.104 Safari/537.36', 'content-type': 'application/json'}

    def register(self):
        data_1 = {"timezone": "Europe", "fromLanguage": "ru", "inviteCode": self.link}
        request = self.s.post('https://www.duolingo.com/2017-06-30/users?fields=id',
                              headers=self.headers, data=json.dumps(data_1))

        token = 'Bearer ' + request.cookies.get_dict()['jwt_token']
        user_id = json.loads(request.content.decode('utf-8'))['id']

        self.headers.update({'Authorization': token})
        data_2 = {"email": self.email, "name": self.name, "password": self.pwd}
        request = self.s.patch(
            'https://www.duolingo.com/2017-06-30/users/{}?fields=adsConfig,email,identifier,name,privacySettings,'
            'trackingProperties,username'.format(user_id), headers=self.headers, data=json.dumps(data_2))

        if 'SESSION_END' in str(request.content):
            print('registered')
        else:
            print('nope')


# create a class object with your referral link https://invite.duolingo.com/BDHTZTB5CWWKTSMDWSGCGNPWFA
# and use register() method for register each account
cs = Duolingo('https://invite.duolingo.com/BDHTZTB5CWWKTSMDWSGCGNPWFA')
cs.register()
