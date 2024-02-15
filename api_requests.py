import requests


class CompClubRequests:
    def __init__(self, ip: str, balance: float):
        self.IP = ip
        self.SESSION = requests.Session()
        self.SESSION.auth = ('admin', 'admin')
        self.limit_balance = balance
        

    def get_username_and_acc_linking(self, userid: str) -> tuple[str, bool]:

        response = self.SESSION.get(f'http://{self.IP}/api/users/{userid}')
        res = response.json()
        username = res['result']['username']

        # опрос на проверку привязки аккaунта
        response = self.SESSION.get(f'http://{self.IP}/api/users/{userid}/note')
        res = response.json()
        if len(res['result']) == 0:
            return username, False
        return username, True


    def put_finger_tmp_to_db(self, userid: str, tmp: str) -> None:
        
        body = {
            'text': tmp,
            'severity': 0
        }
        # вставить текст отпечатка
        response = self.SESSION.post(f'http://{self.IP}/api/v2.0/users/{userid}/notes', json=body)


    def get_finger_tmp_by_userid(self, userid: str) -> str:

        response = self.SESSION.get(f'http://{self.IP}/api/users/{userid}/note')
        tmp = response.json()['result'][0]['text']
        return tmp

    def check_data_login(self, login: str, password: str) -> bool:
        #провера на валидность
        res = self.SESSION.get(f'http://{self.IP}/api/users/{login}/{password}/valid')
        checking = int(res.json()['result']['result'])
        if checking != 0:
            return (False, 'Неверный логин или пароль')
        
        #проверка на человек внутри
        user_id = res.json()['result']['identity']['userId']
        res = self.SESSION.get(f'http://{self.IP}/api/usersessions/activeinfo')
        for i in res.json()['result']:
            if i['userId'] == user_id:
                return (True, 'Запускается батник')
        
        #проверка на баланс
        res = self.SESSION.get(f'http://{self.IP}/api/users/{user_id}/balance')
        if res.json()['result']['deposits'] < self.limit_balance:
            return(False, 'Не хватает средств')
        
        #проверка на абонемент
        res = self.SESSION.get(f'http://{self.IP}/api/users/{user_id}/producttime')
        for i in res.json()['result']:
            productName = i['productName'].lower().replace('.', '')
            if 'vip' in productName or 'вип' in productName:
                if i['isDepleted']==i['isDeleted']==i['isVoided']==i['isExpired']==False:
                    return (True, 'Запускается батник')
        return (False, 'Нет вип или она кончилась')

        
    

    
    
    
    
    
    
    
    
    
    
    def check_data_finger(self) -> bool:
        pass
