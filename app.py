from flask import Flask, render_template, request, redirect, url_for,session
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
from googletrans import Translator
from googletrans.models import Translated 
import requests
translator=Translator()
app = Flask(__name__)
app.secret_key = '1234'
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from  mysqlconnect import *
from datetime import datetime

@app.route('/register',methods=['GET','POST'])                         
def register():
     if request.method=='POST':
          username=request.form.get('username')
          password=request.form.get('password')
          hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
          insert_user_query = "INSERT INTO flaskusers (username, password) VALUES (%s, %s)"
          user_data = (username, hashed_password)
        
          insert_data(insert_user_query, user_data)  # Function to insert data into DB
        
          return redirect(url_for('loginuser'))  # Redirect to a success page or login page
     
     return render_template('register.html')  # Render registration form

@app.route('/login',methods=['GET','POST'])
def loginuser():
     if request.method=='POST':
          username=request.form.get('username')
          print('username',username)
          password=request.form.get('password')
          userquery="SELECT * FROM flaskusers WHERE username = %s"
          user = fetch_data(userquery, (username,))
          print(user)
        
          if user and bcrypt.check_password_hash(user[0]['password'], password): 
                session['username']=username 
                return redirect(url_for('home'))
          else:
                return('Login failed. Check your username and/or password.')  
            
     return render_template('login.html')  



@app.route('/', methods=['GET', 'POST'])
def home():
    botpreresponse='select your bot and and ask questions'
    if 'username' not in session:
         return redirect(url_for('loginuser'))
    else:
         username=session.get('username')
         print(username)
    return render_template('home.html', username=username,botpreresponse=botpreresponse)

@app.route('/science', methods=['GET', 'POST'])
def sciencebot():
    if 'username' not in session:
         return redirect(url_for('loginuser'))
    username=session.get('username')
    text = ''
    botresponse=''
    botpreresponse = 'I am an expert science scholar. You can ask me any questions related to that.'
    if 'chathistory' not in session:
                session['chathistory'] = []

    if request.method == 'POST':
        text = request.form.get('inputmessage')  # Get the input message
        try:
            detection = translator.detect(text).lang  # Detect language
        except AttributeError:
            
            detection = 'en'
            print(f"Language detection failed. Defaulting to English.")
        
        if detection!='en':
             print('another language identified')
             translated_text = translator.translate(text, dest='en').text
             text=translated_text
             
        else:
             text=text
        print(f"Received text: {text}")  # Debugging input

        if text:
            model = genai.GenerativeModel("gemini-pro")
            chat=model.start_chat(history=[])
            prompt = f"""
            You are an expert in science. You must give the response in 2 lines. 
            If the question is about a topic other than science, respond with: 
            "Sorry, I don't know. I am not an expert in that."
            If the user greets you, greet them back politely.
            Question: {text}
            """
            
           
            response=chat.send_message(prompt,stream=True)
            
            
            session['chathistory'].append(("User", text,datetime.now().strftime("%H:%M:%S")))
            
            for chunk in response:
                print(chunk.text)

                session['chathistory'].append(("Bot", chunk.text,datetime.now().strftime("%H:%M:%S")))
            print(f"Model response: {response}")

            session.modified = True
            if response:
                botresponse = session['chathistory']
        else:
            botpreresponse = 'I am an expert science scholar. You can ask me any questions related to that.'

    return render_template('index.html', botresponse=botresponse,botpreresponse=botpreresponse,username=username)

@app.route('/technology', methods=['GET', 'POST'])
def technologybot():
    if 'username' not in session:
         return redirect(url_for('loginuser'))
    botresponse=''
    botpreresponse = 'I am an expert technology scholar. You can ask me any questions related to that.'
    username=session.get('username')
    if 'techchathistory' not in session:
                session['techchathistory'] = []
    if request.method == 'POST':
        text = request.form.get('inputmessage')  # Get the input message
        print(f"Received text: {text}")  # Debugging input
        try:
            detection = translator.detect(text).lang  # Detect language
        except AttributeError:
            
            detection = 'en'
            print(f"Language detection failed. Defaulting to English.")
        
        if detection!='en':
             print('another language identified')
             translated_text = translator.translate(text, dest='en').text
             text=translated_text
             
        else:
             text=text
        print(f"Received text: {text}")  # Debugging input


        if text:
            model = genai.GenerativeModel("gemini-pro")
            chat=model.start_chat(history=[])
            prompt = f"""
            You are an expert in technology. You must give the response in 2 lines. 
            If the question is about a topic other than technology, respond with: 
            "Sorry, I don't know. I am not an expert in that."
            If the user greets you, greet them back politely.
            Question: {text}
            """
            
           
            response=chat.send_message(prompt,stream=True)
            
            
            session['techchathistory'].append(("User", text,datetime.now().strftime("%H:%M:%S")))
            
            for chunk in response:
                print(chunk.text)
                session['techchathistory'].append(("Bot", chunk.text,datetime.now().strftime("%H:%M:%S")))
            print(f"Model response: {response}")

            session.modified = True
            if response:
                botresponse = session['techchathistory']
        else:
             botpreresponse = 'I am an expert technology scholar. You can ask me any questions related to that.'


    return render_template('technology.html', botresponse=botresponse,botpreresponse=botpreresponse,username=username)

@app.route('/history', methods=['GET', 'POST'])
def historybot():
    # Logic for history bot
    if 'username' not in session:
         return redirect(url_for('loginuser'))
    botresponse=''
    username=session.get('username')
    botpreresponse='I am an expert history scholar.You can ask me any questions related to that'
    if 'historychathistory' not in session:
                session['historychathistory'] = []
    if request.method == 'POST':
        text = request.form.get('inputmessage')  # Get the input message
        print(f"Received text: {text}")  # Debugging input
        try:
            detection = translator.detect(text).lang  # Detect language
        except AttributeError:
            
            detection = 'en'
            print(f"Language detection failed. Defaulting to English.")
        
        if detection!='en':
             print('another language identified')
             translated_text = translator.translate(text, dest='en').text
             text=translated_text
             
        else:
             text=text
        print(f"Received text: {text}")  # Debugging input


        if text:
            model = genai.GenerativeModel("gemini-pro")
            chat=model.start_chat(history=[])
            prompt = f"""
            You are an expert in history. You must give the response in 2 lines. 
            If the question is about a topic other than history, respond with: 
            "Sorry, I don't know. I am not an expert in that."
            If the user greets you, greet them back politely.
            Question: {text}
            """
            
           
            response=chat.send_message(prompt,stream=True)
           
            
            session['historychathistory'].append(("User", text,datetime.now().strftime("%H:%M:%S")))
            
            for chunk in response:
                print(chunk.text)
                session['historychathistory'].append(("Bot", chunk.text,datetime.now().strftime("%H:%M:%S")))
            print(f"Model response: {response}")

            session.modified = True
            if response:
         
               botresponse = session['historychathistory']
        else:
             botpreresponse = 'I am an expert history scholar. You can ask me any questions related to that.'

    return render_template('history.html' ,botresponse=botresponse,botpreresponse=botpreresponse,username=username)

@app.route('/literature', methods=['GET', 'POST'])
def literaturebot():
    if 'username' not in session:
         return redirect(url_for('loginuser'))
    username=session.get('username')
    botresponse=''
    botpreresponse='I am an expert literature scholar.You can ask me any questions related to that'
    if 'literaturechathistory' not in session:
                session['literaturechathistory'] = []
    if request.method == 'POST':
        text = request.form.get('inputmessage')  
        print(f"Received text: {text}")  
        try:
            detection = translator.detect(text).lang  # Detect language
        except AttributeError:
            
            detection = 'en'
            print(f"Language detection failed. Defaulting to English.")
        
        if detection!='en':
             print('another language identified')
             translated_text = translator.translate(text, dest='en').text
             text=translated_text
             
        else:
             text=text
        print(f"Received text: {text}")  # Debugging input


        if text:
            model = genai.GenerativeModel("gemini-pro")
            chat=model.start_chat(history=[])
            prompt = f"""
            You are an expert in literature. You must give the response in 2 lines. 
            If the question is about a topic other than literature, respond with: 
            "Sorry, I don't know. I am not an expert in that."
            If the user greets you, greet them back politely.
            Question: {text}
            """
            
           
            response=chat.send_message(prompt,stream=True)
            
            
            session['literaturechathistory'].append(("User", text,datetime.now().strftime("%H:%M:%S")))
            
            for chunk in response:
                print(chunk.text)
                session['literaturechathistory'].append(("Bot", chunk.text,datetime.now().strftime("%H:%M:%S")))
            print(f"Model response: {response}")

            session.modified = True
            if response:
                botresponse = session['literaturechathistory']
        else:
             botpreresponse = 'I am an expert history scholar. You can ask me any questions related to that.'

            
            
    return render_template('literature.html', botresponse=botresponse,botpreresponse=botpreresponse,username=username)
 
@app.route('/logout',methods=['GET','POST'])
def logoutuser():
     if 'username' not in session:
         return redirect(url_for('loginuser'))
     session.pop('chathistory',None)
     session.pop('techchathistory',None)
     session.pop('historychathistory',None)
     session.pop('literaturechathistory',None)
     session.pop('username',None)
     return redirect(url_for('loginuser'))






if __name__ == '__main__':
    app.run(debug=True)
