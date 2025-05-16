from flask import Flask, render_template, request, redirect, session
import mysql.connector
import json
import time
import smtplib
import ssl

app = Flask(__name__)
app.secret_key = "iotihu"

devices = ['A0131', 'B0385']
user = {"username": "abc", "password": "1234"}


@app.route('/')
def main():
    if 'user' in session and session['user'] == user['username']:
        return redirect('/index')
    return ('<h1>You are not logged in.</h1>'
            '<p>'
            '<a href="/login">Click here</a> to login. </p>')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user['username'] and password == user['password']:
            session['user'] = username
            return redirect('/index/')
        return "<h1>Wrong username or password</h1>"
    return render_template("login.html")


@app.route('/addvalue', methods=['POST'])
def addvalue():
    signal = request.data
    cleartext = signal.decode()
    cleartext = json.loads(cleartext)
    print(cleartext)
    if cleartext['server_id'] == 'S03237a':
        if cleartext['device_id'] in devices:
            device = cleartext['device_id']
            temperature = float(cleartext['temperature'])
            temperature = round(temperature, 1)
            rain_status = float(cleartext['rain_status'])
            t = time.asctime(time.localtime())
            print(f'temperature: {temperature}')
            print(f'rain status: {rain_status}')
            print(t)

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="iot"
            )

            mycursor = mydb.cursor()
            sql = "INSERT INTO sensors24 (device, temperature, rain_status, time) VALUES (%s, %s, %s, %s)"
            val = (device, temperature, rain_status, t)
            mycursor.execute(sql, val)
            mydb.commit()
            print("1 record inserted, ID:", mycursor.lastrowid)

            if rain_status == 1:
                mycursor = mydb.cursor()
                mycursor.execute("SELECT rain_status FROM sensors24 ORDER BY ID DESC LIMIT 12")
                myresult = mycursor.fetchall()
                rain = 0

                for x in myresult:
                    print("rain: ", x[0])
                    rain = rain + x[0]
                if rain == 1:
                    port = 465
                    smtp_server = "smtp.gmail.com"
                    sender_email = "your mail"
                    receiver_email = "receiver email"
                    password = 'your password'
                    message = """Subject: Warning

                    It has started raining."""

                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message)
                else:
                    pass
            else:
                pass

            if temperature <= 22:
                return 'Turn off the A/C.'
            elif temperature >= 24:
                return 'Turn on the A/C.'
            return 'OK'
        return 'Unauthorized!'
    return 'Wrong server!'


@app.route('/index/', methods=['GET'])
def getvalues():
    if 'user' in session and session['user'] == user['username']:

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iot"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM sensors24 ORDER BY ID DESC LIMIT 1")
        myresult = mycursor.fetchall()

        for x in myresult:
            print("Id: ", x[0])
            print("Device: ", x[1])
            print("Temperature: ", x[2])
            temp = x[2]

        mycursor.execute("SELECT * FROM sensors24 ORDER BY ID DESC LIMIT 12")
        myresult = mycursor.fetchall()

        t = 0
        counter = 0

        for x in myresult:
            counter += 1
            t += x[2]
        average_temperature = t / counter
        average_temperature = "%.1f" % average_temperature
        print(average_temperature)

        return render_template('index.html', title='Κόμβος 2023.24', field1=temp, field2=average_temperature)
    return ('<h1>You are not logged in.</h1>'
            '<p>'
            '<a href="/login">Click here</a> to login. </p>')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('user')
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
