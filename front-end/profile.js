var navLinks = document.getElementById('navLinks');
function showMenu() {
  var navLinks = document.getElementById('navLinks');
    navLinks.style.right = "0";

}
    function hideMenu() {
      var navLinks = document.getElementById('navLinks');
        navLinks.style.right = "-200px";
    }


function updateDOMWithData(response) {
  console.log('Response is')
  console.log(response.EmCName)
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
}


    function getProfileDataFromSessID(sessID) {
      const params = {
          "sessionid": sessID,
      }
      const http = new XMLHttpRequest()
      var response = ''
      var name = ''
      var status = 0;
      http.open('POST', 'http://127.0.0.1:5000/profile-data')
      http.setRequestHeader('Content-type', 'application/json')
      http.send(JSON.stringify(params)) // Make sure to stringify
      http.onload = function() {
          // Do whatever with response
          console.log('xhttp')
          //console.log(http.responseText)
          //response = http.responseText;
          response = JSON.parse(http.responseText);
          if(response.status == 'success') {
            console.log('Success')
            console.log(response.message)
            updateDOMWithData(response.message)
            name = response.message;
            status = 1;
            return name;
          }
          else {
            console.log("failure")
            console.log(response.message)
            name = 'User';
            status = 0;
            return name;
      }
          }
    }

function onBodyLoad() {
  var sess = localStorage.getItem("sessID");
  console.log('Sess is ')
  console.log(sess)
  getProfileDataFromSessID(sess)
}
