from conn import conn
import json
import emailAlerts

# add to and from json methods no need we are storing user as a global object
# implement password hashing if there is time
# #
cursor = conn.cursor()
class User():



    def login(self,email,password):
        # check if this user exists
        cursor.execute(f"""Select * from user where Email = %s""",(email,))
        user = cursor.fetchone()
        print(user)
        if user is None:
            print("exception")
            raise ValueError("User not found")
        else:
        # check password
            if password == user[4]:
                self.Id = user[0]
                self.name = user[1]
                self.phone = user[2]
                self.email =user[3]
            else:
                raise ValueError("incorrect password")
        # send back confirmation





    def newUser(self,name,email,password,phone):
        # check if email is unique
        print(email)
        cursor.execute("SELECT Email FROM user WHERE Email = %s", (email,))
        existingEmail = cursor.fetchone()
        if existingEmail:
            raise ValueError ("email already in use")
        else:
            cursor.execute(f"""INSERT INTO user (Id, Name , Phone , Email , Password) VALUES (NULL, %s,%s, %s, %s) """,(name,phone,email,password))
            conn.commit()
            self.login(email=email,password=password)
            # emailAlerts.signUpMsg(email=email,name=name)
    def getPhone(self,id):
        cursor.execute(f"""Select Phone from user where Id = %s""",(id,))
        return cursor.fetchone()[0]
      
        


if __name__ =="__main__":
    # for testing connections and queries
    # return empty list if no record is found
    # fstrings work fine 
    # fstrings could be prone to sql injection attacks so we will use built in tupple#

    # to add value first excecute the query using cursor then commit 
    
    from datetime import datetime
    x = datetime.now()
    print(x.strftime("%m/%d/%Y,%H:%M:%S")+'.jpg')
    # cursor.execute(f"""SELECT * FROM location LIMIT 0,100""")
    # # conn.commit()
    # print(json.dumps(cursor.fetchall()))


