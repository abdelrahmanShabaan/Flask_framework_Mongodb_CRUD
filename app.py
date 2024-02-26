from flask import Flask, request ,render_template,redirect,url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

# config system
app = Flask(__name__,template_folder="test") #__main__==>directly  , #file====>non direct
app.config["MONGO_URI"] = "mongodb://localhost:27017/"
client = MongoClient('localhost', 27017)


#create my database with collections
db = client["firstdatabase"]
mycollection=db["users"]



#Here i will show all users
@app.route('/')
def index():
        user_data = mycollection.find({})
        return render_template('users.html' , users_html=user_data) #i will send list of users as element context in html file




@app.route('/users')
def get_users():
    name=request.args.get('name')
    age=request.args.get('age')
    location=request.args.get('location')
    if name != None or age != None or location != None :
        mycollection.insert_one({
            "name" : name,
            "age" : age ,
            "location": location
        })
    if mycollection != []:
        user_data = mycollection.find({})
        return render_template('users.html' , users_html=user_data) #i will send list of users as element context in html file
    else :
        return "<h1> NO Users </h1>"
    



#create user
@app.route('/createuser', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name=request.form.get("name")
        age=request.form.get("age")
        location=request.form.get("location")
        if any([name, age, location]):
            mycollection.insert_one({
                "name": name,
                "age": age,
                "location": location
            })
            print("added success user")
            return redirect('/users')
    
    return render_template('create_user.html')



def get_user_by_id(id):
    return mycollection.find_one({'_id': ObjectId(str(id))})


@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        name = request.form.get("name")
        age = request.form.get("age")
        location = request.form.get("location")
        if any([name, age, location]):
            mycollection.update_one({'_id': ObjectId(id)}, {'$set': {'name': name, 'age': age, 'location': location}})
            print("Found and Updated")
        return redirect('/users')
    else:
        user_to_edit = get_user_by_id(id)
        return render_template('edit_user.html', user=user_to_edit)



@app.route('/delete/<string:id>') 
def delete_user(id):
    if id != None and mycollection.count_documents({'_id': ObjectId(id)}) !=0 : 
            mycollection.delete_one({'_id': ObjectId(id)})
            print("Found and Delete")
    return redirect('/users')



if __name__ == "__main__":
    app.run(debug=True)
    




