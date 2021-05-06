from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Kahvilan nimi', validators=[DataRequired()])
    location = StringField("Kahvilan sijainti Google Mapsissa (URL)", validators=[DataRequired(), URL()])
    open = StringField("Avautuu (esim. 8:00)", validators=[DataRequired()])
    close = StringField("Sulkeutuu (esim 19:00)", validators=[DataRequired()])
    coffee_rating = SelectField("Kahvin laatu", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi_rating = SelectField("Wifin vahvuus", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power_rating = SelectField("Sähköpistokkeiden saatavuus", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    quietness_rating = SelectField("Työskentelyrauha", choices=["✘", "☮","☮☮","☮☮☮","☮☮☮☮","☮☮☮☮☮"], validators=[DataRequired()])
    submit = SubmitField('Lähetä')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding="utf8") as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.location.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_rating.data},"
                           f"{form.quietness_rating.data}")
        return redirect(url_for('cafes'))
    return render_template("add.html", form=form)



@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)

@app.route("/jar")
def jar():
    return render_template("jar.html")


if __name__ == '__main__':
    app.run(debug=True)