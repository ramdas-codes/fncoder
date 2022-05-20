from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def page_load():
    candidates = ['Ironman', 'Batman', 'Superman',
                  'Spiderman', 'Dr. Strange', 'Scarlet Witch',
                  'Wonderwoman', 'Flash', 'Thor', 'Daredevil']

    return render_template("home.html", candidates=candidates)


@app.route('/result', methods=['POST'])
def result_load():
    result = request.form
    voted_candidate = result['candidate']

    return render_template("result.html", voted_candidate=voted_candidate)


if __name__ == '__main__':
    app.run()
