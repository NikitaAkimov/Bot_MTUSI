from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from datetime import datetime
import time
import schedule

login, password = "89105159070", "mavvyd-cimjop"
vk_session = vk_api.VkApi(login=login, password=password, app_id=2685278)
vk_session.auth(token_only=True)

#token = "0ff1c3204ea03b50e4e6b6154315d26505a0cdc05487e5e3173d87aea61b9fec1d0552dfc947d9cea3347"
#vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def job():
    vk_session.method('messages.send', {'peer_id': -185970233, 'message': "помощь", 'random_id': 0})

schedule.every(1).hour.do(job)

while True:
    date = str(datetime.strftime(datetime.now(), "%M:%S"))
    #print(date)
    schedule.run_pending()
    time.sleep(1)
