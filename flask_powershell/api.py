from flask import Flask,request
import subprocess

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return execute_script("test")
    return name

#url: http://127.0.0.1:5000/users?username=joerod
@app.route("/users", methods=['GET'])
def name():
    username = request.args.get('username')
    return username 

#url: http://127.0.0.1:5000/
def execute_script(script):
    cmd = ["powershell","-ExecutionPolicy", "Bypass", ".\{0}.ps1".format(script)]
    print(cmd)
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out,err = p.communicate()
    print(out)
    if(err):
        raise Exception('Error: ' + str(err))

    return out

if __name__ == "__main__":
    app.run(port=5000, host='127.0.0.1', debug=True, threaded=True)   