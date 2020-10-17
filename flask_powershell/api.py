from flask import Flask,request
import subprocess

app = Flask(__name__)

#url: http://127.0.0.1:5000/process?processname=chrome
@app.route("/process", methods=['GET'])
def name(script = 'test2'):
    username = request.args.get('processname') # take arguments from the url and use them in scripts
    cmd = ["powershell","-ExecutionPolicy", "Bypass", ".\{0}.ps1".format(script),username]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out,err = p.communicate()
    print(out)
    if(err):
        raise Exception('Error: ' + str(err))
    return out

#url: http://127.0.0.1:5000/
@app.route("/", methods=['GET'])
def execute_script(script = 'test'):
    cmd = ["powershell","-ExecutionPolicy", "Bypass", ".\{0}.ps1".format(script),""]
    print(cmd)
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out,err = p.communicate()
    print(out)
    if(err):
        raise Exception('Error: ' + str(err))

    return out

if __name__ == "__main__":
    app.run(port=5000, host='127.0.0.1', debug=True, threaded=True)   