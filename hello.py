#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'

@app.route('/index')
def index():
    return 'index page!'

@app.route('/main')
def main():
    return 'main page'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id

@app.route('/logging')
def logging_test():
    test = 1
    app.logger.debug('디버깅 필요')
    app.logger.warning(str(test) + " 라인")
    app.logger.error('에러발생')
    return '로깅 끝'

@app.route('/login_form')
def login_form():
    return render_template('login_form.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if (request.form['username'] == 'js' and request.form['password'] == '0502'):
            session['logged_in'] = True
            session['username'] = request.form['username']
            return request.form['username'] + ' 님 환영합니다.'
        else:
            return '로그인 정보가 맞지 않습니다.'
    else:
        return '잘못된 접근'

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/template')
@app.route('/template/<tempid>')
def template_test(tempid=None):
    sports = ['야구', '축구', '농구']
    return render_template('template.html', tempid=tempid, sports=sports)

app.secret_key = 'sample_secret_key'
 
if __name__ == '__main__':
    app.debug = True
    app.run()
