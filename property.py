from conn import conn
from datetime import datetime
from os import remove
cursor = conn.cursor()
MAX = 9999999999999999
MIN_DATE = datetime(2021,12,5)
MAX_DATE = datetime.now()
class Property():
    def __init__(self)->None:
        pass
    def getOwners(self,ownerId ):
        cursor.execute(f"""Select * from property where Owner_id = %s""",(str(ownerId),))
        return cursor.fetchall()
    def deleteProp(self,propId):
        cursor.execute(f"select Base_img from property where Id  = {propId}")
        img = cursor.fetchone()
        if img:
            remove(f'C:\\Users\\Sajeel Hashmi\\Desktop\\DBMS PROJECT\\static\\data\\{img[0]}')
            cursor.execute(f"DELETE FROM property where Id = {propId}")
            conn.commit()
    def deleteSearch(self,id,url):
        cursor.execute("DELETE FROM searches where User_id = %s AND Url = %s",(id,url,))
        conn.commit()
    def getOwnerId(self,propId):
        cursor.execute(f"SELECT Owner_id from property where id = {propId}")
        return cursor.fetchone()[0]
    def updateImg(self,propId,newImg):
        cursor.execute(f"select Base_img from property where Id  = {propId}")
        img = cursor.fetchone()
        if img:
            # remove(f'C:\\Users\\Sajeel Hashmi\\Desktop\\DBMS PROJECT\\static\\data\\{img[0]}')
            # UPDATE `property` SET `Base_img` = '1' WHERE `property`.`Id` = 1 
            cursor.execute(f"UPDATE property SET Base_img = %s where id = {propId}",(newImg,))
            conn.commit()
    def updateListing(self,id,listing):
        cursor.execute("UPDATE property SET Listing = %s WHERE Id = %s",(listing,id,))
        conn.commit()                            
    def updatePrice(self,id,price):
        cursor.execute("UPDATE property SET Price = %s WHERE Id = %s",(price,id,))
        conn.commit()                            
    def updateArea(self,id,area):
        cursor.execute("UPDATE property SET Area = %s WHERE Id = %s",(area,id,))
        conn.commit()                            
    def updateRooms(self,id,rooms):
        cursor.execute("UPDATE property SET Rooms = %s WHERE Id = %s",(rooms,id,))
        conn.commit()                        
    def updateAddress(self,id,address):
        cursor.execute("UPDATE property SET Address = %s WHERE Id = %s",(address,id,))
        conn.commit()            
    def updateDesc(self,id,desc):
        cursor.execute("UPDATE property SET Description = %s WHERE Id = %s",(desc,id,))
        conn.commit()            



    def getSavedProps(self,userId):
        """ this will return a list of tuples where a tuple will have all the property info
            returns empth list if no properties are saved"""
        cursor.execute(f"SELECT Property_id from savedprop where User_id = {userId}")
        saved = cursor.fetchall()
        # print(saved)
        propList = []
        for propId in saved:
           d=  self.getPropById(propId[0])
           propList.append(d)
        #    print(d)
        return(propList)


    def getAll(self,lowerLimit = 0,upperLimit = 3,minDate =MIN_DATE,maxDate = MAX_DATE,listing = '%',city =None,location =None,minArea = 0,maxArea =MAX,minRooms = 0,maxRooms =MAX,minPrice = 0,maxPrice =MAX,propType='%'):
        if city is None:
            query = "SELECT * FROM property WHERE Upload_date BETWEEN %s AND %s AND Price BETWEEN %s AND %s AND Rooms BETWEEN %s AND %s AND Area BETWEEN %s AND %s AND Listing LIKE %s AND Type Like %s limit %s,%s"
            cursor.execute(query, (minDate, maxDate, minPrice, maxPrice, minRooms, maxRooms, minArea, maxArea, listing,propType,lowerLimit,upperLimit))
            return cursor.fetchall()
        if location is None:
            query = "SELECT * FROM property WHERE Upload_date BETWEEN %s AND %s AND Price BETWEEN %s AND %s AND Rooms BETWEEN %s AND %s AND Area BETWEEN %s AND %s AND Listing LIKE %s AND Type Like %s AND City_id = %s limit %s,%s"
            cityId = getCityIdFromName(city)
            cursor.execute(query, (minDate, maxDate, minPrice, maxPrice, minRooms, maxRooms, minArea, maxArea, listing, propType,cityId,lowerLimit,upperLimit))
            return cursor.fetchall()
        query = "SELECT * FROM property WHERE Upload_date BETWEEN %s AND %s AND Price BETWEEN %s AND %s AND Rooms BETWEEN %s AND %s AND Area BETWEEN %s AND %s AND Listing LIKE %s AND Type Like %s AND Location_id = %s limit %s,%s"
        locationId = getLocationIdFromName(location,city)
        print(locationId)
        print(query)
        cursor.execute(query, (minDate, maxDate, minPrice, maxPrice, minRooms, maxRooms, minArea, maxArea, listing,propType, locationId,lowerLimit,upperLimit))
        return cursor.fetchall()      
           
    def getPropById(self,id):
        cursor.execute(f"""Select * from property where id = {id}""")
        return (cursor.fetchone())

    def getCityName(self,id):
        cursor.execute(f"SELECT Name FROM city WHERE Id = {id}")
        return cursor.fetchone()[0]
    def getLocationName(self,id):
        cursor.execute(f"SELECT Name FROM location WHERE Id = {id}")
        return cursor.fetchone()[0]
    def new(self,ownerId,cityID,locationId,uploadDate,listing,area,price,address,description,img,rooms,propType):
        cursor.execute(f"INSERT INTO property (Id, Owner_id , City_id , Location_id , Upload_date,Listing,Type,Area,Price,Address,Description,Base_img,Rooms) VALUES (NULL, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s,%s) """,(ownerId,cityID,locationId,uploadDate,listing,propType,area,price,address,description,img,rooms))
        conn.commit()
        print("added")
def getAllCity():
    """Return a list of tuples with value id , name"""
    cursor.execute('SELECT * from city')
    return cursor.fetchall()
def getAllLocation(id):
    """Return a list of tuples with single value name"""
    cursor.execute(f'Select Name from location where City_id = {id}')
    return cursor.fetchall()
def getCityIdFromName(name):
    cursor.execute("SELECT Id FROM city WHERE Name LIKE %s", (name,))
    return cursor.fetchone()[0]
def getLocationIdFromName(name,cityName):
    cursor.execute("SELECT Id FROM city where Name like %s",(cityName,))
    cityId = cursor.fetchone()[0]
    cursor.execute("SELECT Id FROM location WHERE Name LIKE %s AND City_id = %s", (name,cityId,))
    return cursor.fetchone()[0]
def getSavedSearches(id):
    cursor.execute(f"SELECT Url from searches where User_id = {id}")
    return cursor.fetchall()
def saveSearch(id,url):
    cursor.execute('INSERT INTO searches (User_id,Url) VALUES (%s,%s)',(id,url,))
    conn.commit()
def saveProp(userId,propId):
    try:
        cursor.execute('INSERT INTO savedprop (User_id,Property_id) VALUES (%s , %s)',(userId,propId,))
        conn.commit()
    except Exception as e:
        raise ValueError ('you have already saved this property')
def unsaveProp(userId,propId):
    cursor.execute('DELETE FROM savedprop WHERE User_id = %s AND Property_id = %s',(userId,propId,))
    conn.commit()

def createAlert(listing,city,location,minPrice,maxPrice,minArea,maxArea,minRooms,maxRooms,propType,checkDate,userId):
    print(checkDate)
    if city is None:
        name = f"""
    {{
	"priceBetween": "{minPrice} and {maxPrice if maxPrice != MAX else 'any' }",
	"areaBetween": "{minArea} and {maxArea if maxArea != MAX else 'any'}",
	"roomsBetween": "{minRooms} and {maxRooms if maxRooms != MAX else 'any'}",
	"listing": "{listing if listing !='%' else 'RENT/BUY both'}",
	"type": "{propType if propType !='%' else 'any'}"
    }} """
        query = f"SELECT Id FROM property WHERE Price BETWEEN {minPrice} AND {maxPrice} AND Rooms BETWEEN {minRooms} AND {maxRooms} AND Area BETWEEN {minArea} AND {maxArea} AND Listing LIKE '{listing}' AND Type Like '{propType}'"
        cursor.execute("INSERT INTO alerts (User_id, Query, Name,Check_date) VALUES (%s, %s, %s,%s)", (userId, query, name,checkDate))
        conn.commit()

        return
        # return cursor.fetchall()
    if location is None:
        name = f"""
    {{
	"priceBetween": "{minPrice} and {maxPrice if maxPrice != MAX else 'any' }",
	"areaBetween": "{minArea} and {maxArea if maxArea != MAX else 'any'}",
	"roomsBetween": "{minRooms} and {maxRooms if maxRooms != MAX else 'any'}",
	"listing": "{listing if listing !='%' else 'RENT/BUY both'}",
	"type": "{propType if propType !='%' else 'any'}",
	"city": "{city}"
    }} """

        cityId = getCityIdFromName(city)
        query = f"SELECT * FROM property WHERE Price BETWEEN {minPrice} AND {minPrice} AND Rooms BETWEEN {minRooms} AND {maxRooms} AND Area BETWEEN {minArea} AND {maxArea} AND Listing LIKE '{listing}' AND Type Like '{propType}' AND City_id = {cityId}"
        cursor.execute("INSERT INTO alerts (User_id, Query, Name,Check_date) VALUES (%s, %s, %s,%s)", (userId, query, name,checkDate))
        conn.commit()
        return
    name = f"""
    {{
	"priceBetween": "{minPrice} and {maxPrice if maxPrice != MAX else 'any' }",
	"areaBetween": "{minArea} and {maxArea if maxArea != MAX else 'any'}",
	"roomsBetween": "{minRooms} and {maxRooms if maxRooms != MAX else 'any'}",
	"listing": "{listing if listing !='%' else 'RENT/BUY both'}",
	"type": "{propType if propType !='%' else 'any'}",
	"city": "{city}",
	"location": "{location}"
    }} """
    locationId = getLocationIdFromName(location,city)
    query = f"SELECT * FROM property WHERE Price BETWEEN {minPrice} AND {minPrice} AND Rooms BETWEEN {minRooms} AND {maxRooms} AND Area BETWEEN {minArea} AND {maxArea} AND Listing LIKE '{listing}' AND Type Like '{propType}' AND Location_id = {locationId}"
    cursor.execute("INSERT INTO alerts (User_id, Query, Name,Check_date) VALUES (%s, %s, %s,%s)", (userId, query, name,checkDate))
    conn.commit()
    return


def getAlerts(userId):
    print(userId)
    cursor.execute(f"SELECT * FROM alerts WHERE User_id = {userId}")
    return cursor.fetchall()


def createAlertProp(alertId):
    #SELECT * FROM `property` WHERE `Upload_date` >= '2023-06-01' 
    # SELECT `Query` FROM `alerts` WHERE `Id` = 4 #
    cursor.execute(f"SELECT Query, Check_date from alerts where Id = {alertId}")
    data = cursor.fetchone()
    query = data[0]
    checkDate = data[1]

    query +="  Upload_date >= %s"
    print (query)
    print(checkDate)
    print(type(checkDate))
    cursor.execute(query,(checkDate,))
    queryRes =  cursor.fetchall()
    if queryRes:
        for res in queryRes:
            # INSERT INTO `alert_prop` (`Alert_id`, `Property_id`) VALUES ('4', '89') 
            propId = res[0]
            cursor.execute("INSERT INTO alert_prop (Alert_id, Property_id) values (%s,%s)",(alertId,propId,))
            conn.commit()
    else:
        print("query returns empty")
    newCheck = datetime.now()
    # UPDATE `alerts` SET `Check_date` = '2023-06-06' WHERE `alerts`.`Id` = 5 
    cursor.execute("UPDATE alerts SET Check_date = %s WHERE Id = %s",(newCheck,alertId,))
    conn.commit()

def getAlertProp(alertId):
    cursor.execute("SELECT Property_id from alert_prop WHERE Alert_id = %s ",(alertId,))
    propId = cursor.fetchall()
    data = []
    p = Property()
    if propId:
        for id in propId:
            prop = p.getPropById(id[0])
            propInfo =  {
            "id" : prop[0],
            # "ownerId" : prop[1],
            "city" : p.getCityName(prop[2]),
            "location" : p.getLocationName(prop[3]),
            "uploadDate" : prop[4].strftime("%d/%m/%Y"),
            "listing" : prop[5],
            "propType":prop[6],
            "area" : prop[7],
            "price" : prop[8],
            "address" : prop[9],
            "desc" : prop[10],
            "baseImgUrl" : (prop[11]),
            "rooms":prop[12],
            # "ownerContact": USER.getPhone(prop[1])
            }
            data.append(propInfo)
    return data


def deleteAlertProp(alertId,propId):
    # "DELETE FROM alert_prop WHERE `alert_prop`.`Alert_id` = 5 AND `alert_prop`.`Property_id` = 91"
    cursor.execute("DELETE FROM alert_prop WHERE Alert_id = %s AND Property_id = %s ",(alertId,propId,))
    conn.commit()

def deleteAlert(alertId):
    cursor.execute("DELETE FROM alerts WHERE Id = %s",(alertId,))
    conn.commit()
if __name__ == "__main__":
    print(createAlertProp(4))
    # cursor.execute("Select * from property limit 5,10")
    # print(cursor.fetchall())
    # x = Property()
    # cursor.execute(f"DELETE FROM property where Id = 88")
    # conn.commit()
    # cursor.execute(f"select Base_img from property where Id  = 2334")
    # img = cursor.fetchone()
    # print(img)
    # if img:
    #     remove(f'C:\\Users\\Sajeel Hashmi\\Desktop\\DBMS PROJECT\\static\\data\\{img[0]}')

    # x.getSavedProp(userId =2)
    # print(cursor.fetchone())
    # MIN_DATE = datetime(2021,12,5)
    # print(MIN_DATE)
    # # data = {}
    # cities = getAllCity()

    # for city in cities:
    #     city_id = city[0]
    #     city_name = city[1]
    #     locations = getAllLocation(city_id)
    #     location_names = [location[0] for location in locations]
    #     data[city_name] = location_names

    # json_data = json.dumps(data)
    # print(json_data)


    # testing query structure and adding to values tupple
    # lowerLimit = 0
    # upperLimit = 3
    # cursor.execute(f"""Select * from property limit {lowerLimit},{upperLimit}""")
    #     # will return a list of tuples
    # print (cursor.fetchall())
    # cursor.execute(f"""Select * from property limit 0,10""")
    #     # will return a list of tuples
    # x = datetime.now()
    # print(x.strftime("%d/%m/%Y"))
    # data = []
    # properties=(cursor.fetchall())
    # PROP = Property()
    # for prop in properties:
    #    d =  {
    #     "id" : prop[0],
    #     "ownerId" : prop[1],
    #     "cityId" : prop[2],
    #     "locationId" : prop[3],
    #     "uploadDate" : prop[4].strftime("%d/%m/%Y"),
    #     "listing" : prop[5],
    #     "area" : prop[6],
    #     "price" : prop[7],
    #     "address" : prop[8],
    #     "desc" : prop[9],
    #     "baseImgUrl" : PROP.getBaseImg(id= prop[10])
    #     }
    #    data.append(d)
    # print(data)
