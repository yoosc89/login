import pymysql
from pymysql import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class MySQL:
    def __init__(self):      
        self.sqlconn = pymysql.connect(host='', user='', password='', db='', charset='utf8')
        self.cursor = self.sqlconn.cursor()


    def insert_user(self, account):
        self.cursor.execute("insert into program_users values (%s, %s, %s, %s);", account)    
        self.sqlconn.commit()
        self.sqlconn.close()
   
    def login_user(self,id, pwd, token, program_name):
        self.cursor.execute("SELECT pwd, token FROM program_users WHERE id= %s and program_name = %s ;", [id,program_name])
        Adata = self.cursor.fetchall()[0]
        try:
            if check_password_hash(Adata[0], pwd) and check_password_hash(Adata[1], token) : 
                return 'login' #로그인 성공 리턴값
            else:
                return 'fail' #로그인 실패 리턴값
        except IndexError: 
            print('로그인에 실패했습니다')
            return 'fail' #로그인 실패 리턴값


def create_account():
    used_program = 'test' #프로그램 이름
    while True:
        id = input('id를 입력하세요 : ')
        pwd = input('pwd를 입력하세요 : ')
        pwd_cnf = input('pwd를 다시 한번 입력하세요 : ')
        if pwd == pwd_cnf:
            break
        else:
            print('암호가 다르게 입력되었습니다.')

    token = input('인증번호를 입력하세요 : ')
    
    pwd = generate_password_hash(pwd)
    token = generate_password_hash(token)
    MySQL.insert_user([id, pwd, token, used_program])


def login():
    id = input('id를 입력하세요 : ')
    pwd = input('pwd를 입력하세요 : ')
    token = input('인증번호를 입력하세요 : ')
    program_name = input('프로그램명을 입력하세요 : ')
    MySQL.login_user(id, pwd, token, program_name)


def exit():
    print("종료합니다")
    return False


def select_func():
    while True:
        select = input('이용할 서비스를 입력하세요 1. 계정생성 , 2. 로그인, 3. 창닫기 : ')

        function={
            '1' : create_account,
            '2' : login,
            '3' : exit
        }
        try:
            func = function[select]
        except KeyError:
            return select_func()

        if func() == False:
            break
            

if __name__ == '__main__':
    select_func()