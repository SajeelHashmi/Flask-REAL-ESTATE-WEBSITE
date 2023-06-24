import smtplib
from email.message import EmailMessage
import property
from json import loads
# whenever a person signs in send them a message
cursor = property.cursor
conn = property.conn
sender = "ADD YOUR EMAIL"
password = "ADD YOUR APP KEY"



def signUpMsg(email,name):

    em = EmailMessage()
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    try:
        # Authentication
        s.login(sender, password)
    except:
        print('Incorrect Username or Password:\n')
        return 
    em["To"] = email
    message = f"""
    Dear {name},
        Thank you for choosing SnM Properties, your trusted destination for all your real estate needs. We are thrilled to have you on board and excited to embark on this journey together.
        Welcome to our community of homeowners, buyers, sellers, and enthusiasts! At SnM Properties, we believe that every property tells a unique story. Our mission is to provide you with
        an exceptional real estate experience, where you can explore, discover, and connect with properties that resonate with your dreams and aspirations.
        Here are a few key features and benefits you can expect from SnM Properties:

        1) Comprehensive Property Listings: Discover a vast range of properties available for sale or rent, including apartments, houses, condos, and commercial spaces. Each listing
        is an opportunity to uncover the story behind the property and envision the possibilities it holds.

        2) Advanced Search Filters: Utilize our advanced search filters to narrow down your options based on your specific preferences. Filter by location, price, property type,
        number of bedrooms, and more to find the properties that best suit your needs and resonate with your unique story.

        3) Saved Searches and Alerts: Save your favorite searches and set up personalized alerts to receive notifications whenever new properties matching your criteria are added
        to our platform. Stay one step ahead in the competitive real estate market and never miss an opportunity to discover a property that speaks to your story.

        4) Interactive Maps and Neighborhood Insights: Explore neighborhoods and surrounding areas with our interactive maps, which provide valuable information about local
        amenities, schools, transportation, and more. Immerse yourself in the context of each property's surroundings and uncover the elements that contribute to its unique narrative.

        5) Engaged Community: Join a vibrant community of homeowners, buyers, sellers, and real estate professionals who share their experiences, tips, and insights. Connect with
        like-minded individuals, ask questions, and receive guidance throughout your real estate journey. Together, we can create a rich tapestry of stories within the SnM Properties community.

        Remember, at SnM Properties, every property tells a unique story. We're committed to providing you with the tools, resources, and support to uncover the stories that resonate with
        you and make your real estate dreams a reality. We're constantly working on enhancing SnM Properties and adding new features to ensure you have the best possible experience. 
        Your feedback and suggestions are invaluable to us, so please don't hesitate to reach out to our support team if you have any questions, concerns, or ideas for improvement.
        To get started, simply log in to your SnM Properties account using the credentials you provided during the signup process. We encourage you to complete your profile, set your
        preferences, and begin your search for the perfect property that tells your unique story. Once again, welcome to SnM Properties - Where Every Property Tells a Unique Story! We're 
        thrilled to have you as part of our community, and we look forward to helping you discover the stories behind remarkable properties.
        Happy searching!

        Best regards,
        SnM Properties Team

    """
    em["From"] = sender
    em["Subject"] = "Welcome to SnM Properties - Where Every Property Tells a Unique Story!"
    em.set_content(message)
    s.send_message(em)
    s.quit()

def sendMsg(email,subject,msg):
    em = EmailMessage()
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    try:
        # Authentication
        s.login(sender, password)
    except:
        print('Incorrect Username or Password:\n')
        return 
    em["To"] = email
    em["From"] = sender
    em["Subject"] = subject
    em.set_content(msg)
    s.send_message(em)
    s.quit()

def checkAllAlerts():
    cursor.execute(f"SELECT * FROM alerts ")
    alerts =  cursor.fetchall()
    for a in alerts:
        property.createAlertProp(a[0])
    cursor.execute(""" 
            SELECT u.Email, a.Name, u.Name,  ap.property_count
            FROM alerts AS a
            JOIN (
              SELECT alert_id, COUNT(property_id) AS property_count
              FROM alert_prop
              GROUP BY alert_id
            ) AS ap ON a.Id = ap.alert_id
            JOIN user AS u ON u.Id = a.User_id;""")
    alertData = cursor.fetchall()
    print(len(alertData))
    for a in alertData:
        email = a[0]
        alertInfo = loads(a[1])
        name = a[2]
        propCount = a[3]
        subject = f"{propCount} New properties were found for your alert"
        # print(email)
        # print(alertInfo)
        # print(name)
        # print(propCount)
        msg = f"""Dear {name},
we have found {propCount} properties with the following filters
Price between {alertInfo['priceBetween']}
Area between {alertInfo['areaBetween']}
rooms between {alertInfo['roomsBetween']}
Listing Type {alertInfo['listing']}
Property Type {alertInfo['type']}
"""
        if 'city' in alertInfo:
            msg += f"""City {alertInfo['city']}
"""
        if 'location' in alertInfo:
            msg += f"""Location {alertInfo['location']}
"""
        msg +="""Login to view these and find your dream home
Best Regards,
SnM Properties team"""
        sendMsg(email=email,msg=msg,subject=subject)
        # print(msg)

if __name__ == "__main__":

    checkAllAlerts()
