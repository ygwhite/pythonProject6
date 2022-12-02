from SimpleQIWI import *
from time import  sleep
def pay(message):
    token = 'a094adf00b8af3410c1f1a1c539f49cb'
    phone = '+79787015978'
    api = QApi(token=token, phone=phone)
    price = 10
    comment = api.bill(price)
    print(comment)
    api.start()
    def pay1(comment):
       while True:
            if api.check(comment):
                print('Есть контакт!')
            sleep(5)