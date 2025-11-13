from flask import Flask, render_template, request, redirect, url_for, flash
import urllib3
import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.secret_key = 'vijay892089'  # required for flash

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        enrollment = request.form['enrollment'].strip()
        dob = request.form['dob'].strip()
        html = fetch_bteup_result(enrollment, dob)
        if html:
            return render_template("result.html", result_html=html)
        else:
            flash("❌ No record found. Please try again.")
            return redirect(url_for('index'))  # redirect back to input form
    return render_template("index.html")


@app.route('/admit')
def admit():
    return render_template('admit.html')

@app.route('/admit2')
def admit2():
    return render_template('admit2.html')


@app.route('/view/<enrollment>')
def view_result(enrollment):
    return "<h2>This route is no longer used since we don't save raw files.</h2>"


def fetch_bteup_result(enrollment, dob):
    session = requests.Session()
    url = "https://result.bteexam.com/even/main/rollno.aspx"
    res = session.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')

    try:
        viewstate = soup.find("input", {"id": "__VIEWSTATE"})["value"]
        event_validation = soup.find("input", {"id": "__EVENTVALIDATION"})["value"]
    except:
        return None

    data = {
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": event_validation,
        "txtRollNo": enrollment,
        "txt_dob": dob,
        "btnSave": "Show Result"
    }

    response = session.post(url, data=data, verify=False)

    if "Invalid" in response.text or "Please enter" in response.text:
        return None

    # ✅ Replace BTEUP logo with your custom logo
    html = response.text.replace('/images/1.jpg', '/static/images/1.png')

    return html


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
