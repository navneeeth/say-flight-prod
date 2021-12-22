#from flash import Flask
 #import dbCommands as dbCommands
from flask import Flask, render_template, jsonify, request
#from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin
import random
import string
import datetime
import json
import os
import time
import dbCommands

app = Flask(__name__)
CORS(app, support_credentials=True)
#app.debug = True




def logAPICall(name):
    timestamp = datetime.datetime.now()
    dbCommands.logAPICall(name, str(timestamp))


@app.route('/endpoints/endpoint-login/', methods=['POST'])
def endpoints_endpoint_login():
    logAPICall('e/endpoint_login')
    request_data = request.get_json()
    endpointID = request_data['endpointID']
    password = request_data['password']
    result = attemptLogin(endpointID, password)
    if(result == "success"):
        name = getNameFromEndpointID(endpointID)
        return jsonify({
        "status": "success",
        "message": name,
        "endpointID": endpointID
        })
    else:
        return jsonify({
        "status": "failure",
        "message": "Invalid credentials.",
        "endpointID": endpointID
        })

@app.route('/endpoints/create-endpoint/', methods=['POST'])
def endpoints_create_endpoint():
    logAPICall('e/create-endpoint')
    request_data = request.get_json()
    name = request_data['name']
    password = request_data['password']
    result = createEndpoint(name, password)
    return jsonify({
    "status": "success",
    "message": result,
    "name": name
    })

#signup

@app.route('/test', methods = ['POST', 'GET', 'OPTIONS'])
def hello():
    logAPICall('test')
    value = jsonify({
    "status": "success",
    "message": "hello"
    })
    value.headers.add('Access-Control-Allow-Origin', '*')
    value.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return value

def generateSNumber():
    randomNo = 's'
    randomNoChars = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(9)])
    randomNo = randomNo + randomNoChars
    print(randomNo)
    return randomNo

def generateCNumber():
    randomNo = random.randint(10000,99999)
    print(randomNo)
    return randomNo

def generateSessionID():
    sNo = generateSNumber()
    while(dbCommands.isDuplicateSNumber(sNo)):
        sNo = generateSNumber()
    return str(sNo)

def generateCustomerID():
    cNo = generateCNumber()
    while(dbCommands.isDuplicateCNumber(cNo)):
        cNo = generateCNumber()
    return cNo

def validateLogin(email, pwd, timestamp):
    if(dbCommands.checkIfEmailExists(email)):
        if(dbCommands.validateLogin(email, pwd)):
            sessionID = generateSessionID()
            dbCommands.recordLogin(email, sessionID, timestamp)
            return sessionID
        else:
            return 0;
    else:
        return 0;

@app.route('/validate-login', methods = ['POST', 'GET', 'OPTIONS'])
@cross_origin()
def validate_login():
    print('request')
    print(request)
    print(request.args)
    #print(request.args.get('email'))
    request_data = request.get_json()
    #request_data = json.loads(request.data)
    #print(request_data)
    print('Hey')
    entered_email = request_data['email']
    entered_pwd = request_data['pwd']
    entered_timestamp = request_data['timestamp']
    logAPICall('validate-login')
    val = validateLogin(entered_email, entered_pwd, entered_timestamp)
    if type(val) == int:
        value = jsonify({
        "status": "failure",
        "message": "Incorrect credentials."
        })

    else:
        value = jsonify({
        "status": "success",
        "message": str(val)
        })
    #value.headers.add('Access-Control-Allow-Origin', '*')
    #value.headers.add('Access-Control-Allow-Headers', 'Content-Type, Origin, X-Auth-Token')
    #value.headers.add('Access-Control-Expose-Headers', 'Content-Length, X-JSON')
    return value

def validate_signup(streetNO,houseNO,streetName,zip,custcountry,ctcode,contactNo,email,gender,EmCName,customer_Fname,customer_Lname,customerNation,EmCNo,EmCountry, pwd):
    customerid = generateCustomerID()
    if(dbCommands.insertIntoCustomer(customerid,streetNO,houseNO,streetName,zip,custcountry,ctcode,contactNo,email,gender,EmCName,customer_Fname,customer_Lname,customerNation,EmCNo,EmCountry)):
        dbCommands.loginAccess(email,pwd)
        return 1
    else:
        return 0
    #insert these values in the aj nk cust table
    #create a customer number generateCNumber()
    #call a db function called insertIntoCustomer
    #convert necessary strings to numbers
    #if(db.insertIntoCustomer()) {
    #insert a value in the login access table for the newly created email and pwd
    #return 1
    #}
    #else { return 0}


def emailAlreadyExists(email):
    if(dbCommands.checkIfEmailExists(email)):
        return True
    else:
        return False

@app.route('/sign-up', methods = ['POST', 'OPTIONS'])
@cross_origin()
def validatesignup():
   request_data = request.get_json()
   print(request_data)
   customerid = generateCustomerID()
   customer_Fname=request_data['customer_Fname']
   customer_Lname= request_data['customer_Lname']
   email = request_data['email']
   streetNO=request_data['streetNO']
   houseNO = request_data['houseNO']
   streetName = request_data['streetName']
   zip = request_data['zip']
   custcountry =request_data['custcountry']
   ctcode= request_data['ctcode']
   contactNo = request_data['contactNo']
   gender = request_data['gender']
   EmCNo = request_data['EmCNo']
   EmCName = request_data['EmCName']
   EmCountry = request_data['EmCountry']
   customerNation = request_data['customerNation']
   password = request_data['password']

   json_data = { "customer id":customerid,"street number":streetNO,"house number":houseNO,"street name":streetName,"zipcode":zip,"customer country":custcountry,"country code":ctcode,"contact number": contactNo,"email":email,"gender":gender,"emergency contact name":EmCName,
   "customer_Fname":customer_Fname,"customer_Lname":customer_Lname,"customer nationality":customerNation,"emergency contact number":EmCNo,"emergency country code":EmCountry,"password": password}
   #loginAccess('validatesignup') add changes in the brackets.
   if(emailAlreadyExists(email)):
        val = jsonify({
        "status": "401",
        "message": "Email already exists"
        })
        return val
   values = validate_signup(streetNO,houseNO,streetName,zip,custcountry,ctcode,contactNo,email,gender,EmCName,customer_Fname,customer_Lname,customerNation,EmCNo,EmCountry, password)
   if(values) != 0:
       val = jsonify({
       "status": "success",
       "message": "Insertion successful"
       })
   else:
       val = jsonify({
       "status": "failure",
       "message": "Insertion failed"
       })
   #val.headers.add('Access-Control-Allow-Origin', '*')
   #val.headers.add('Access-Control-Allow-Headers', 'Content-Type')
   return val

def extractJsonFromString(str):
    arr = str.split(",")
    custID=arr[0]
    streetNO=arr[1]
    houseNO=arr[2]
    streetName=arr[3]
    streetName=streetName[2:-1]
    zip=arr[4]
    custcountry=arr[5]
    custcountry=custcountry[2:-1]
    ctcode=arr[6]
    contactNo=arr[7]
    email=arr[8]
    email=email[2:-1]
    gender=arr[9]
    gender=gender[2:-1]
    EmCName=arr[10]
    EmCName=EmCName[2:-1]
    membership=arr[11]
    membership=membership[2:-1]
    customer_Fname=arr[12]
    customer_Fname=customer_Fname[2:-1]
    customerLname=arr[13]
    customerLname=customerLname[2:-1]
    customerNation=arr[14]
    customerNation=customerNation[2:-1]
    EmCNo=arr[15]
    EmCountry=arr[16]
    resultstr="{"+"\"custID\":"+"\""+custID+"\""+","+"\"streetNO\":"+"\""+streetNO+"\""+","+"\""+"houseNO\":"+"\""+houseNO+"\""+","+"\"streetName\":"+"\""+streetNO+"\""+","+"\"zip\":"+"\""+zip+"\""+","+"\"custcountry\":"+"\""+custcountry+"\""+","+"\"ctcode\":"+"\""+ctcode+"\""+","+"\"contactNo\":"+"\""+contactNo+"\""+","+"\"email\":"+"\""+email+"\""+","+"\"gender\":"+"\""+gender+"\""+","+"\"EmCName\":"+"\""+EmCName+"\""+","+"\"membership\":"+"\""+membership+"\""+","+"\"customer_Fname\":"+"\""+customer_Fname+"\""+","+"\"customerLname\":"+"\""+customerLname+"\""+","+"\"customerNation\":"+"\""+customerNation+"\""+","+"\"EmCNo\":"+"\""+EmCNo+"\""+","+"\"EmCountry\":"+"\""+EmCountry+"\""+"}";
    print(resultstr)
    print('The above is the final string')
    return resultstr
    #print(resultstr)
#teststr="62247, 1, 221, 'BakerStLondon', 98056, 'United Kingdom', 1, 9875678901,'abcde@gmail.com', 'Female', 'Navneeth', 'A', 'Anshika', 'Jain', 'Indian', 1234567892, 1"
#extractJsonFromString(teststr)
@app.route('/profile-data', methods=['POST','OPTIONS'])
@cross_origin()
def profile_data():
    request_data = request.get_json()
    sessID = request_data['sessionid']
    print(request_data)
    extracted_email = dbCommands.checkuser(sessID)
    if(extracted_email == 0):
        val = jsonify({
        "status": "401",
        "message": "Invalid session id"
        })
        return val
    else:
        resultedStr = dbCommands.fetchDataFromEmail(extracted_email)
        if(resultedStr == 0):
            val = jsonify({
            "status": "402",
            "message": "User data does not exist"
            })
            return val
        else:
            finalJson = extractJsonFromString(resultedStr)
            json_data= json.loads(finalJson)
            val = jsonify({
            "status": "success",
            "message": json_data
            })
            return val

def processInputString(data_received):
    length = int(data_received['length'])
    bookingIDs = []
    choices = []
    passenger_name = 'Passenger'
    for i in range(1, length+1):
        #print(data_received['data'][passenger_name+str(i)]['Bookid'])
        bookingIDs.append(int(data_received['data'][passenger_name+str(i)]['Bookid']))
        choices.append(int(data_received['data'][passenger_name+str(i)]['Choice']))
    #print(bookingIDs)
    #print(choices)
    return (bookingIDs, choices)

def retrieveFromBookingID(bookingIDList, choicesList):
    #get the following values from bookID
    #bookid, sourceair, destair,
    '''
    var jsonString = '{"length": "'+bookingArray.length+'", "data": {';
    jsonString= jsonString + '"Passenger'+(i+1)+'": {\"Bookid\": \"'+bookingArray[i]+'\", \"Choice\": \"' + choicesArray[i]
    if(i == bookingArray.length-1) {
      jsonString = jsonString + '\"}}}'
    } else {
      jsonString = jsonString + '\"},'
    }
    '''
    jsonData = '{"length": "'+str(len(bookingIDList))+'", "data": {'
    for i in range(0, len(bookingIDList)):
        bookingID = bookingIDList[i]
        choice = choicesList[i]
        airportName = dbCommands.getAirportNameFromBookID(bookingID)
        sourceAirport = dbCommands.getSourceAirportFromBookID(bookingID)
        destAirport = dbCommands.getDestAirportFromBookID(bookingID)
        meal = dbCommands.getMealFromBookID(bookingID)
        cabin = dbCommands.getCabinFromBookID(bookingID)
        splas_list = dbCommands.getSpecialAssistanceFromBookID(bookingID)
        ins_plan = dbCommands.getInsurancePlanFromID(choice)
        dept_time = dbCommands.getDepartureTime(bookingID)
        arr_time = dbCommands.getArrivalTime(bookingID)
        arr_time_zone = dbCommands.getArrivalTimeZone(bookingID)
        dept_time_zone = dbCommands.getDepartureTimeZone(bookingID)
        fullName = dbCommands.getFullNameFromBookID(bookingID)
        memName = dbCommands.getMembershipName(bookingID)
        planPrice = dbCommands.getPlanPrice(choice)
        jsonData = jsonData + '"Passenger'+str(i+1)+'": {\"BookingID\": \"'+str(bookingIDList[i])+'\", \"SourceAirport\": \"' + sourceAirport
        jsonData = jsonData + '\", \"DestinationAirport\": \"' + destAirport + '\", "Meal": "' + meal + '", "Cabin": "' + cabin
        jsonData = jsonData + '\", "SpecialAssistance": {'
        if(splas_list == 0):
            jsonData = jsonData + '}, '
        elif(len(splas_list) == 1):
            jsonData = jsonData + '"1": "'+str(splas_list[0])+'"}, '
        else:
            for j in range(0, len(splas_list)):
                if(j == len(splas_list)-1):
                    jsonData = jsonData + '"'+str(j+1)+'": "'+str(splas_list[j])+'"}, '
                else:
                    jsonData = jsonData + '"'+str(j+1)+'": "'+str(splas_list[j])+'",'
        jsonData = jsonData + '"Insplan": "' + str(ins_plan) + '", "FlightDeparture": "'+dept_time + '", "FlightArrival": "'+ arr_time
        jsonData = jsonData + '", "DepartureTimeZone": "' + dept_time_zone + '", "ArrivalTimeZone": "' + arr_time_zone + '", "FlightCarrier": "'
        jsonData = jsonData + airportName + '", "PassName": "' + fullName + '", "Planprice" : "' + planPrice + '", "Membership": "' + memName + '"}'
        if(not i == len(bookingIDList) - 1):
            jsonData = jsonData + ', '
    jsonData = jsonData + "}}"
    print(jsonData)
    '''
        bookingID = bookingID[i]
        choice = choicesList[i]
        airportName = dbCommands.getAirportNameFromBookID(bookingID)
        sourceAirport = dbCommands.getSourceAirportFromBookID(bookingID)
        destAirport = dbCommands.getDestAirportFromBookID(bookingID)
        meal = dbCommands.getMealFromBookID(bookingID)
        cabin = dbCommands.getCabinFromBookID(bookingID)
        splas_list = dbCommands.getSpecialAssistanceFromBookID(bookingID)
        ins_plan = dbCommands.getInsurancePlanFromID(choice)
        dept_time = dbCommands.getDepartureTime(bookingID)
        arr_time = dbCommands.getArrivalTime(bookingID)
        arr_time_zone = dbCommands.getArrivalTimeZone(bookingID)
        dept_time_zone = dbCommands.getDepartureTimeZone(bookingID)
        fullName = dbCommands.getFullNameFromBookID(bookingID)
        memName = dbCommands.getMembershipName(bookingID)
        '''

    return jsonData


@app.route('/plan-a-trip',methods=['POST','OPTIONS'])
@cross_origin()
def plan_a_trip():
    request_data = request.get_json()
    print('Printing req data')
    print(request_data)
    (bIDs, choices) = processInputString(request_data)
    print(bIDs)
    print(choices)
    jsonData = retrieveFromBookingID(bIDs, choices)
    jsonForm = json.loads(jsonData)
    #print(request_data['data']['Passenger1'])
    val = jsonify({
    "status": "success",
    "message": jsonForm
    })
    return val

@app.route('/trip-list',methods=['POST','OPTIONS'])
def triplist():
    request_data = request.get_json()
    print(request_data)
    if(dbCommands.checkuser(sessionid)):
        if(dbCommands.checkCustomer(sessionid)):
            if(dbCommands.passengerPassport(customerID)):
                dbCommands.iternaryInfo(passportno)
                SRairport=request_data['source airport']
                FLid= request_data['flight id']
                PpassNo=request_data['passport number']
                Mid=request_data['membership id']
                desAirport=request_data['destination airport']
                InsId= request_data['Insurance id']
                cabid= request_data['cabin id']
                json_data = {"source airport":SRairport,"Flight id":FLid,"Passport number":PpassNo,"Membership id":Mid,"destination airport":desAirport,"insurance id":InsId,"cabin id":cabid}














def getNameFromEmail(extracted_email):
    name = dbCommands.getFullNameFromEmail(extracted_email)
    if(name == 0):
        return 0
    else:
        return name


@app.route('/getNameFromSessionID', methods=['POST','OPTIONS'])
@cross_origin()
def getNameFromSessionID():
    request_data = request.get_json()
    sessID = request_data['sessID']
    extracted_email = dbCommands.checkuser(sessID)
    if(extracted_email == 0):
        val = jsonify({
        "status": "401",
        "message": "No data available"
        })
        return val
    else:
        full_name = getNameFromEmail(extracted_email)
        if(full_name == 0):
            val = jsonify({
            "status": "402",
            "message": "User name does not exist"
            })
            return val
        else:
            val = jsonify({
            "status": "success",
            "message": full_name
            })
            return val


if __name__ == '__main__':
   app.run()
