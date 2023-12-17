$(document).ready(function() {
  var $results = $('.results-content'),
    d, h, m,
    i = 0;

	sleep(5000);

	const params = new Proxy(new URLSearchParams(window.location.search), {
		get: (searchParams, prop) => searchParams.get(prop),
	});
    var username =  params.username;

	document.getElementById('home').onclick = function() {window.location = 'http://finalproject.landing.s3-website-us-east-1.amazonaws.com?username=' + username};
	document.getElementById('add-post').onclick = function() {window.location = 'http://finalproject.addpost.s3-website-us-east-1.amazonaws.com?username=' + username};
	document.getElementById('edit-profile').onclick = function() {window.location = 'http://finalproject.editprofile.s3-website-us-east-1.amazonaws.com?username=' + username};
	search();

	function sleep(milliseconds) {
	  var start = new Date().getTime();
	  for (var i = 0; i < 1e7; i++) {
		if ((new Date().getTime() - start) > milliseconds){
		  break;
		}
	  }
	}

  async function callGetPostsApi(username) {
    // params, body, additionalParams
    return sdk.searchPostsGet({q: 'username: ' + username}, {}, {});
  }


  async function search() {
    const params = new Proxy(new URLSearchParams(window.location.search), {
		get: (searchParams, prop) => searchParams.get(prop),
	});
    var username =  params.username;
    response = await callGetPostsApi(username)
	var data = response.data;
	if (data.results && data.results.length > 0){
		var results = data.results;
	}
	var row = 0
	for (let i = 0; i < results.length; i++){
		if (i%4 == 0){
			row = row + 1
			insertRow(row)
		}
		var username = results[i]['username'];
		var base = results[i]['base'];
		var caption = results[i]['caption'];
		var tags = results[i]['tags'];
		var url = results[i]['url'];
		insertPost(username, base, caption, tags, url, i, row);
	}
  }

  function insertRow(row){
	  var rowdiv = '<div id="row' + row + '"></div>'
	  document.getElementById('result-content').innerHTML += rowdiv;
	  return;
  }

  function insertPost(username, base, caption, tags, url, i, row) {
	var rowdiv = "row" + row
	console.log(rowdiv)
	var postdiv = '<div id="' + i + '"  style="width:175px; display:inline-block;"></div>'
	document.getElementById(rowdiv).innerHTML += postdiv;
	var image = '<img src=' + httpGet(url) + ' style="width:150px;height:150px;text-align:center;" />'
	var user_caption = '<p style="width:150px;text-align:center;">' + username + ': ' + caption + '</p>'
	var location = '<p style="width:150px;text-align:center;">@' + base + '</p>'
	var post_tags = '<p style="width:150px;text-align:center;">'
	tags_length = tags.length
	tags_substring = (tags.substring(1, tags_length-1))
	tags_list = tags_substring.split(',')
	for (let i = 0; i < tags_list.length; i++){
		tag = tags_list[i].trim()
		tag_length = tag.length
		cleaned_tag = tag.substring(1,tag_length-1)
		post_tags = post_tags + '#' + cleaned_tag + ' ';
	}
	post_tags = post_tags + '</p>';
	document.getElementById(i).innerHTML += image;
	document.getElementById(i).innerHTML += user_caption;
	document.getElementById(i).innerHTML += post_tags;
	document.getElementById(i).innerHTML += location;
	document.getElementById(i).style.border = "thin solid #000000";
	return
  }
  
function httpGet(theUrl)
  {
    var xmlHttp = null;

    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
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