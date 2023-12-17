$(document).ready(function() {
  var $results = $('.results-content'),
    d, h, m,
    i = 0;

	const params = new Proxy(new URLSearchParams(window.location.search), {
		get: (searchParams, prop) => searchParams.get(prop),
	});
    var username =  params.username;

	document.getElementById('add-post').onclick = function() {window.location = 'http://finalproject.addpost.s3-website-us-east-1.amazonaws.com?username=' + username};
	document.getElementById('profile').onclick = function() {window.location = 'http://finalproject.usercontent.s3-website-us-east-1.amazonaws.com?username=' + username};
	document.getElementById('base').style.visibility = "hidden";
	document.getElementById('filter').style.visibility = "hidden";
	onload();


  async function callGetPostsApiSearch(searchTerms) {
    // params, body, additionalParams
    return sdk.searchPostsGet({q: 'posts: ' + searchTerms + ' :username = ' + username}, {}, {});
  }

  async function callGetPostsApiHome(username) {
    // params, body, additionalParams
    return sdk.searchPostsGet({q: 'home: ' + username}, {}, {});
  }



  async function search(searchTerms) {
	document.getElementById('result-content').innerHTML = "";
	document.getElementById('base').value = "Select"
    const params = new Proxy(new URLSearchParams(window.location.search), {
		get: (searchParams, prop) => searchParams.get(prop),
	});
    var username =  params.username;
    response = await callGetPostsApiSearch(searchTerms)
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
		var like = results[i]['liked']
		insertPost(username, base, caption, tags, url, i, row, like);
	}
	addLike(results)
	document.getElementById('base').style.visibility = "visible";
	document.getElementById('filter').style.visibility = "visible";
	document.getElementById('filter').onclick = function(){
			filterPosts(results, document.getElementById('base').value)
	};
  }

  function filterPosts(results, base){
	  document.getElementById('result-content').innerHTML = "";
	  posts = []
	  for (let i=0; i< results.length; i++){
		  var postBase = results[i]['base']
		  if (base == postBase){
			  posts.push(results[i])
		  }
	  }
	  var row = 0
	  for (let i = 0; i < posts.length; i++){
		if (i%4 == 0){
			row = row + 1
			insertRow(row)
		}
		var username = posts[i]['username'];
		var postBase = posts[i]['base'];
		var caption = posts[i]['caption'];
		var tags = posts[i]['tags'];
		var url = posts[i]['url'];
		var like = posts[i]['liked']
		insertPost(username, postBase, caption, tags, url, i, row, like);
	}
	addLike(results)
  }

    async function onload() {
	const params = new Proxy(new URLSearchParams(window.location.search), {
		get: (searchParams, prop) => searchParams.get(prop),
	});
    var username =  params.username;
    response = await callGetPostsApiHome(username)
	var data = response.data;
	if (data.results && data.results.length > 0){
		var results = data.results;
	}
	var row = 0
	document.getElementById('loader').style.display = "none";
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
		var like = results[i]['liked']
		insertPost(username, base, caption, tags, url, i, row, like);
	}
	addLike(results)
  }

$(window).on('keydown', function(e) {
    if (e.which == 13) {
      	document.getElementById('result-content').innerHTML = '';
      	searchTerms = document.getElementById('search-input').value;
		search(searchTerms);
		document.getElementById('search-input').value = '';
		return false;
    }
  })

  function addLike(results){
	num = results.length
	for (let i = 0; i < num; i++){
		document.getElementById('heart' + i).onclick = function(){
			likePost(results[i]['username_time'], i)
		};
	}
  }

  function insertRow(row){
	  var rowdiv = '<div id="row' + row + '" style="display:flex" ></div>'
	  document.getElementById('result-content').innerHTML += rowdiv;
	  return;
  }

  function insertPost(username, base, caption, tags, url, i, row, like) {
  console.log(like)
	var rowdiv = "row" + row
	console.log(rowdiv)
	var postdiv = '<div id="' + i + '"  style="width:175px; display:inline-block;"></div>'
	document.getElementById(rowdiv).innerHTML += postdiv;
	var image = '<img src=' + httpGet(url) + ' style="width:150px;height:150px;text-align:center;" />'
	var user_caption = '<p style="width:150px;text-align:center;">' + username + ': ' + caption + '</p>'
	var location = '<p style="width:150px;text-align:center;">@' + base + '</p>'
	var post_tags = '<p style="width:150px;text-align:center;">'
	if (like){
		var heart = '<img id="heart' + i + '" src=Heart.png style="width:25px;height:20px" />'
		}
	else {
		var heart = '<img id="heart' + i + '" src=emptyHeart.png style="width:25px;height:20px" />'	}
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
	document.getElementById(i).innerHTML += heart;
	document.getElementById(i).innerHTML += user_caption;
	document.getElementById(i).innerHTML += post_tags;
	document.getElementById(i).innerHTML += location;
	document.getElementById(i).style.border = "thin solid #000000";
	return
  }

  function likePost(post_id, i){
	document.getElementById('heart' + i).src = 'Heart.png'
	return sdk.uploadLikePost({}, {
      information: [post_id, username]
      }, {});
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