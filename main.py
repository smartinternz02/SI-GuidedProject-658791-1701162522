# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
from flask import Flask,render_template,request,redirect, url_for
from cloudant.client import Cloudant
#Authenticate using an IAM APIu Key
client = Cloudant.iam({
  "apikey": "qy9wdJVJNyl2MZKjvm9jsOzgt3cq6LQHhnV94d6_Lfsk",
  "host": "7471e2f6-3bf9-461a-bbcf-dba900138edb-bluemix.cloudantnosqldb.appdomain.cloud",
  "iam_apikey_description": "Auto-generated for key crn:v1:bluemix:public:cloudantnosqldb:us-south:a/3f916b1c8ce94d9dbd0cf103d1e133af:40aeb180-3edb-40e7-a6cb-0e4d6acbdb38:resource-key:aa77a4b4-9535-4741-95e4-d3b75d63681d",
  "iam_apikey_id": "ApiKey-b6f5fc25-9d9a-4e26-91d1-68c812811a27",
  "iam_apikey_name": "Service credentials-1",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/3f916b1c8ce94d9dbd0cf103d1e133af::serviceid:ServiceId-d2365997-b13c-4a95-bddd-f5238df61f62",
  "url": "https://7471e2f6-3bf9-461a-bbcf-dba900138edb-bluemix.cloudantnosqldb.appdomain.cloud",
  "username": "7471e2f6-3bf9-461a-bbcf-dba900138edb-bluemix"
}, connect=True)
my_database = client.create_database('my_database')

app=Flask(__name__)

model=load_model("Updated-Xception-diabetic-retinopathy.h5")
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/index.html')
def home():
    return render_template("index.html")
#registration page
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/afterreg', methoids=['POST'])
def afterreg():
    X = [X for X in request.form.values()]
    print(X)
    data = {
    '_id' = X[1],
    'name' = X[0],
    'psw' = X[2]
    }
    print(data)
    query = {'_id': {'$eq': data['_id']}}
    docs = my_database.get_query_result(query)
    print(docs)
    print(len{docs.all()})
    if{len(docs.all()==0)}
        url = my_database.create_document(data)
        #response = requests.get(url)
        return render_template('register.html', pred = "Registration Successful, please login using your details")
        else:
        return render_template('register.html', pred = "You are already a member, please login using your details")
#login page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/afterlogin',methods=['POST'])
def afterlogin() :
    user = request.form['_id']
    passw = request.form['psw']
    print(user,passw)

    query = {'_id', {'$eq': user}}
    docs = my_database.get_query_result(query)
    print(docs)
    print(len(docs.all()))
    if(len(docs.all()) == 0):
       return render_template('login.html', pred = "The user name is not found.")
    else:
       if((user==docs[0][0]['_id'] and passw==docs[0][0]['psw'])):
           return redirect(url_for('prediction'))
       else:
           print('Invalid User')

#logut page
@app.route('/logout')
def login():
    return render_template('logout.html')

@app.route('/result', methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        f = request.files['image']
        basepath = os.path.dirname(__file__)
        filepath = os.path.join(basepath, 'uploads', f.filename)
        f.save(filepath)
        img = image.load_img(filepath, target_size=(299,299))
        x = image.img_to_array(img)
        x = np.expand_dims(x,axis=0)
        img_data=preprocess_input(x)
        prediction = np.argmax(model.predict(img_data), axis=1)
        index = ['No Diabetic Retinopathy', 'Mild DR', 'Moderate DR', 'Severe DR', 'Proliferative DR']
        result=str(index[prediction[0]])
        print(result)
        return render_template('prediction.html', prediction=result)


@app.route('/predict',methods=['GET','POST']))
def upload():
    if request.method=='POST':
        f=request.files['image']
        basepath=os.path.dirname(__file__)
        filepath=os.path.join(basepath,'uploads',f.filename)
        f.save(filepath)
        img=image.load_img(filepath,target_size=(64,64))
        x=image.img_to_array(img)
        x=np.expand_dims(x,axis=0)
        pred=np.argmax(model.predict(x),axis=1)
        index=['Bear','Crow','Elephant','Rat']
        text="The Classified Animal is : " +str(index[pred[0]])
    return text

if __name__=='__main__':
    app.run()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
