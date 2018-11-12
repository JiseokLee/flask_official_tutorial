# _*_ coding: utf-8 _*_

from flask import Flask, request, session, render_template, redirect, url_for
app = Flask(__name__)


# @app.route()를 통해 URL 패턴과 POST Method를 정의하고, 바로 하단의 함수에서 URL 패턴 매칭되는 Action을 처리
@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/main')
def main():
    return 'Main Page'

# <>로 URL 패턴을 변수로 처리 가능
@app.route('/user/<username>')
def showUserProfile(username):
    return 'USER : %s' % username

@app.route('/user/id/<int:userId>')
def showUserProfileById(userId):
    return 'USER ID : %d' % userId

# @app.route('/account/login', methods=['POST']) 내부에 methods 항목을 통해 받을 REST Action Type을 지정
# 지정 이외의 Action Type을 사용하면 Flask가 405 에러를 출력
# request 모듈에서 POST 한 파라미터 값을 가져오기 위해서는 request.form['id']와 같이 사용
# request.form['id']로 사용 시 id 파라미터가 없으면 Flask가 400 에러를 출력
@app.route('/account/login', methods=['POST'])
def login():
    if request.method == 'POST':
        userId = request.form['id']
        wp = request.form['wp']

        if len(userId)==0 or len(wp)==0:
            return userId + ', ' + wp + ' 로그인 정보를 제대로 입력하지 않았습니다.'

        session['logFlag'] = True
        session['userId'] = userId
        return session['userId'] + ' 님 환영합니다.'
    else:
        return '잘못된 접근입니다.'

# 로그인 정보 가져오기
@app.route('/user', methods=['GET'])
def getUser():
    if session.get('logFlag') != True:
        return '잘못된 접근입니다.'

    userId = session['userId']
    return '[GET][USER] USER ID : {0}'.format(userId)

# redirect()를 활용하면, 사용자의 조회 위치를 변경할 수 있다.
# url_for()는 route 주소로 이동하는 것이 아닌 정의된 함수를 호출한다. 위 예제에서 main을 호출하는 대상은 main()인 함수다.
# session.clear()를 사용하면 따로 설정 필요없이 session을 비울 수 있다.
@app.route('/account/logout', methods=['POST','GET'])
def logout():
    session['logFlag'] = False
    session.pop('userId', None)
    return redirect(url_for('main'))

# flask 에러 처리
# @app.errorhandler()를 통해 특정 에러를 Catch 및 처리 할 수 있다.
@app.errorhandler(400)
def uncaughtError(error):
    return '잘못된 사용입니다.'

# flask 응답 처리
# make_response() 함수를 통해 반환 되는 Object를 만들고, 이를 처리 가능할 수 있게 된다.
@app.errorhandler(404) 
def not_found(error): 
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

# app.secret_key는 세션 키를 생성하며, 로그인과 같이 세션을 맺는 경우 필수적으로 넣어야 한다.
# 세션 생성 시, app.secret_key로 키를 생성하지 않으면 Flask가 500 에러를 출력
app.secret_key = 'sample_secret_key'

if __name__ == '__main__':
    # app.debug는 개발의 편의를 위해 존재, True 값일 경우 코드를 변경하면 자동으로 서버가 재시작, 또한 웹 상에서 파이썬 코드를 수행할 수 있게 됨
    app.debug = True
    # 현재 접근은 개발 소스가 존재하는 로컬에서만 가능하다. 외부에서도 접근을 가능하게 하려면 app.run(host='0.0.0.0')로 서버 실행부를 변경해야 한다.
    app.run()
