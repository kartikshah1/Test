
// Showdown converter
var converter = new Showdown.converter();


/* Login **********************************************/

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function ajax_json_request(url, type, data) {
    csrftoken = getCookie('csrftoken');
    if (!(type=="GET" || type=="get")) {
        data["csrfmiddlewaretoken"] = csrftokenValue;
    }

    var request = $.ajax({
        url: url,
        type: type,
        data: data,
        timeout: 5000,
        contentType: "application/x-www-form-urlencoded",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        dataType: "html"
    });

    //On failure display error message
    request.fail(function(jqXHR, textStatus) {
    	if (jqXHR.status == 404) {
    		response = {detail: "Network error: Please check your internet connection"};
    	}
    	else {
    		response = jQuery.parseJSON(jqXHR.responseText);
    	}
        display_global_message(response.detail, "error");
    });

    return request;
}




/*
    Custom AJAX request (Supporting file upload)

    Use this function to upload a file to server using
    Ajax. Ideally, options.data should be a formData object.
    It can be constructed, for example, as follows:

    var formData = new FormData(formDOMNode);

    For more details see:
    http://stackoverflow.com/questions/166221/how-can-i-upload-files-asynchronously-with-jquery
    Also see implementation of the ImageUploader component for sample usage

    options = {
        url: '..',
        type: '..',
        data: '...',
        [beforeSend: function(xhr, settings),]
        [success: function(response),]
        [progressFunction: function(event),]
        [error: function(xhr, textStatus)]
    }

    progressFunction can be used to track the progress of the upload. Example:
    progressFunction = function (e){
    if(e.lengthComputable){
        $('progress').attr({value:e.loaded,max:e.total});
    }
}
*/
function ajax_custom_request(options){
    // Get the csrftoken
    csrftoken = getCookie('csrftoken');
    if (!(options.type=="GET" || options.type=="get")) {
        options.data["csrfmiddlewaretoken"] = csrftokenValue;
    }

    //atatch the progressHandlingFucntion at the right place
    progressFunction = function(){};
    if (options.progressFunction){
        progressFunction = options.progressFunction;
        delete options.progressFunction;
    }
    options.xhr = function() {  // Custom XMLHttpRequest
        var myXhr = $.ajaxSettings.xhr();
        if(myXhr.upload){ // Check if upload property exists
            // For handling the progress of the upload
            myXhr.upload.addEventListener('progress',
                progressFunction, false);
        }
        return myXhr;
    };

    // update beforeSend to send request header
    beforeSend = function(){}
    if (options.beforeSend) beforeSend = options.beforeSend;
    options.beforeSend = function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        beforeSend(xhr, settings);
    }

    // Options to tell jQuery not to process
    // data or worry about content-type.
    options.cache = false;
    options.contentType = false;
    options.processData = false;
    request = $.ajax(options);
    return request;
}


/********* Message Info *****************/

function display_global_message(message, type) {
    // Type can be : ["info", "success", "error", "warning"]
    if(type=="error") {
        type = "danger";
    }

    clearTimeout($("#message-text").stop().data('timer'));
    $("#message-text").fadeOut(function() {
    	$("#message-text").html(message);
    });
    $("#message-text").removeClass().addClass("alert alert-" + type);
    $("#message-text").fadeIn(function() {
        var elem = $(this);
        $.data(this, 'timer', setTimeout(function() {elem.fadeOut();}, 3000));
    });
}

