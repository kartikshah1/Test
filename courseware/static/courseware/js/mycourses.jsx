/** @jsx React.DOM */

/** Author : Shrikant Nagori **/

var Course = React.createClass({

	unRegister: function() {
		console.log("IN Unregister");
		url = "/courseware/api/course/" + this.props.course.id + "/deregister";
        request = ajax_json_request(url, "GET", {});
        console.log("Asds");
        request.done(function(response) {
        	console.log("ass");
            display_global_message("The course was successfully unenrolled", "success");
            $("#" + "course" + this.props.course.id).remove();
        }.bind(this));
        request.complete(function(response) {
        	console.log("ss")
            if (response.status != 200) {
                display_global_message("The course could not be unenrolled", "error");
            }
        }.bind(this));
	},

	setProgress: function() {
		course = this.props.course;
    	var div = document.getElementById("pgbar" + course.id);
		div.style.width = course.progress + "%";
		if(course.coursetag == 2){
			$('#' + "button" + course.id).attr("disabled", true);
		}
    },

    showProgress: function() {
    	$('.mycourseProgress').tooltip({
	      show: {
	        effect: "slideDown",
	        delay: 250
	      }
	    });
    },

	componentDidMount: function() {
        this.setProgress();
        this.showProgress();
    },

	render: function(){
		course = this.props.course;
		var progress = course.progress + "%"
    	var url = "/courseware/course/" + course.id;
    	var buttonurl = "/courseware/course/" + course.id;
    	var pgbarid = "pgbar" + course.id;
    	var buttonid = "button" + course.id;
    	var label = "label" + course.id;
    	var modal = "modal" + course.id;
    	var courseid = "course" + course.id;
    	var mymodal = "#" + modal;

    	var start_msg = "";
    	var button_msg = "";
    	var is_disabled = "";
    	if(course.coursetag == 1){
    		start_msg = "Course Started : " + course.start_date;
    		button_msg = "Take Class";
    	}
    	else if(course.coursetag == 2){
    		start_msg = "Course Starts : " + course.start_date;
    		button_msg = "Take Class";
    		buttonurl = "";
    	}
    	else {
    		start_msg = "Course Ended : " + course.end_date;
    		buttonurl = "/courseware/course/" + course.id +"/grades";
    		button_msg = "View Grades";
    	}
		return <div id={courseid} class = "row mycourseBox">
            		<div class = "row" >
            			<div class = "col-md-6 mycourseHeading">
            				 IIT BOMBAY
            			</div>
            			<div class = "col-md-6">
            				<div class = "mycourseDate">
            					{start_msg}
            				</div>
            			</div>
            		</div>
         			<div class = "row mycourseTitle">
            			<a href= {url}> {course.title}
            			</a>
            		</div>
            		<div class = "row mycourseActions">
            			<DeregisterModal label={label} modal={modal} title={course.title} callback={this.unRegister} />
            			<div class = "col-md-1 mycourseLink">
            				<a data-toggle="modal" href={mymodal}> Unregister
            				</a>
            			</div>
            			<div class = "col-md-2 mycourseLink">
            				<a href =""> Course Information
            				</a>
            			</div>
            			<div class = "col-md-2 col-md-offset-1">
            				<a id = {buttonid} href={buttonurl} class="btn btn-primary tool-tip mybtn" data-original-title="" >
								{button_msg}
							</a>
            			</div>
            			<div class = "col-md-5">
                			<div title = {progress} class = "mycourseProgress">
                				Course Progress
                			</div>
                			<div class="progress progress-striped  pgdiv">
								<div id= {pgbarid} class="progress-bar pgbar" role="progressbar" aria-valuenow={progress} aria-valuemin="0" aria-valuemax="100">
							 	</div>
							</div>
						</div>
            		</div>
        		</div>;
	}
});

var MyCourseBody = React.createClass({



	getInitialState: function() {
		console.log("enter the dragon");
        return {
            loaded: false,
        };
    },

	render: function() {
			console.log(this.props.courses);
			console.log("Hello");
			courses = jQuery.parseJSON(this.props.courses);
			console.log(courses);
            if(courses == ""){
                courses = (<div class="alert alert-danger alert-dismissable">No courses enrolled yet</div>);
            }
            else {
    			var courses = courses.map(
    				function (course) {
    	            	return <Course course={course} />;
                }.bind(this));
            }
	    return (
	        <div>
                <div>
                {courses}
                </div>
	        </div>
	    );
	}
});
