from flask import Flask, render_template, url_for, request, jsonify
from model_prediction import * 
from predict_response import *
 
app = Flask(__name__)

predicted_emotion=""
predicted_emotion_img_url=""

@app.route('/')
def index():
    entries = show_entry()
    return render_template("index.html", entries=entries)
 
@app.route('/predict-emotion', methods=["POST"])
def predict_emotion():
    
    # Obtenha a entrada de texto da requisição POST
    input_text = request.json.get("text")  
    
    if not input_text:
        # Resposta a enviar se input_text não for definida
        response = {
                    "status": "error",
                    "message": "Digite um texto para prever a emoção!"
                  }
        return jsonify(response)
    else:  
        predicted_emotion, predicted_emotion_img_url = predict(input_text)
        
        # Resposta a enviar se input_text for definida
        response = {
                    "status": "success",
                    "data": {
                            "predicted_emotion": predicted_emotion,
                            "predicted_emotion_img_url": predicted_emotion_img_url
                            }  
                   }

        # Enviar resposta         
        return jsonify(response)


@app.route("/save-entry", methods=["POST"])
def save_entry():

    # Obtenha a data, a emoção prevista e o texto digitado pelo usuário para salvar a entrada
    date = request.json.get("date")           
    emotion = request.json.get("emotion")
    save_text = request.json.get("text")

    save_text = save_text.replace("\n", " ")

    # Entrada CSV
    entry = f'"{date}","{save_text}","{emotion}"\n'  

    with open("./static/assets/data_files/data_entry.csv", "a") as f:
        f.write(entry)
    return jsonify("Success")


@app.route("/bot-response", methods=["POST"])
def bot():
    # Obtenha a entrada do usuário
    input_text = request.json.get("user_bot_input_text")  
    # Chame o método para obter a resposta do robô
    bot_res = bot_response(input_text)
    
    response = {
        "bot_response": bot_res
    }
      
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)