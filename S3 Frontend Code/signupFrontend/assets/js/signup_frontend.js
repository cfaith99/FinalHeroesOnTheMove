$(document).ready(function() {
  var $results = $('.results-content'),
    d, h, m,
    i = 0;
	document.getElementById('usernamelbl').style.visibility = "hidden";
	document.getElementById('passwordlbl').style.visibility = "hidden";
	document.getElementById('firstlbl').style.visibility = "hidden";
	document.getElementById('lastlbl').style.visibility = "hidden";
	document.getElementById('baselbl').style.visibility = "hidden";


  function callUploadUserAPI(user_information) {
    // params, body, additionalParams
    return sdk.uploadUserPost({}, {
      information: user_information
      }, {});
  }
  
  function callSearchUserAPI(username) {
    // params, body, additionalParams
    return sdk.searchUsersGet({q: username}, {}, {});
  }

  //function callPutPhotoApi(file, photoKey, contentType, customLabels) {
    // params, body, additionalParams
    //console.log('file64:')
    //console.log(file)
    //return sdk.uploadFolderObjectPut({'Content-Type': 'text/base64', 'folder': 'assignment2.b2', 'object': photoKey, 'X-Api-Key': 'KVxqSUcSJn5AjNPQlx8f2aaDmq75wksiby98PCE1', 'x-amz-meta-customlabels': customLabels, 'body': file}, file, {});
  //}

  //checks if username is not used, that passwords match, and that all fields are filled in
  function validateEntries() {
	document.getElementById('usernamelbl').style.visibility = "hidden";
	document.getElementById('passwordlbl').style.visibility = "hidden";
	document.getElementById('firstlbl').style.visibility = "hidden";
	document.getElementById('lastlbl').style.visibility = "hidden";
	document.getElementById('baselbl').style.visibility = "hidden";

    username =  document.getElementById('username').value;
	var valid = true
    callSearchUserAPI(username)
      .then((response) => {
        console.log(response);
        var data = response.data;
		var results = data.results;

		//checks that username is valid
		console.log(results['username']);
		if (results['username'] != 'None' || username == "") {
			document.getElementById('usernamelbl').style.visibility = 'visible';
			valid = false;
		}

		//checks that passwords match
		password = document.getElementById('password').value;
		password2 = document.getElementById('password2').value;
		if (password == "" || password != password2){
			document.getElementById('passwordlbl').style.visibility = 'visible';
			valid = false;
		}

		//checks that all other fields have been entered
		firstname = document.getElementById('firstname').value;
		lastname = document.getElementById('lastname').value;
		base = document.getElementById('base').value;

		if (firstname == ""){
			document.getElementById('firstlbl').style.visibility = 'visible';
			valid = false;
		}
		if (lastname == ""){
			document.getElementById('lastlbl').style.visibility = 'visible';
			valid = false;
		}
		if (base == "Select"){
			document.getElementById('baselbl').style.visibility = 'visible';
			valid = false;
		}

		if (valid){
			information = firstname + ',' + lastname + ',' + base + ',' + username + ',' + password;
			resp = callUploadUserAPI(information);
			console.log(resp)
			window.location = 'http://finalproject.signin.s3-website-us-east-1.amazonaws.com';
		}
      })
      .catch((error) => {
        console.log('an error occurred', error);
      });
  }


  //$(window).on('keydown', function(e) {
   // if (e.which == 13) {
     // 	document.getElementById('result-content').innerHTML = '';
      //search();
      //return false;
    //}
  //})

  document.getElementById('signup').onclick = function() {validateEntries()};


  //function insertPicture(url) {
	//console.log('inserting ' + url);
	//var htmlURL = '<img src=' + url + ' style="width:100px;height:100px;" />'
	//console.log(htmlURL)
	//document.getElementById('result-content').innerHTML += htmlURL;
  //}

  async function uploadPicture() {
	var files = document.getElementById('file-upload').files;
	var file = files[0];
	var file64 = await getBase64(file);
	console.log('file64 1')
	console.log(file64)
	console.log(file.size);
	var photoKey = encodeURIComponent(file.name);
	var contentType = file.type;
	var bucket = 'assignment2.b2';
	var customLabels = document.getElementById('custom-labels').value
	console.log(customLabels)
	callPutPhotoApi(file64, photoKey, contentType, customLabels)
	document.getElementById('custom-labels').value = '';
	document.getElementById('file-upload').value = '';
  }

  async function getBase64(file){
	var reader = new FileReader();

	if (file){
		const reader = new FileReader();
		return new Promise(resolve => {
			reader.onload = ev => {
				resolve(ev.target.result)
			}

			reader.readAsDataURL(file)
		});
	}
  }

});