from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
from datetime import datetime
from data import raspisanie

token = "25a99390fbbb59c3b9c4ad2bb0094a2cf7b3e36857687b9f8d418ea7646f0526b9d9b5c9c392b99e7dfed"
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def save_dict_to_file(dic):
    f = open('data_user.txt','w')
    f.write(str(dic))
    f.close()

def load_dict_from_file():
    f = open('data_user.txt','r')
    data=f.read()
    f.close()
    return eval(data)

# === функция Клавиатура ===
def create_keyboard(response):
    keyboard = VkKeyboard(one_time = False)
    if str(response) == 'клавиатура':
        keyboard.add_button('пн', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('вт', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('ср', color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button('чт', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('пт', color=VkKeyboardColor.DEFAULT)
    elif str(response) == 'закрыть':
        return keyboard.get_empty_keyboard()
    
    keyboard = keyboard.get_keyboard()
    return keyboard

# ==== Словарь с идентификаторм и номером группы пользователя ====
data_user = {}

# ==== Сообщение по шаблону ====
mess = "hello friend!!!"

# ==== Сообщение с рекламой ====
mess_ad = {
    1 : "Хочешь заказать реферат, диплом, контрольную или курсовую по отличной цене? Переходи по ссылке на сервис Напишем!!! \nhttps://ad.admitad.com/g/jyvqpi890n656cbb99e110ecf760fc/",
    2 : "Обучение программированию, web дизайну и многому другому на GeekBrains \nhttps://ad.admitad.com/g/k3dfvevwit656cbb99e165a37ca03d/ \n=== Купоны и скидки === \nСкидка 10% на факультеты GeekUniversity! - Cкидка действует 5 дней после активации. \nhttps://ad.admitad.com/g/914l66e9cl656cbb99e165a37ca03d/?i=3 \nСкидка 15% на все профессии! \nhttps://ad.admitad.com/g/o17llm0vov656cbb99e165a37ca03d/?i=3"
}

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            #print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
            #print('Текст сообщения: ' + str(event.text))
            #print(event.user_id)
            response = event.text.lower()
            response_2 = response.split()
            keyboard = create_keyboard(response_2[0])
            if event.from_user and not (event.from_me):
                # === Отправка пользователю расписания на нужный день ===
                data_user = load_dict_from_file()
                for arr_user in data_user:
                    if str(event.user_id) == arr_user:
                        user_group = data_user[str(event.user_id)]
                        for arr in raspisanie:
                            if str(user_group) == arr:
                                for arr1 in raspisanie[arr].items():
                                    if str(response_2[0]) == str(arr1[0]):
                                        vk_session.method('messages.send', {'user_id': event.user_id, 'message': str(arr1[1]), 'random_id': 0})
                # === Регистрация пользователя ===
                if str(response_2[0]) == "регистрция":
                    data_user = load_dict_from_file()
                    user_id = str(event.user_id)
                    new_user = {user_id : response_2[1]}
                    data_user.update(new_user)
                    save_dict_to_file(data_user)
                    mess = "Вы зарегестрированы"
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': mess, 'random_id': 0})
                # === Отправка сообщения администратору ===
                if str(response_2[0]) == "админу":
                    mess = "Ваше сообщение отправлено."
                    mess_admin = "Вам написал пользователь @id" + str(event.user_id) + " " +" ".join(str(x) for x in response_2[1:])
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': mess, 'random_id': 0})
                    vk_session.method('messages.send', {'user_id': 202477769, 'message': mess_admin, 'random_id': 0})
                # === Инстукция по использованию бота ===
                if str(response_2[0]) == "помощь":
                    mess = "Регистрация пользователя \nРегистрация, регистрция [номер группы] \nПримеры команд: \nрегистрация зрс1701 \nрегистрация брв1701 \nрегистрация бст1901" + "\n\n" + "Расписание, [день недели]" + "\n" + "Примеры команд: \nвт \nпт \nср" + "\n\n" + "Клавиатура с днями недели \nЧтобы воспользоваться быстрым вводом с клавиатуры напишите боту сообщение Клавиатура \nПримеры команд: \nклавиатура" + "\n\n" + "Обратная связь" + "\n" + "Чтобы обратиться к администраторам сервиса с предложением для улучшения сервиса, коррекцией расписания или другим вопросам отправьте команду \nадмину [ваше сообщение] \n или напишите нам на почту yetanothercompany2019@gmail.com"
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': mess, 'random_id': 0})
                # === открыть клавиатуру ===
                if str(response_2[0]) == "клавиатура":
                    mess = "Нажми на кнопку, чтобы получить рсписание на нужный день"
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': mess, 'random_id': 0, 'keyboard': keyboard})
                # === закрыть клвиатуру ===
                if str(response_2[0]) == 'закрыть':
                    mess = "закрыть"
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': mess, 'random_id': 0, 'keyboard': keyboard})
