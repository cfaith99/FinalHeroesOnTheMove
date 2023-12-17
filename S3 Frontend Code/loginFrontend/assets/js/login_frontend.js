$(document).ready(function() {
  var $results = $('.results-content'),
    d, h, m,
    i = 0;

   document.getElementById('loginlbl').style.visibility = "hidden";

  function callSearchUserAPI(username) {
    // params, body, additionalParams
    return sdk.searchUsersGet({q: username}, {}, {});
  }

  //checks if username and password are valid
  function validateEntries() {
	document.getElementById('loginlbl').style.visibility = "hidden";

    username =  document.getElementById('username').value;
    password = document.getElementById('password').value;
	var valid = true
    callSearchUserAPI(username)
      .then((response) => {
        console.log(response);
        var data = response.data;
		var results = data.results;

		//checks that username exists - if it does checks that password is correct
		console.log(results['username']);
		if (results['username'] == 'None') {
			document.getElementById('loginlbl').style.visibility = 'visible';
			valid = false;
		}
        else{
            if (results['password'] != password){
                document.getElementById('loginlbl').style.visibility = 'visible';
			    valid = false;
            }
        }
		if (valid){
			window.location = 'http://finalproject.landing.s3-website-us-east-1.amazonaws.com?username='+username;
		}
      })
      .catch((error) => {
        console.log('an error occurred', error);
      });
  }


  $(window).on('keydown', function(e) {
    if (e.which == 13) {
      validateEntries();
      return false;
    }
  })

  document.getElementById('signup').onclick = function() {window.location = 'http://finalproject.signup.s3-website-us-east-1.amazonaws.com'};
    document.getElementById('login').onclick = function() {validateEntries()};


});