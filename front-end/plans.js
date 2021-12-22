var navLinks = document.getElementById('navLinks');
function showMenu() {
  var navLinks = document.getElementById('navLinks');
    navLinks.style.right = "0";

}
    function hideMenu() {
      var navLinks = document.getElementById('navLinks');
        navLinks.style.right = "-200px";
    }


function onBodyLoad() {
  const cards = document.querySelectorAll(".card");
  const scards = document.querySelectorAll(".scard");
  var signupFormDOM = document.getElementById('signup-form')
  var secondStep = document.getElementById('second-step')
    var thirdForm = document.getElementById('payment-form');
  signupFormDOM.style.display="none";
  secondStep.style.display="none";
  thirdForm.style.display="none";
  //console.log(cards.length);
    for (var i = 0; i < cards.length; i++) {
      console.log('cards' + i + cards[i]);
      cards[i].style.display="none";
      scards[i].style.display="none";
    }
}

function onChooseClick() {
  const cards = document.querySelectorAll(".card");
  var choice = document.getElementById('pc').value;
  console.log('Choice is '+choice);
  var signupFormDOM = document.getElementById('signup-form')

  for (var i = 0; i < choice; i++) {
      cards[i].style.display="inline";
    //cards[i].style.display="none";
  }
  signupFormDOM.style.display="inline";
  for(var i = 2; i <= parseInt(choice)+1; i++) {
    console.log('Currently in i = '+i)
    var bookstr = 'lbookid'+i
    var bookid = document.getElementById(bookstr);
    var paraString = "<b>Enter Booking ID for Passenger "+i+":</b>"
    bookid.innerHTML = paraString;
  }

  signupFormDOM.scrollIntoView();
}

function onNextClick() {
var secondForm = document.getElementById('second-step');
  secondForm.scrollIntoView();
}

function beginPayment() {
  var thirdForm = document.getElementById('payment-form');
  thirdForm.style.display="inline";
  var pDOM = document.getElementById('costs-and-plans');
  var costsArr = JSON.parse(localStorage.costs);
  var plansArr = JSON.parse(localStorage.plans);
  //costsArr = localStorage.getItem("costs");
  //plansArr = localStorage.getItem("plans");
  var pStr = "<p><b>";
  var sum = 0;
  for(var i = 0; i < costsArr.length; i++) {
    pStr+= plansArr[i]
    pStr += "             "
    pStr += costsArr[i]
    pStr+= " USD <br>"
    sum = sum + parseInt(costsArr[i])
  }
  pStr += "<hr>Total:      "+sum+ " USD</b></p>"
  pDOM.innerHTML = pStr;
  thirdForm.scrollIntoView();
}


function processPayment() {
  var url = "dashboard.html"
  window.location.href = url
  localStorage.setItem("paySuccess", "yes")

}
function setupDOMWithJSON(outputJson) {
  /*
  document.getElementById("fname").value = response.customer_Fname
  document.getElementById("lname").value = response.customerLname
  document.getElementById("gender").value = response.gender
  document.getElementById("nationality").value = response.customerNation
  document.getElementById("hnumber").value = response.houseNO.substring(1,response.houseNO.length - 1)
  document.getElementById("snumber").value = response.streetNO.substring(1,response.streetNO.length - 1)
  document.getElementById("sname").value = response.streetName
  document.getElementById("zipcode").value = response.zip
  document.getElementById("country").value = response.custcountry
  document.getElementById("ccode").value = response.ctcode
  document.getElementById("contact").value = response.contactNo.substring(1,response.contactNo.length - 1)
  document.getElementById("emailid").value = response.email
  document.getElementById("ecname").value = response.EmCName
  document.getElementById("eccode").value = response.EmCountry
  document.getElementById("econtact").value = response.EmCNo.substring(1,response.EmCNo.length - 1)

  document.getElementById("user-details").style.visibility = "visible";
  */
  console.log(outputJson.length)
  data = outputJson["data"];
  console.log(data);
  const scards = document.querySelectorAll(".scard");
  var choice = document.getElementById('pc').value;
  var secondForm = document.getElementById('second-step');
  for (var i = 0; i < choice; i++) {
      scards[i].style.display="inline";
    //cards[i].style.display="none";
  }
  secondForm.style.display="inline";
  console.log(document.getElementById("rarrtz"+1))
  console.log(document.getElementById("rarrtz1"))
  var costs = []
  var plans = []
  for(var i = 1; i <= parseInt(outputJson.length); i++) {
    newprice = 0.9*parseInt(data["Passenger"+i]["Planprice"])
    plans.push(data["Passenger"+i]["Insplan"])
    costs.push(newprice)
    document.getElementById("rfarrtz"+i).innerHTML = data["Passenger"+i]["ArrivalTimeZone"]
    document.getElementById("rbookid"+i).innerHTML = data["Passenger"+i]["BookingID"]
    document.getElementById("rsourceairport"+i).innerHTML = data["Passenger"+i]["SourceAirport"]
    document.getElementById("rdestairport"+i).innerHTML = data["Passenger"+i]["DestinationAirport"]
    document.getElementById("rmealplan"+i).innerHTML = data["Passenger"+i]["Meal"]
    document.getElementById("rcabin"+i).innerHTML = data["Passenger"+i]["Cabin"]
    document.getElementById("rinsplan"+i).innerHTML = data["Passenger"+i]["Insplan"] + ", " + data["Passenger"+i]["Planprice"] + " USD"
    document.getElementById("rfldept"+i).innerHTML = data["Passenger"+i]["FlightDeparture"]
    document.getElementById("rfldeptz"+i).innerHTML = data["Passenger"+i]["DepartureTimeZone"]
    document.getElementById("rfarrt"+i).innerHTML = data["Passenger"+i]["FlightArrival"]
    document.getElementById("fcarrier"+i).innerHTML = data["Passenger"+i]["FlightCarrier"]
    document.getElementById("rname"+i).innerHTML = data["Passenger"+i]["PassName"]
    document.getElementById("rmembership"+i).innerHTML = data["Passenger"+i]["Membership"] + " 10% discount"
    splAs = data["Passenger"+i]["SpecialAssistance"]
    console.log(Object.keys(splAs).length)
    var splAsStr = ''
    for(var j = 0; j < Object.keys(splAs).length; j++) {
      if(j == splAs.length-1) {
        splAsStr += splAs[j.toString()];
      }
      else {
        splAsStr += splAs[j.toString()] + ', ';
      }
    }
    console.log(splAsStr)
    document.getElementById("rsplass"+i).value = splAsStr
  }
  console.log(costs)
  console.log(plans)
  localStorage.plans = JSON.stringify(plans);
  localStorage.costs = JSON.stringify(costs);
  //localStorage.setItem("plans", plans)
  //localStorage.setItem("costs", costs)
  onNextClick()
}

function makePlanAPICall(bookingArray, choicesArray) {
  var jsonString = '{"length": "'+bookingArray.length+'", "data": {';

  for(var i = 0; i < bookingArray.length; i++) {
    jsonString= jsonString + '"Passenger'+(i+1)+'": {\"Bookid\": \"'+bookingArray[i]+'\", \"Choice\": \"' + choicesArray[i]
    if(i == bookingArray.length-1) {
      jsonString = jsonString + '\"}}}'
    } else {
      jsonString = jsonString + '\"},'
    }
  }
  console.log(jsonString)
  var jsonObj = JSON.parse(jsonString)
  console.log(jsonObj)
  const params = jsonObj
  const http = new XMLHttpRequest()
  var response = ''
  var outputJson = ''
  var status = 0;
  http.open('POST', 'http://127.0.0.1:5000/plan-a-trip')
  http.setRequestHeader('Content-type', 'application/json')
  http.send(JSON.stringify(params)) // Make sure to stringify
  http.onload = function() {
      // Do whatever with response
      console.log('xhttp')
      //console.log(http.responseText)
      //response = http.responseText;
      response = JSON.parse(http.responseText);
      if(response.status == 'success') {
        console.log(response.message)
        outputJson = response.message;
        setupDOMWithJSON(outputJson)
        status = 1;
        return name;
      }
      else {
        console.log("failure")
        console.log(response.message)
        //name = 'User';
        status = 0;
        return name;
  }
      }


}

function isDuplicateBookingID(bookingArray, bookID) {
  console.log(bookingArray)
  console.log(bookID)
  var flag = 0;
  for(var i = 0; i < bookingArray.length; i++) {
    if(bookID == bookingArray[i]) {
      flag = 1;
      break;
    }
  }
  if(flag == 1) {
    return true;
  }
  else {
    return false;
  }
}

function validateTrip() {
  console.log('in validateTrip')
  var choice = document.getElementById('pc').value;
  console.log(choice)
  var stat = document.getElementById('plan-status');
  stat.innerHTML="";
  var choicesArray = [];
  var bookingArray = [];
  var flag = 0;
  var choiceInt = parseInt(choice);
  for(var i = 1; i <= choiceInt+1; i++) {
    var bookstr = 'bookid'+i;
    console.log(bookstr)
    var choicestr = 'cbookid'+i;
    console.log(choicestr)
    var bookid = document.getElementById(bookstr);
    var choiceid = document.getElementById(choicestr);
    if(bookid.value.length == 0 || choiceid.value.length == 0) {
      console.log('Entered val')
      flag = 1;
      stat.innerHTML = "<p style=\"color:Tomato;\">Some of your values are empty. Please enter them.</p>"
      break;
    }
    else if(isDuplicateBookingID(bookingArray, bookid.value)) {
      flag = 1;
      stat.innerHTML = "<p style=\"color:Tomato;\">Do not enter duplicate values for booking ID.</p>"
      break;
    }
    else {
      bookingArray[i-1] = bookid.value;
      choicesArray[i-1] = choiceid.value;
    }
  }
  if(flag != 1) {
    console.log('Booking Array elements')
    for(var i = 0; i < bookingArray.length; i++) {
      console.log(bookingArray[i])
    }
    console.log('Choice Array elements')
    for(var i = 0; i < choicesArray.length; i++) {
      console.log(choicesArray[i])
    }
    makePlanAPICall(bookingArray, choicesArray)
  }
}
