import mysql.connector
import time


db =mysql.connector.connect(host='test-db-mysql-travel-insurance-do-user-9282953-0.b.db.ondigitalocean.com',

database='defaultdb', user='doadmin', password='', port='25060', auth_plugin='mysql_native_password')

mycursor = db.cursor()


def logAPICall(apiCallName, timestamp):
    mycursor.execute('insert into logAPI values(\''+str(apiCallName)+'\', \''+str(timestamp)+'\');')
    db.commit()

def isDuplicateSNumber(sno):
    mycursor.execute('select * from loginRecords where sessionID=\''+sno+'\';')
    result = mycursor.fetchall()
    if result == []:
        return False
    else:
        return True

def isDuplicateCNumber(cno):
    mycursor.execute('select * from aj_nk_cust where custid=\''+str(cno)+'\';')
    result = mycursor.fetchall()
    if result == []:
        return False
    else:
        return True

def checkIfEmailExists(email):
    print(email)
    mycursor.execute('select * from loginAccess where email=\''+str(email)+'\';')
    result = mycursor.fetchall()
    if result == []:
        print('Returning false in check email exists')
        return False
    else:
        print('Returning true in check email exists')
        return True

def validateLogin(email, password):
    mycursor.execute('select * from loginAccess where email=\''+str(email)+'\' and pwd = \''+str(password)+'\';')
    result = mycursor.fetchall()
    if result == []:
        print('Returning false in login validation')
        return False
    else:
        print('Returning true in login validation')
        return True

def recordLogin(email, sessionID, timestamp):
    mycursor.execute('insert into loginRecords values(\''+str(sessionID)+'\', \''+str(email)+'\', \''+str(timestamp)+'\');')
    db.commit()

def insertIntoCustomer(customerid,streetNO,houseNO,streetName,zip,custcountry,ctcode,contactNo,email,gender,EmCName,customer_Fname,customer_Lname,customerNation,EmCNo,EmCountry):
    print('Generated ID is:')
    print(customerid)
    print('End')
    print(len(streetNO))
    if(len(streetNO)) == 0:
        streetNO = 0
    mycursor.execute('insert into aj_nk_cust values('+str(customerid)+', '+str(streetNO)+', '+str(houseNO)+', \''+str(streetName)+'\', '+str(zip)+', \''+str(custcountry)+'\', '+str(ctcode)+', '+str(contactNo)+', \''+str(email)
    +'\', \''+str(gender)+'\', \''+str(EmCName)+'\', \'A\', \''+str(customer_Fname)+'\', \''+str(customer_Lname)+'\' ,\''+str(customerNation)+'\', '+str(EmCNo)+', '+str(EmCountry)+');')
    db.commit()
    return True

def validate_signup(email,customerID):
    mycursor.execute('select * from loginAccess where email=\''+str(email)+'\' and customerID = \''+customerID+'\';')
    result = mycursor.fetchall()
    if result == []:
        return False
    else:
        return True

def loginAccess(newemail,newpass):
    mycursor.execute('insert into loginAccess values(\''+str(newemail)+'\', \''+str(newpass)+'\');')
    db.commit()

def checkuser(sessionid):
    mycursor.execute('select email from loginRecords where sessionID=\''+str(sessionid)+'\';')
    result = mycursor.fetchall()
    print(result)
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        return result

def fetchDataFromEmail(emailid):
    mycursor.execute('select * from aj_nk_cust where custemail=\''+str(emailid)+'\';')
    result = mycursor.fetchall()
    if result==[]:
        return 0
    #print(str(result))
    else:
        print('resulting string')
        result = str(result)
        result = result[2:-2]
        print(str(result))
        return result
#fetchDataFromEmail('qwerty@gmail.com')

def checkCustomer(sessionID):
    mycursor.execute('select customerID from aj_nk_cust where sessionid=\''+str(sessionid)+'\';')
    result = mycursor.fetchall()
    if result==[]:
        return False
    else:
        return True
def passengerPassport(customerID):
    mycursor.execute('select ppassno from aj_nk_pass where customerID=\''+int(customerID)+'\';')
    result = mycursor.fetchall()
    if result==[]:
        return False
    else:
        return True

def iternaryInfo(passportno):
    mycursor.execute('select * from aj_nk_fl_pass where passportno=\''+int(passportno)+'\';')
    result = mycursor.fetchall()
    if result==[]:
        return False
    else:
        return True



def getFullNameFromEmail(extracted_email):
    mycursor.execute('select custfname from aj_nk_cust where custemail=\''+str(extracted_email)+'\';')
    result = mycursor.fetchall()
    nameStr = ''
    print(result)
    if result==[]:
        return 0
    #print(str(result))
    else:
        result = str(result)
        result = result[3:-4]
        print(str(result))
        nameStr = nameStr + result
    mycursor.execute('select custlname from aj_nk_cust where custemail=\''+str(extracted_email)+'\';')
    result = mycursor.fetchall()
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    print('Final name is')
    print(nameStr)
    return nameStr

def getAirportNameFromBookID(bookID):
    statement = 'select AIRName from aj_nk_alines where AIRid = (select AIRid from aj_nk_flight where'
    statement = statement+' FLid = (select FLid from aj_nk_fl_pas where ItenaryID = ' +str(bookID)+ '));'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    #print('Final name is')
    print(nameStr)
    return nameStr

def getSourceAirportFromBookID(bookID):
    statement = 'select SRairport from aj_nk_fl_pas where ItenaryID = '+str(bookID)+';'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    #print('Final name is')
    print(nameStr)
    return nameStr

def getDestAirportFromBookID(bookID):
    statement = 'select desAirport from aj_nk_fl_pas where ItenaryID = '+str(bookID)+';'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    #print('Final name is')
    print(nameStr)
    return nameStr

def getMealFromBookID(bookID):
    statement = 'select MName from aj_nk_meal where mealid = (select mealid from aj_nk_fl_pas where ItenaryID = '+str(bookID)+');'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    #print('Final name is')
    print(nameStr)
    return nameStr

def getCabinFromBookID(bookID):
    statement = 'select cabname from aj_nk_cabin where cabid = (select cabid from aj_nk_fl_pas where ItenaryID = '+str(bookID)+');'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    #print('Final name is')
    print(nameStr)
    return nameStr

def getSpecialAssistanceFromBookID(bookID):
    statementStr = 'select splname from aj_nk_splas where splid in (select splid from aj_nk_sa where itenaryid='+str(bookID)+');'
    mycursor.execute(statementStr)
    result = mycursor.fetchall()
    if result==[]:
        return 0
    #print(str(result))
    else:
        print('resulting string')
        resultList = []
        for i in range(0, len(result)):
            resultList.append(str(result[i])[2:-3])
        print(resultList)
        return resultList

def getInsurancePlanFromID(insID):
    statement = 'select planname from aj_nk_plans where planid='+str(insID)+';'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    #print('Final name is')
    print(nameStr)
    return nameStr

def getDepartureTime(bookID):
    statement = 'select fldtime from aj_nk_flight where flid = (select flid from aj_nk_fl_pas where itenaryid ='+str(bookID)+');'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    #print('Final name is')
    print(nameStr)
    return nameStr

def getArrivalTime(bookID):
    statement = 'select flatime from aj_nk_flight where flid = (select flid from aj_nk_fl_pas where itenaryid ='+str(bookID)+');'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    #print('Final name is')
    print(nameStr)
    return nameStr

def getDepartureTimeZone(bookID):
    statement = 'select fldzone from aj_nk_flight where flid = (select flid from aj_nk_fl_pas where itenaryid ='+str(bookID)+');'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    #print('Final name is')
    print(nameStr)
    return nameStr

def getArrivalTimeZone(bookID):
    statement = 'select flazone from aj_nk_flight where flid = (select flid from aj_nk_fl_pas where itenaryid ='+str(bookID)+');'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    #print('Final name is')
    print(nameStr)
    return nameStr

def getFullNameFromBookID(bookID):
    mycursor.execute('select pfname from aj_nk_pass where ppassno = (select ppassno from aj_nk_fl_pas where itenaryid ='+str(bookID)+');')
    result = mycursor.fetchall()
    nameStr = ''
    print(result)
    if result==[]:
        return 0
    #print(str(result))
    else:
        result = str(result)
        result = result[3:-4]
        print(str(result))
        nameStr = nameStr + result
    mycursor.execute('select plname from aj_nk_pass where ppassno = (select ppassno from aj_nk_fl_pas where itenaryid ='+str(bookID)+');')
    result = mycursor.fetchall()
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    print('Final name is')
    print(nameStr)
    return nameStr

def getMembershipName(bookID):
    statement = 'select memname from passengers_with_membership where ppassno = (select ppassno from aj_nk_fl_pas where itenaryid = '+str(bookID)+');'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        result = str(result)
        result = result[3:-4]
        #print(str(result))
        nameStr = nameStr + ' ' + result
    #print('Final name is')
    print(nameStr)
    return nameStr

def getPlanPrice(planID):
    statement = 'select planprice from aj_nk_plans where planid ='+str(planID)+';'
    mycursor.execute(statement)
    result = mycursor.fetchall()
    nameStr = ''
    if result==[]:
        return 0
    else:
        #print(str(result))
        result = str(result)
        result = result[2:-3]
        #print(str(result))
        nameStr = nameStr + result
    #print('Final name is')
    print(nameStr)
    return nameStr

#getPlanPrice(1)
'''
select aj_nk_pass.PFname, aj_nk_pass.PLName, aj_nk_memship.MEMName, aj_nk_cust.CUSTID from
aj_nk_pass join aj_nk_cust on aj_nk_pass.CUSTID = aj_nk_cust.CUSTID join aj_nk_memship on
aj_nk_cust.CUSTID = aj_nk_memship.CUSTID where aj_nk_pass.CUSTID = 20;


getAirportNameFromBookID('21')
getSourceAirportFromBookID('21')
getDestAirportFromBookID('21')
getMealFromBookID('21')
getCabinFromBookID('21')
getSpecialAssistanceFromBookID('21')
getInsurancePlanFromID('6')
getDepartureTime('21')
getArrivalTime('21')
getArrivalTimeZone('21')
getDepartureTimeZone('21')
getFullNameFromBookID('21')
getMembershipName('21')
'''
