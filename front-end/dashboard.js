var navLinks = document.getElementById('navLinks');



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
  var paySuccess = localStorage.getItem("paySuccess");
  var payDOM = document.getElementById('paySuccess')
  payDOM.innerHTML = ''
  console.log(paySuccess)
  if(paySuccess == null) {
    console.log(paySuccess)
    var navLinks = document.getElementById('navLinks');
    var sess = localStorage.getItem("sessID");
    console.log('Sess is ')
    console.log(sess)
    var url = window.location+"";
    var message = url.substr((url.indexOf('=')+1));
    console.log('The name received is:');
    console.log(message);
    message = message.replace(/%20/g, " ");
    var username_dom = document.getElementById('username');

      username_dom.innerHTML = "Hello, " + message + "!";
  }
  else {
    var payDOM = document.getElementById('paySuccess')
    localStorage.setItem("paySuccess", null);
    payDOM.innerHTML = 'You have successfully completed the payment!'
  }
}



function showMenu() {
  var navLinks = document.getElementById('navLinks');
    navLinks.style.right = "0";

}
    function hideMenu() {
      var navLinks = document.getElementById('navLinks');
        navLinks.style.right = "-200px";
    }

    window.addEventListener('beforeunload', function (e) {
    // Cancel the event
    //e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
    // Chrome requires returnValue to be set
    //a = confirm('Are you sure?')
    e.returnValue = "Are you sure you want to leave?";
  });

  function HandleBackFunctionality()
   {
       if(window.event)
      {
            if(window.event.clientX < 40 && window.event.clientY < 0)
           {
               alert("Browser back button is clicked...");
           }
           else
           {
               alert("Browser refresh button is clicked...");
           }
       }
       else
       {
            if(event.currentTarget.performance.navigation.type == 1)
           {
                alert("Browser refresh button is clicked...");
           }
           if(event.currentTarget.performance.navigation.type == 2)
          {
                alert("Browser back button is clicked...");
          }
       }
   }
