var navLinks = document.getElementById('navLinks');
function onBodyLoad() {
  var url = window.location+"";
  var message = url.substr((url.indexOf('=')+1));
  console.log('The message received is:');
  console.log(message);
  var login_stat = document.getElementById('login-status');
  if(message=='success') {
    login_stat.innerHTML = "<h3>You have successfully signed up! Log in with your new credentials!</h3>";
  }

}

function showMenu() {
    navLinks.style.right = "0";

}
    function hideMenu() {
        navLinks.style.right = "-200px";
    }

    function validateEmail(email) {
      if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))
  {
    return (true);
  }
  else {
    return false;
  }
    }

    function getUserNameFromSessionID(sessID) {
      const params = {
          "sessID": sessID,
      }
      const http = new XMLHttpRequest()
      var response = ''
      var name = ''
      var status = 0;
      http.open('POST', 'http://127.0.0.1:5000/getNameFromSessionID')
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
            name = response.message;
            var finalURL = "dashboard.html?name=" + name;
            window.location.href=finalURL;
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



function makeAPICall(email_entered, pwd_entered, stat) {
  var dt = new Date();
  timestamp = dt.toISOString();
  let data = {
    'email': email_entered,
    'pwd': pwd_entered,
    'timestamp': timestamp
  }
  //var form_data = new FormData();
//form_data.append( "json", JSON.stringify( data ) );

// Form fields, see IDs above
        const params = {
            "email": email_entered,
            "pwd": pwd_entered,
            "timestamp": timestamp
        }
        const http = new XMLHttpRequest()
        var response = ''
        var status = 0;
        http.open('POST', 'http://127.0.0.1:5000/validate-login')
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
              localStorage.setItem("sessID", response.message);
              var full_name = getUserNameFromSessionID(response.message);
              status = 1;
            }
            else {
              console.log("failure")
              console.log(response.message)
              stat.innerHTML = "<p>Invalid credentials. Please try again.</p>";
              status = 0;
        }
            }
            //alert(http.responseText)
            console.log('status is:');
            console.log(status);
            return status;
}

function testAPICall() {
  fetch('http://127.0.0.1:5000/test')
  .then((response) => {
  // handle the response
  console.log('Value received');
  return response.json();
  })
  .then((data) => {
  console.log('returned value');
    console.log(data);
  })
  .catch(function() {
  console.log('Some error');
  // handle the error
  });
}


function validateLogin() {

      //testAPICall()


      var stat = document.getElementById('login-status');
      var email_entered = document.getElementById('email').value;
      var pwd_entered = document.getElementById('pwd').value;
      if(pwd_entered.length == 0 || email_entered.length == 0) {
        stat.innerHTML = "<p>Your email or password cannot be empty.</p>";
      }
      else {
        if(validateEmail(email_entered)) {
          makeAPICall(email_entered, pwd_entered, stat)
        }
        else {
          stat.innerHTML = "<p>Please enter a valid email address.</p>";
        }
      }
  }

    const userAction = async () => {
      const response = await fetch('http://127.0.0.1:5000/test/');
      const myJson = await response.json(); //extract JSON from the http response
      console.log(myJson);
      // do something with myJson
    }
    /*
    const userAction = async () => {
  const response = await fetch('http://example.com/movies.json', {
    method: 'POST',
    body: myBody, // string or object
    headers: {
      'Content-Type': 'application/json'
    }
  });
  const myJson = await response.json(); //extract JSON from the http response
  // do something with myJson
}
*/
