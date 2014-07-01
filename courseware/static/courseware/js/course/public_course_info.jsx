/** @jsx React.DOM */

var CourseBody = React.createClass({

	handleClicks: function(event) {
		course = jQuery.parseJSON(this.props.course);
		url = "/courseware/api/course/" + course.id + "/register";
        options = {
            url: url,
            type: "GET",
            data: {},
            success: function(response) {
                location.reload();
            },
            error: function(xhr, textStatus) {
                console.log(xhr.responseText);
                display_global_message(xhr.responseText, "error");
            }
        }
        request = ajax_custom_request(options);
	},

	render: function() {
	 	return (
            <div>
            	<a onClick ={this.handleClicks} class="btn btn-primary tool-tip enrollbtn">
                 	Enroll
                </a>
            </div>
        );
	}
});
