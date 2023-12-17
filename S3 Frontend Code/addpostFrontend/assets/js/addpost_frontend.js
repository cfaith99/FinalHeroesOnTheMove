$(document).ready(function() {
  var $results = $('.results-content'),
    d, h, m,
    i = 0;
	document.getElementById('captionlbl').style.visibility = "hidden";
	document.getElementById('baselbl').style.visibility = "hidden";


  function callUploadContentAPI(post_information) {
    // params, body, additionalParams
    return sdk.uploadPostContentPost({}, {
      information: post_information
      }, {});
  }
  
  //function callSearchUserAPI(username) {
    // params, body, additionalParams
    //return sdk.searchUsersGet({q: username}, {}, {});
  //}

  async function callPutPhotoApi(file, contentType, bucket, photoKey) {
    // params, body, additionalParams
    console.log('file64:')
    console.log(file)
    return sdk.uploadPhotoBucketKeyPut({'Content-Type': 'text/base64', 'bucket': bucket, 'key': photoKey, 'body': file}, file, {});
  }

  //checks if username is not used, that passwords match, and that all fields are filled in
  function validateEntries() {
	document.getElementById('captionlbl').style.visibility = "hidden";
	document.getElementById('baselbl').style.visibility = "hidden";

	const params = new Proxy(new URLSearchParams(window.location.search), {
		get: (searchParams, prop) => searchParams.get(prop),
	});
    var username =  params.username;
	const time = Date.now();
	console.log(username);
	console.log(time);
	var valid = true


	//checks that caption and base are not empty
	caption = document.getElementById('caption').value;
	console.log(caption)
	base = document.getElementById('base').value;

	if (caption == ""){
		document.getElementById('captionlbl').style.visibility = 'visible';
		valid = false;
	}
	if (base == "Select"){
		document.getElementById('baselbl').style.visibility = 'visible';
		valid = false;
	}
	var send_caption = caption.replace(",", "*");
	if (valid){
		picture_files = document.getElementById('file-upload').files;
		picture = "";
		photoKey = "";
		if (picture_files.length != 0){
			picture = picture_files[0]
			photoKey = encodeURIComponent(picture.name);
		}
		var tags = document.getElementById('tags').value;
		var new_tags = tags.replace(",", "/");
		key = username + time;
		post_content = [key, username, photoKey,send_caption, base, new_tags];
		callUploadContentAPI(post_content);
		if (picture != ""){
			if (picture.type == 'image/png'){
				s3PhotoKey = key + '.png';
			}
			if (picture.type == 'image/jpg'){
				s3PhotoKey = key + '.jpg';
			}
			console.log(s3PhotoKey);
			uploadPicture(s3PhotoKey, username);
		}
	}
  }


  //$(window).on('keydown', function(e) {
   // if (e.which == 13) {
     // 	document.getElementById('result-content').innerHTML = '';
      //search();
      //return false;
    //}
  //})

  document.getElementById('post').onclick = function() {validateEntries()};


  //function insertPicture(url) {
	//console.log('inserting ' + url);
	//var htmlURL = '<img src=' + url + ' style="width:100px;height:100px;" />'
	//console.log(htmlURL)
	//document.getElementById('result-content').innerHTML += htmlURL;
  //}

  async function uploadPicture(photoKey, username) {
	var files = document.getElementById('file-upload').files;
	var file = files[0];
	var file64 = await getBase64(file);
	var contentType = file.type;
	console.log('file64 1')
	console.log(file64)
	console.log(file.size);
	var bucket = 'finalproject.postpictures';
	var results = await callPutPhotoApi(file64, contentType, bucket, photoKey);
	sleep(8000);
	window.location = 'http://finalproject.usercontent.s3-website-us-east-1.amazonaws.com?username=' + username;
  }

  function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
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