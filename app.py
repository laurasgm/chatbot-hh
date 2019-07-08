import os, sys
from flask import Flask, request
from pymessenger import Bot
from utils import wit_response

PAGE_ACCESS_TOKEN = "EAAgFHVm3DPMBACmsHv1Y5pqb0cmnYd3SELKgJGU1AmoCuI6s7uEbnTYXEpzZAt7GX56vF6AgHZAqor8KT4tZAZAA160Mwwpp3vwKSVSmIwZCgHDwKhct4edEGctnux5Fth5SrfSNnie6aIYgGYJ3XJNgqanbPtZA27pCq8MOfN9AZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "hello world", 200



@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']



                if 'message' in messaging_event:
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'
                    
                    response = None

                    entity, value = wit_response(messaging_text)
                    print (entity, value)

                    cont = 0

                    
                    if entity == 'sintomas':
                        
                        if value == 'si':
                            response = "gracias, siga describiendo los sintomas por favor"
                            cont=+5
                        elif value == 'no':
                            response = "continua, por favor"
                            cont=+3
                        elif value == 'puedo' or 'respirar':
                            cont=+4
                            response = "continua, aqui sigo"

                        elif value == 'dolor' or 'pecho':
                            response = 'Reponda si o no, ¿El dolor es como si se sentara un elefante encima?'
                        
                        elif value == 'nauseas' or 'desmayo':
                            cont=+1
                            response = "aja..."
                        elif value == 'fatiga':
                            cont=+2
                            response = "será mejor que estés escribiendo esto sentado"
                        elif value == 'mandibular' or 'adormecimiento' or 'msi':
                            cont+=3
                    elif entity == 'saludo':
                        response = "Hola soy el bot de healthy heart, por favor comienza a describir tus sintomas, uno por cada mensaje que envies. Recuerda decir -listo- cuando termines, gracias por la atención. Espero no mueras :3"
                    elif entity == 'resultado':
                        print (cont)
                        if cont >= 5:
                            response = "Consulta por URGENCIAS, riesgo ALTO de un infarto agudo de miocardio"
                            cont = 0
                        elif cont == 3 or cont == 4:
                            response = "Te recomiendo que realices una consulta PRIORITARIA lo antes posible"
                            cont = 0
                        elif cont < 3:
                            response = "Te recomiendo que realices una consulta EXTERNA"
                            cont = 0
                
                bot.send_text_message(sender_id, response)


    return "ok",200

def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True , port = 80)
