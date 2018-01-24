import json
import apiai #используется для подключения к DialogFlow и отправки запроса
from handler.base_plugin import BasePlugin

class MLChatterPlugin(BasePlugin):

    def __init__(self, prefixes=("",)):

        super().__init__()

        self.prefixes = prefixes

    async def check_message(self, msg):
        return not msg.is_out and not msg.is_forwarded

    async def process_message(self, msg):
        for prefix in self.prefixes:
            if msg.text.startswith(prefix):
                request = apiai.ApiAI('ТУТ ВАШ CLIENT ACCESS TOKEN').text_request() # Токен API к Dialogflow
                request.lang = 'ru' # На каком языке будет послан запрос
                request.session_id = 'Small-Talk' # ID Сессии диалога (нужно, чтобы потом учить бота)
                request.query = msg.text[len(prefix):].strip() # Посылаем запрос к ИИ с текстом от юзера, при этом убирая префикс
                responsejson = json.loads(request.getresponse().read().decode('utf-8'))
                response = responsejson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
                # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
                if response:
                    await msg.answer(response)
                else:
                    await msg.answer('Я Вас не совсем понял!')
                break
        else:
            return False
