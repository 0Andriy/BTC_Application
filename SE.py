import requests
import json
from email import message
import smtplib
from email.mime.text import MIMEText



#! Клас для операцій зв'язаних з валютою
class Сurrency:

    def __init__(self) -> None:
        pass

    
    #! Отримуємо котіровки з біржи по валютам 
    def get_ticket(self, coin1='btc', coin2='uah'):
        response = requests.get(url=f"https://btc-trade.com.ua/api/ticker/{coin1}_{coin2}")
        list = json.loads(response.text)
        return list


#! Клас для функціоналу пов'язаних з роботою бази даних (у нашому випадку з файлами)
class WorkWithDatabase:

    def __init__(self, path="DataBase-00.txt") -> None:
        self.path = path


    #! Зчитуємо базу даних
    def readDatabase(self):
        with open(self.path, "r") as file:
            list = [line.strip() for line in file]
        return list


    #! Дописуємо в базу даних (або краще зробити на перезапис всього файла а не дописувати, оскільки можуть вискочити нежданчики)
    def writeDatabase(self, mail):
        with open(self.path, "a") as file:
            file.write(f'\n{mail}')


#! Клас для роботи з поштою
class Mail:

    def __init__(self, path) -> None:
        self.__sender= '1223qwe@gmail.com'  #! паролі і логін краще було закинути в якись конфіг файл або в середовище окруженнія для надійності але так тут не роблю
        self.__password = '1234567890'
        self.__db = WorkWithDatabase(path=path)


    #! Перевіряємо наявністю веденої пошти у нашій базі ( при наявномті виводиться -- всьо добре, коли нема додається до бази)
    def subscribe(self, mail):
        list = self.__db.readDatabase()
        if mail in list: print(f'Пошта -- {mail} -- присутня в базі даних')
        else:
            print(f'Пошта -- {mail} -- не було знайдено в базі даних, тому буде додана до бази даних')
            self.__db.writeDatabase(mail)


    #! Проводимо розсилку по наявним поштам в базі
    def sendEmails(self, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        list = self.__db.readDatabase()

        try:
            server.login(self.__sender, self.__password)
            msg = MIMEText(message)
            #! Тема листа
            msg["Subject"] = "BTC to UAH"  #? subject

            for receiver in list:
                server.sendmail(self.__sender, receiver, msg.as_string())

            return "The message was sent successfully!"
        except Exception as _ex:
            return f'{_ex}\nCheck your login or password please!'



#! *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def main():
    cur = Сurrency()
    db = WorkWithDatabase(path="DataBase-00.txt")
    mail = Mail(path="DataBase-00.txt")

    print(f'Виберіть операцію:\nВзнати поточний курс біткоіну (BTC) до гривні (UAH) -- 1\nПідписати емейл на отримання інформації по зміні курсу -- 2\nЗробити розсилку котіровки всім підписникам -- 3\n')
    f = input("Type your answer:  ")
    
    match f:
        case '1':
            list = cur.get_ticket()
            price_sell = list['btc_uah']['sell']
            print(f'1 BTC = {price_sell} UAH')
        case '2':
            mail.subscribe(mail=input('Ведіть вашу пошту для підписання на розсилку: ').strip())
        case '3':
            list = cur.get_ticket()
            price_sell = list['btc_uah']['sell']
            mail.sendEmails(message=f'1 BTC = {price_sell} UAH')
        case _:
            print("Такої операції нема у списку")

if __name__ == '__main__':
    main()