

function passwordNotStrong(pwd) {
  var passw = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;
if(pwd.match(passw)) {
  return false;
}
else {
  return true;
}
}

function emailNotStrong(email) {
  if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)) {
    return false;
  }
  else {
    return true;
  }
}

function numberIncorrect(phone) {
  if(/^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im.test(phone)) {
    return false;
  }
  else {
    return true;
  }
}

function makeAPICall(street_no, house_no, street_name, zipcode, country, country_code, contact_no, email, gender, emcontact_name, firstName, lastName, nationality, emcontact_no, emcountry_code, first_p) {
  var dt = new Date();
  timestamp = dt.toISOString();
  const params = {
    "streetNO":street_no,
  "houseNO":house_no,
  "streetName":street_name,
  "zip":zipcode,
  "custcountry":country,
  "ctcode":country_code,
  "contactNo": contact_no,
  "email":email,
  "gender":gender,
  "EmCName":emcontact_name,
 "customer_Fname":firstName,
 "customer_Lname":lastName,
 "customerNation":nationality,
 "EmCNo":emcontact_no,
 "EmCountry":emcountry_code,
 "password": first_p
  }
  const http = new XMLHttpRequest()
  var response = ''
  var status = 0;
  var login_stat = document.getElementById('login-status')
  var signup_stat = document.getElementById('signup-status')
  http.open('POST', 'http://127.0.0.1:5000/sign-up')
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
        //login_stat.innerHTML = '<p>You have successfully signed up! Login with your credentials.</p>'
        window.location.href="loginPage.html?message=success";
        status = 1;
      }
      else {
        if(response.status=='401') {
          console.log("failure")

          signup_stat.innerHTML = "<p style=\"color:Tomato;\">The email you entered is already in use. Please use another email.</p>";
          status = 0;
        }
        else {
          console.log("failure")

          signup_stat.innerHTML = "<p style=\"color:Tomato;\">There is some error in the server. Please try again.</p>";
          status = 0;
        }
  }
      }
      http.onerror = function() {
        console.log("failure")

        signup_stat.innerHTML = "<p style=\"color:Tomato;\">There is some error in the server. Please try again.</p>";
        status = 0;
      }
}


function validateSignUp() {
  console.log('Hello, in VALIDATE')
  var first_p = document.getElementById('psw').value;
  var second_p = document.getElementById('psw-repeat').value;
  var stat = document.getElementById('signup-status');
  var first_name = document.getElementById('fname').value;
  var last_name = document.getElementById('lname').value;
  var gender = document.getElementById('gender').value;
  var nationality = document.getElementById('nationality').value;
  var house_no = document.getElementById('hnumber').value;
  var street_no = document.getElementById('snumber').value;
  var street_name = document.getElementById('sname').value;
  var zip = document.getElementById('zipcode').value;
  var country = document.getElementById('country').value;
  var country_code = document.getElementById('ccode').value;
  var contact_no = document.getElementById('contact').value;
  var email = document.getElementById('emailid').value;
  var emcontact_name = document.getElementById('ecname').value;
  var emcountry_code = document.getElementById('eccode').value;
  var emcontact_no = document.getElementById('econtact').value;
  var messageText = '';
  var flag = 0;
  var pwd_flag = 1;
  var values_flag = 1;

  console.log(first_name)
  if(house_no.length== 0 || street_name.length == 0 ||
     zip.length == 0 || country.length ==0 || country_code.length ==0 ||
     contact_no.length ==0 || email.length ==0 || gender.length == 0 ||
     emcontact_name.length == 0 || first_name.length == 0 ||
     last_name.length == 0 || nationality.length == 0 ||
     emcontact_no.length ==0 || emcountry_code.length == 0 || first_p.length == 0) {
       console.log('Entered first check')
       values_flag = 0;
       flag = 1;
       messageText+= "Some of your values are empty.<br>"
     }
  if(first_p != second_p) {
    console.log('Entered second check')
    pwd_flag = 0;
    flag = 1;
    messageText+= "Your passwords do not match.<br>"
  }
  if(pwd_flag && values_flag) {
    console.log('Entered third check')
    if(passwordNotStrong(first_p)){
      flag = 1;
      messageText+= "Your password is not strong.<br>"
    }
    if(emailNotStrong(email)) {
      flag = 1;
      messageText+= "Your email is invalid.<br>"
    }
    if(numberIncorrect(contact_no)) {
      flag = 1;
      messageText+= "Your contact number is invalid.<br>"
    }
    if(numberIncorrect(emcontact_no)) {
      flag = 1;
      messageText+= "Your emergency contact number is invalid.<br>"
    }
  }
  if(pwd_flag == 0 || flag == 1 || values_flag == 0) {
    console.log(messageText);
    stat.innerHTML = '<p style="color:Tomato;">'+messageText+'</p>';
  }
  else {
    makeAPICall(street_no, house_no, street_name, zip, country, country_code, contact_no, email, gender, emcontact_name, first_name, last_name, nationality, emcontact_no, emcountry_code, first_p)
  }
}

//var form = document.forms['signup_form']
//form.onsubmit = validateSignUp()
