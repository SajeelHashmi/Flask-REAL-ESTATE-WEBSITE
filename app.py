from flask import Flask,request,redirect,session,jsonify
from flask import render_template
import user 
import property
from datetime import datetime
import os
from math import ceil
import json

MAX = 9999999999999999

MIN_DATE = datetime(2021,12,5)

# global  objects for queries
USER = user.User()
PROP=property.Property()



# 
# 1.0 have been saved as a backup as a zip file
# now working on version 1.1 
# extra features will include
#   alerts
#       alerts can be saved and will be checked after a certain period of time to show properties with certain chracterstics
#       alerts can be removed 
#       alert props will be the properties returned when an alert is checked#








# Add type attribute to property with three possible values 
#       1 HOUSE
#       2 APARTMENT 
#       3 COMERCIAL
# integrate email bot in this
# remake contact page for email bot
# add alerts in this
# make a hashing function for password protection#





# delete property endpoint
# delete Search endpoint
# unsave property endpoint
# update property endpoint
# update profile endpoint#

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# dont use global obect for user use session








# 1.1 progress
#   Alerts created done
#   Create alert_prop Table done
#   add save prop in property page done
#   create logic to get and delete alert properties after viewing  done
#   delete alert functionality left
#   render them on the userDashboard
#       alert data is being rendered just need to format it for ui ux done
#       render alert properties done
#       check button done  and functionality done
#       remove alert button and functionality done
#   
#   and at the end make email system to check alerts #
@app.route('/saveAlert', methods=['POST'])
def saveAlert():
    if 'user' in session:
            
        cityArg = request.form.get("city") 
        locationArg = request.form.get("location") 
        listingArg = request.form.get('listing') 
        minPriceArg = request.form.get("minPrice")
        maxPriceArg = request.form.get("maxPrice")
        maxAreaArg = request.form.get("maxArea")
        minAreaArg = request.form.get("minArea")
        minRoomsArg = request.form.get("minRooms")
        maxRoomsArg = request.form.get("maxRooms")
        propTypeArg = request.form.get("propType")
            # print(f"city: {cityArg}")
            # print(f"location: {locationArg}")
            # print(f"listing: {listingArg}")
            # print(f"minPrice: {minPriceArg}")
            # print(f"maxPrice: {maxPriceArg}")
            # print(f"maxArea: {maxAreaArg}")
            # print(f"minArea: {minAreaArg}")
            # print(f"minRooms: {minRoomsArg}")
            # print(f"maxRooms: {maxRoomsArg}")
            # print(f"propType: {propTypeArg}")


        city = cityArg if cityArg != '' and cityArg is not None else None  
        location = locationArg if locationArg != '' and locationArg is not None else None  
        listing = listingArg if listingArg != '' and listingArg is not None else '%'
        propType = propTypeArg if propTypeArg != '' and propTypeArg is not None else '%'

        minPrice = minPriceArg if minPriceArg != '' and minPriceArg is not None else 0
        maxPrice = maxPriceArg if maxPriceArg != '' and maxPriceArg is not None else MAX
        maxArea = maxAreaArg if maxAreaArg != '' and maxAreaArg is not None else MAX
        minArea = minAreaArg if minAreaArg != '' and minAreaArg is not None else 0
        minRooms = minRoomsArg if minRoomsArg != '' and minRoomsArg is not None else 0 
        maxRooms = maxRoomsArg if maxRoomsArg != '' and maxRoomsArg is not None else MAX

        # print(location)
        # print(type(minPrice))
        checkDate = datetime.now()
    
        #     # send simple query
        
        # # print("home")
        # lowerLimit = pgNmbr*15
        # upperLimit = lowerLimit +15
        # print(lowerLimit)
        # print(upperLimit)
        print(listing)

        print(city)
        print(location)
        print(listing)
        print(minPrice)
        print(maxPrice)
        print(maxArea)
        print(minArea)
        print(minRooms)
        print(maxRooms)
        print(checkDate)
        print(propType)
        property.createAlert(listing=listing,city=city,location=location,minPrice=minPrice,maxPrice=maxPrice,minArea=minArea,maxArea=maxArea,minRooms=minRooms,maxRooms=maxRooms,propType=propType,checkDate=checkDate,userId=session['userId'])
        return f"{session['user']} your alert has succesfully been created"
    else:
        return 'you have to be logged in to save an alert',403
  # Save the alert to the database
  # ...

    # return 'Success'  # Or you can return a JSON response indicating success


@app.route('/checkForPropAlert', methods=['POST'])
def checkForPropAlert():
    if "user" in session:
        alertId = request.form.get('alertId')
        print(alertId)
        property.createAlertProp(alertId)
    return redirect("/userdashboard#alerts")


@app.route('/deleteAlert', methods=['POST'])
def deleteAlert():
    if "user" in session:
        alertId = request.form.get('alertId')
        print(alertId)
        property.deleteAlert(alertId)
    return redirect("/userdashboard#alerts")


@app.route('/alert/<int:alertId>/<int:propId>')
def deleteAlertProp(alertId,propId):
    property.deleteAlertProp(alertId,propId)
    return redirect(f"/property{propId}")

@app.route('/about')
def about():
    data = {}
    if 'user' in session:
        data['name'] = session['user']
    return render_template("about.html",data=data)





# add more users and more properties
# complete frontend completely
# add other functionality you want like
# email for sign up
# hashing function for password
# Add contact page that accepts message and sends confirmation back to sender thanking them for thier feedback
# debating wether or not to add contact page most of the code is already written but will ruin the asthetic of nav bar
# contact form made linked via footer
# add functionality to mail new user mail user on contactMsg endpoint and in user.User.newUser function 












# complete and tested



# fixed test completely one more time 
# complete and tested
@app.route('/updatePropImg', methods=['POST'])
def updatePropImg():

    id =request.form.get('propId')
    print(id)
    if session['userId'] !=PROP.getOwnerId(id):
        print("return failure")
        return "" ,501
    print("AT UPDATE PROP")
    base_img = request.files['baseImgCropped']
    file_extension = os.path.splitext(base_img.filename)[1].lower()            
    # Generate a unique name for the file using strftime
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    unique_name = f"{timestamp}_{session['userId']}{file_extension}"
    # print(unique_name)
    save_directory = os.path.join("static", "data")
    # Save the file with the unique name
    base_img.save(os.path.join(save_directory, unique_name)) 
    # now create a function to delete the old image and update the url in database
    PROP.updateImg(propId=id,newImg = unique_name)


    return '',200
    




@app.route('/updateListing', methods=['POST'])
def updateListing():
    id = request.form.get("id")
    listing = request.form.get("listing")
    PROP.updateListing(id=id,listing = listing)
    return redirect(f'editprop/{id}')


@app.route('/updatePrice', methods=['POST'])
def updatePrice():
    id = request.form.get("id")
    price = request.form.get("price")
    PROP.updatePrice(id=id,price=price)
    return redirect(f'editprop/{id}')


@app.route('/updateArea', methods=['POST'])
def updateArea():
    id = request.form.get("id")
    area = request.form.get("area")
    PROP.updateArea(id=id,area=area)
    return redirect(f'editprop/{id}')


@app.route('/updateRooms', methods=['POST'])
def updateRooms():
    id = request.form.get("id")
    rooms = request.form.get("rooms")
    PROP.updateRooms(id=id,rooms=rooms)
    return redirect(f'editprop/{id}')

@app.route('/updateAddress', methods=['POST'])
def updateAddress():
    id = request.form.get("id")
    address = request.form.get("address")
    PROP.updateAddress(id=id,address=address)
    return redirect(f'editprop/{id}')


@app.route('/updateDesc', methods=['POST'])
def updateDesc():
    id = request.form.get("id")
    desc = request.form.get("description")

    PROP.updateDesc(id=id,desc=desc)
    return redirect(f'editprop/{id}')
@app.route('/editprop/<int:id>')
def editProp(id):
    a = PROP.getOwnerId(id)
    prop = PROP.getPropById(id)
    print(a)
    data={}
    print(session)
    if session['userId'] ==PROP.getOwnerId(id):
        propInfo =  {
            "id" : prop[0],
            # "ownerId" : prop[1],
            "city" : PROP.getCityName(prop[2]),
            "location" : PROP.getLocationName(prop[3]),
            "uploadDate" : prop[4].strftime("%d/%m/%Y"),
            "listing" : prop[5],
            "area" : prop[6],
            "price" : prop[7],
            "address" : prop[8],
            "desc" : prop[9],
            "baseImgUrl" : (prop[10]),
            "rooms":prop[11],
            # "ownerContact": USER.getPhone(prop[1])
            }

        data['name'] = session['user']
        return render_template("editProp.html",data=data,propInfo=propInfo)






@app.route('/unsaveProp', methods=['POST'])
def unSaveprop():
    if 'userId' in session:
        propId = request.get_json()['id']
        property.unsaveProp(userId= session['userId'],propId=propId)
        return (f'{session["user"]} Property unsaved')
    return ('Not logged in')




@app.route('/delProp', methods=['POST'])
def delProp():
    print("inside DeleteProp")
    if 'userId' in session:
        propId = request.get_json()['id']
        ownerId = PROP.getOwnerId(propId)
        if ownerId == session['userId']:
            PROP.deleteProp(propId=propId)
            return (f'{session["user"]} Property removed')
    return ('Not logged in')

@app.route('/delSearch', methods=['POST'])
def delSearch():
    if 'userId' in session:
        url = request.get_json()['id']
        PROP.deleteSearch(id= session['userId'],url=url)
        return (f'{session["user"]} Search Deleted')
    return ('Not logged in')



@app.route('/saveProperty', methods=['POST'])
def saveProperty():
    propId = request.get_json()['id']
    print(propId)  # Print the request body
    if 'user' in session:
        try:
            property.saveProp(userId=session["userId"],propId=propId)
            return 'Property saved successfully!'  # Return a response message
        except ValueError as e:
            print('Error:', e)
            return str(e), 400 
    else:
        return "Login to save a property ", 400

@app.route("/login",methods=["POST"])
def login():
    if 'user' in session:
        session.pop('user',None)
        session.pop('userId',None)
    email = request.form.get("email")
    password = request.form.get("password")
    
    try:
        USER.login(email=email,password=password)
    except ValueError as e:
        print("exception")
        print(str(e))
        return str(e) ,500
    
    session['user'] = USER.name
    session["userId"] = USER.Id
    return "login succesfull",200


@app.route('/')
def home():
    data = {}
    # print("home")
    properties = PROP.getAll(lowerLimit=0,upperLimit=3)
    Propdata = []
    # print(properties)
    for prop in properties:
       print("inside loop")
       d =  {
        "id" : prop[0],
        # "ownerId" : prop[1],
        "city" : PROP.getCityName(prop[2]),
        "location" : PROP.getLocationName(prop[3]),
        "uploadDate" : prop[4].strftime("%d/%m/%Y"),
        "listing" : prop[5],
        "propType":prop[6],
        "area" : prop[7],
        "price" : prop[8],
        "address" : prop[9],
        "desc" : prop[10],
        "baseImgUrl" : (prop[11]),
        "rooms":prop[12]
        }
       Propdata.append(d)
       # on landing page lenght of featured properties will always be three
    if 'user' in session:
        name = session['user']
        data = {'name': session['user']}

        print("data")
        return render_template("landing.html",Propdata = Propdata,data = data)
    # if "message" in session:
    #     message = session['message']    
    #     session.pop('message')
    #     return render_template("landing.html",message = message,data = data)

    else:
        return render_template("landing.html",Propdata = Propdata,data = data)








@app.route('/explore/', methods=["GET", "POST"])
@app.route('/explore/<int:pgNmbr>', methods=["GET", "POST"])
def explore(pgNmbr=0):
    data = {}
    cityArg = request.args.get("city") 
    locationArg = request.args.get("location") 
    listingArg = request.args.get('listing') 
    minPriceArg = (request.args.get("minPrice"))  
    maxPriceArg = (request.args.get("maxPrice"))  
    maxAreaArg = (request.args.get("maxArea"))  
    minAreaArg = (request.args.get("minArea"))  
    minRoomsArg = (request.args.get("minRooms"))  
    maxRoomsArg = (request.args.get("maxRooms"))  
    propTypeArg = (request.args.get("propType"))  

    city = cityArg if cityArg != '' and cityArg is not None else None  
    location = locationArg if locationArg != '' and locationArg is not None else None  
    listing = listingArg if listingArg != '' and listingArg is not None else '%'
    propType = propTypeArg if propTypeArg != '' and propTypeArg is not None else '%'

    minPrice = minPriceArg if minPriceArg != '' and minPriceArg is not None else 0
    maxPrice = maxPriceArg if maxPriceArg != '' and maxPriceArg is not None else MAX
    maxArea = maxAreaArg if maxAreaArg != '' and maxAreaArg is not None else MAX
    minArea = minAreaArg if minAreaArg != '' and minAreaArg is not None else 0
    minRooms = minRoomsArg if minRoomsArg != '' and minRoomsArg is not None else 0 
    maxRooms = maxRoomsArg if maxRoomsArg != '' and maxRoomsArg is not None else MAX





    start = request.args.get('after')
    print(location)
    print(type(minPrice))
    minDate = datetime.strptime(start, '%Y-%m-%d').date() if start != '' and start is not None else MIN_DATE

 
        # send simple query
    
    # print("home")
    lowerLimit = pgNmbr*15
    upperLimit = lowerLimit +15
    # print(lowerLimit)
    # print(upperLimit)
    # print(listing)

    # print(city)
    # print(location)
    # print(listing)
    # print(minPrice)
    # print(maxPrice)
    # print(maxArea)
    # print(minArea)
    # print(minRooms)
    # print(maxRooms)
    # print(start)






    print(lowerLimit,upperLimit)
    properties = PROP.getAll(lowerLimit=lowerLimit,upperLimit=upperLimit,listing=listing,city=city,location=location,minPrice=minPrice,maxPrice=maxPrice,minArea=minArea,maxArea=maxArea,minRooms=minRooms,maxRooms=maxRooms,minDate=minDate,propType=propType)
    propData = []
    data['count'] = len(properties)
    print(data["count"])
    data['currentPage'] = pgNmbr 
    data["totalPage"] = ceil(data["count"]/15)
    print(data)
    for prop in properties:
    #    print("inside loop")
       d =  {
        "id" : prop[0],
        # "ownerId" : prop[1],
        "city" : PROP.getCityName(prop[2]),
        "location" : PROP.getLocationName(prop[3]),
        "uploadDate" : prop[4].strftime("%d/%m/%Y"),
        "listing" : prop[5],
        "propType":prop[6],
        "area" : prop[7],
        "price" : prop[8],
        "address" : prop[9],
        "desc" : prop[10],
        "baseImgUrl" : (prop[11]),
        "rooms":prop[12]
        }
       propData.append(d)
       # on landing page lenght of featured properties will always be three
    if 'user' in session:
        name = session['user']
        data['name'] = name

        # print("data")
        return render_template("explore.html",propData = propData,data = data)
    # if "message" in session:
    #     message = session['message']    
    #     session.pop('message')
    #     return render_template("landing.html",message = message,data = data)

    else:
        print(data)
        return render_template("explore.html",propData = propData,data = data)














    # only ask for min date 
    # 15 results perpage 



# give users details to the template to
@app.route('/userdashboard')
def userdashboard():
    # check if user is signed in
    data = {}
    if 'user' in session:
        data = {'name': session['user']}
        properties = PROP.getOwners(session['userId'])
        sellerPropData = []
        alerts = property.getAlerts(session['userId'])
        print("alerts")
        # print(alerts)
        alertData = []
        for a in alerts:
            print(a[2])
            d ={
                "id" : a[0],
                "name":json.loads(a[2]),
                "prop": property.getAlertProp(a[0])
                }
            print(d['prop'])
            alertData.append(d)
        # print (alertData)
        for prop in properties:
            # print("inside loop")
            d =  {
                "id" : prop[0],
                # "ownerId" : prop[1],
                "city" : PROP.getCityName(prop[2]),
                "location" : PROP.getLocationName(prop[3]),
                "uploadDate" : prop[4].strftime("%d/%m/%Y"),
                "listing" : prop[5],
                "propType":prop[6],
                "area" : prop[7],
                "price" : prop[8],
                "address" : prop[9],
                "desc" : prop[10],
                "baseImgUrl" : (prop[11]),
                "rooms":prop[12]
                }
            sellerPropData.append(d)
        # print(sellerPropData)

        Savedproperties = PROP.getSavedProps(session['userId'])
        savedPropData = []
        for prop in Savedproperties:
            # print("inside loop")
            d =  {
                "id" : prop[0],
                # "ownerId" : prop[1],
                "city" : PROP.getCityName(prop[2]),
                "location" : PROP.getLocationName(prop[3]),
                "uploadDate" : prop[4].strftime("%d/%m/%Y"),
                "listing" : prop[5],
                "propType":prop[6],
                "area" : prop[7],
                "price" : prop[8],
                "address" : prop[9],
                "desc" : prop[10],
                "baseImgUrl" : (prop[11]),
                "rooms":prop[12]
                }
            savedPropData.append(d)
        
        
        savedSearches = property.getSavedSearches(session['userId'])
        # print(savedSearches)

        







        return render_template("userdashboard.html",data = data,sellerPropData=sellerPropData,savedPropData = savedPropData,savedSearches=savedSearches,alertData = alertData)
    else:
        return redirect("/")


@app.route('/signup',methods=["GET","POST"])
def signup():
    #first check if there is a current user if yes log them out first
    # if method is post create new user and redirect to userDashboard/editprofile
    data = {}
    if request.method =="POST":
        if 'user' in session:
            session.pop('user',None)
            session.pop('userId',None)
        
        name =  request.form.get("username")
        email = request.form.get("email")
        phone = request.form.get("phone")
        pass1 = request.form.get("password")
        pass2 = request.form.get("pass2")

        if pass1 == pass2:
            try:
                USER.newUser(name=name,phone=phone,email=email,password=pass1)
            except ValueError as e:
                data['msg'] = str(e)
                return render_template("signup.html",data = data)
            session['user'] = USER.name
            session["userId"] = USER.Id
            session['msg'] = f"greetings {USER.name} to your dashboard start selling buying and renting with us today"
            return redirect("/userdashboard")
        else:
            data['msg']="passwords donot match"
 

    if 'user' in session:
        name = session['user']
        data['name'] = name
    return render_template("signup.html",data = data)


@app.route('/newproperty',methods=["GET","POST"])
def newproperty():
    data = {}
    # check the print statements before moving forward
 
    if 'user' in session:
        if request.method =="POST":
            listingType = request.form.get('listingType')

            description = request.form.get('description')
            propType = request.form.get('propType')
            print(description)
            price = request.form.get('price')
            area = request.form.get('area')
            rooms = request.form.get('rooms')
            city =request.form.get('city')
            location = request.form.get('location')
            address = request.form.get('address')
            locationId = property.getLocationIdFromName(location,city)
            cityId = property.getCityIdFromName(city)
            # print(request.form)
            # print(request.files)
            base_img = request.files['baseImgCropped']
            file_extension = os.path.splitext(base_img.filename)[1].lower()

            # Generate a unique name for the file using strftime
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d%H%M%S")
            unique_name = f"{timestamp}_{session['userId']}{file_extension}"
            # print(unique_name)
            save_directory = os.path.join("static", "data")
            # Save the file with the unique name
            base_img.save(os.path.join(save_directory, unique_name)) 
            PROP.new(ownerId=session['userId'],cityID=cityId,locationId=locationId,uploadDate=now,listing=listingType,area=area,price=price,address=address,description=description,img=unique_name,rooms=rooms,propType=propType)  


        return render_template("newprop.html",data = data)
    return redirect('/')
        

        
 
      
@app.route("/property<int:x>")
def propertyPage(x):
    prop = PROP.getPropById(x)
    data ={}
    if prop is not None:
        propInfo =  {
            "id" : prop[0],
            # "ownerId" : prop[1],
            "city" : PROP.getCityName(prop[2]),
            "location" : PROP.getLocationName(prop[3]),
            "uploadDate" : prop[4].strftime("%d/%m/%Y"),
            "listing" : prop[5],
            "propType":prop[6],
            "area" : prop[7],
            "price" : prop[8],
            "address" : prop[9],
            "desc" : prop[10],
            "baseImgUrl" : (prop[11]),
            "rooms":prop[12],
            "ownerContact": USER.getPhone(prop[1])
            }
        if 'user' in session:
            data = {'name': session['user']}
        return render_template("prop.html" ,data = data,propInfo=propInfo)
    else:
        # replace later with 404 template
        return "notfound",404
    


@app.route('/saveSearch', methods=['POST'])
def saveSearch():
    if 'userId' in session:
        url = (request.form.get('url'))
        property.saveSearch(id= session['userId'],url=url)
        return (f'{session["user"]} your search was saved')
    return ('Not logged in')

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user',None)
        session.pop('userId',None)
    return redirect('/')


@app.route("/getCityLocation")
def getCityLocation():
    data = {}
    cities = property.getAllCity()

    for city in cities:
        city_id = city[0]
        city_name = city[1]
        locations = property.getAllLocation(city_id)
        location_names = [location[0] for location in locations]
        data[city_name] = location_names

    
    print(jsonify(data))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)