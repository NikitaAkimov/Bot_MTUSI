from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from datetime import datetime
from data import raspisanie

token = "25a99390fbbb59c3b9c4ad2bb0094a2cf7b3e36857687b9f8d418ea7646f0526b9d9b5c9c392b99e7dfed"
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

mess = "hello friend!!!"

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            #print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
            #print('Текст сообщения: ' + str(event.text))
            #print(event.user_id)
            response = event.text.lower()
            response_2 = response.split()
            if event.from_user and not (event.from_me):
                for arr in raspisanie:
                    if str(response_2[0]) == arr:
                        for arr1 in raspisanie[arr].items():
                            persent = ""
                            response_2.append(persent)
                            #print(response_2)
                            if str(response_2[1]) == str(arr1[0]):
                                vk_session.method('messages.send', {'user_id': event.user_id, 'message': str(arr1[1]), 'random_id': 0})
                            elif str(response_2[1]) == "":
                                mess = "Введите корректную команду. \nЧтобы узнать список команды напишите мне Помощь."
                                vk_session.method('messages.send', {'user_id': event.user_id, 'message': mess, 'random_id': 0})
                                break
                # === Отправка сообщения администратору ===
                if str(response_2[0]) == "админу":
                    mess = "Ваше сообщение отправлено."
                    mess_admin = "Вам написал пользователь @id" + str(event.user_id) + " " +" ".join(str(x) for x in response_2[1:])
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': mess, 'random_id': 0})
                    vk_session.method('messages.send', {'user_id': 202477769, 'message': mess_admin, 'random_id': 0})
                # === Инстукция по использованию бота ===
                if str(response_2[0]) == "помощь":
                    mess = "Расписание, [номер группы] [день недели]" + "\n" + "Примеры команд: \nзрс1701 вт \nбрв1701 пт \nбст1901 ср" + "\n\n" + "Обратная связь" + "\n" + "Чтобы обратиться к администраторам сервиса с предложением для улучшения сервиса, коррекцией расписания или другим вопросам отправьте команду \nадмину [ваше сообщение] \n или напишите нам на почту yetanothercompany2019@gmail.com"
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': mess, 'random_id': 0})
