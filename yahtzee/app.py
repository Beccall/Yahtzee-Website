from flask import Flask, render_template, request, session, url_for
from flask_session import Session
from yahtzee.dice import Dice
from werkzeug.utils import redirect

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template('home.html', score_sheet=session['scorecard'])

    if request.method == "POST":
        if session['scorecard']:
            feedback = request.form.get('feedback')
            if feedback == "CLEAR SCOREBOARD":
                session.clear()
                session['scorecard'] = []
                session["play"] = Dice()
        else:
            session['scorecard'] = []
        return render_template('home.html', score_sheet=session['scorecard'])



@app.route("/yahtzee", methods=["GET", "POST"])
def yahtzee():
    count = 0
    session['roll_dice'] = ''
    prompt = ''
    if request.method == "GET":
        return render_template("index.html", roll_dice=session['roll_dice'], turn=session["turn"],
                               keep_dice=session["keep_dice"], score_sheet=session["scorecard"],
                               prompt=prompt, options=session["options"], count=count)
    if request.method == "POST":
        session["options"] = []
        session['scorecard'] = session["play"].score_sheet()
        feedback = request.form.getlist("feedback")
        if not feedback or (len(feedback) > 1 and "keep all dice" in feedback):
            if not feedback:
                prompt = "To 'Roll Again', you must select dice"
            else:
                prompt = "To 'Keep All Dice', you can not select dice"
            feedback = "ROLL AGAIN"
        elif feedback[0] == "ROLL DICE":
            session["turn"] = 1
            session['roll_dice'] = session["play"].roll(5)
            session["keep_dice"] = []
            for dice in session['roll_dice']:
                session["keep_dice"].append(dice)
        elif feedback[0] != "ROLL AGAIN" and feedback[0] != "keep all dice" and session["turn"] < 4:
            for di in feedback:
                session["keep_dice"].remove(int(di))
            session["turn"] += 1
            session['roll_dice'] = session["play"].roll(len(feedback))
            for dice in session['roll_dice']:
                session["keep_dice"].append(dice)
        if feedback[0] == "keep all dice" or session["turn"] == 3:
            session["turn"] = 0
            session["play"].count(session["keep_dice"])
            session["options"] = session["play"].options()

            return redirect('/scorecard')

        return render_template("index.html", feedback=feedback, roll_dice=session['roll_dice'], turn=session["turn"],
                               keep_dice=session["keep_dice"], score_sheet=session["scorecard"],
                               prompt=prompt, options=session["options"], count=count)


@app.route('/scorecard', methods=["GET", "POST"])
def scorecard():
    prompt=''
    if request.method == "GET":
        return render_template('scorecard.html', keep_dice=session["keep_dice"], options=session["options"],
                               score_sheet=session['scorecard'])
    if request.method == "POST":
        feedback = request.form.get('feedback')
        if not feedback:
            prompt = "You must select a category"

        elif feedback == "ROLL DICE":
            return redirect(url_for("yahtzee"))
        else:
            amount = session['options'][feedback]
            session['scorecard'] = session["play"].add_score(feedback, amount)
            session['options'] = []
            session['keep_dice'] = []
        return render_template('scorecard.html', feedback=feedback, keep_dice=session["keep_dice"],
                               options=session["options"], score_sheet=session["scorecard"], turn=session["turn"],
                               scorecard=session["scorecard"], prompt=prompt)


if __name__ == '__main__':
    app.run(debug=True)
