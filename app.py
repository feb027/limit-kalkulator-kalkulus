from flask import Flask, render_template, request, flash
from sympy import limit, symbols, oo, fraction, expand, sympify, pi, sin, tan, cos

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

x = symbols('x')

def validate_expression(expression_str):
    try:
        expression = sympify(expression_str)

        if any(subexpr.has(x) and subexpr.is_real is False for subexpr in expression.args):
            flash('Ekspresi matematika tidak valid. Akar kuadrat dari bilangan negatif tidak diperbolehkan.', 'error')
            return None
    except:
        flash('Ekspresi matematika tidak valid.', 'error')
        return None
    return expression

@app.route('/calculate_limit', methods=['GET', 'POST'])
def calculate_limit():
    result = None
    if request.method == 'POST':
        expression_str = request.form['expression']

        expression = validate_expression(expression_str)
        if expression is None:
            return render_template('index.html', result=result)

        numerator, denominator = fraction(expression)

        if numerator != 0 or denominator != 0:
            expression = expand(expression)

        lim_x_approaches = request.form['lim_x_approaches']

        try:
            if lim_x_approaches.lower() == 'pi':
                lim_x_approaches = pi  
            else:
                lim_x_approaches = sympify(lim_x_approaches) 
        except ValueError:
            flash('Nilai x mendekati harus berupa bilangan, "pi", atau ekspresi matematika valid.', 'error')
            return render_template('index.html', result=result)

        try:
            result = limit(expression, x, lim_x_approaches)
            if result.is_symbol:
                flash('Hasil limit tidak valid', 'error')
                result = None
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')

    return render_template('index.html', result=result)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/materi')
def materi():
    return render_template('materi.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
