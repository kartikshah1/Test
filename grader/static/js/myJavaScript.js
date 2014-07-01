function view_callback(data){
  if (data.status == 'Success!'){
    $('#contenthere').html(data.status);
  }else{
    for (message in data.status){
      $('#contact_errors').append("<p><b>" + message + ":</b>" + data.status["message"] + "</p>");
    }
  }
}
function getView(ID){
  data = $(ID).serializeObject();
  Dajaxice.testing.send_message(view_callback, {'form':data});
  return false;
}
//ajaxify anchors
$(function() {
    $('a').click(function(e) {
    	if($(this).attr('ajaxify')) {
    		var newurl = this.href;
       	$.ajax({
            url: $(this).attr('ajaxify'),
            dataType:'html',
            cache: false,
            success : function(data){
 				    history.pushState(null, "", newurl);
				    //Create jQuery object from the response HTML.
				    var $response=$(data);

			    	//Query the jQuery object for the values
    				var oneval = $response.find('#contenthere');
    				var $title = $('title')
    				var doctitle = $response.filter('title').text();
    				document.title = doctitle;
				    //var subval = $response.filter('#sub').text();
				    $("#contenthere").html(oneval);
						}
        })
        return false;
    }
    else {
    	return true;
    }
    });
});

// Ajax autocomplete
$(function() {
  $("#id_name_or_id").autocomplete({
    source: "/courses/searchcourses/"
  });
});

