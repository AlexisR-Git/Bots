from flask import Flask, request, jsonify
from twilio.rest import Client
import random
 
app = Flask(__name__)
 
# Credenciales de Twilio
account_sid = 'your_twilio_account_sid'
auth_token = 'your_twilio_auth_token'
client = Client(account_sid, auth_token)
 
# Almacenar temporalmente el OTP
otp_store = {}
 
@app.route('/send_otp', methods=['POST'])
def send_otp():
    phone_number = request.json['phone']
    otp = random.randint(100000, 999999)
    
    # Guardar OTP asociado al número de teléfono
    otp_store[phone_number] = otp
    
    # Enviar el OTP a través de Twilio
    message = client.messages.create(
        body=f'Su código de verificación es {otp}',
        from_='+your_twilio_number',
        to=phone_number
    )
    return jsonify({"message": "OTP enviado con éxito"}), 200
 
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    phone_number = request.json['phone']
    otp_received = request.json['otp']
    
    # Verificar si el OTP coincide
    if otp_store.get(phone_number) == int(otp_received):
        return jsonify({"message": "Autenticación exitosa"}), 200
    else:
        return jsonify({"message": "OTP incorrecto"}), 401
 
if __name__ == '__main__':
app.run(debug=True)