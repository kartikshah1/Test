/** @jsx React.DOM */


// Showdown converter
var converter = new Showdown.converter();


var PersonalInfo = React.createClass({
    render: function() {
        var user_profile = JSON.parse(this.props.user_profile);
        return (
            <table class="table col-md-8">
                <tr>
                    <th>Gender</th>
                    <td>{user_profile.gender}</td>
                </tr>
                <tr>
                    <th>Date of Birth</th>
                    <td>{user_profile.dob}</td>
                </tr>
                <tr>
                    <th>City</th>
                    <td>{user_profile.city}</td>
                </tr>
                <tr>
                    <th>State</th>
                    <td>{user_profile.state}</td>
                </tr>
                <tr>
                    <th>Country</th>
                    <td>{user_profile.country}</td>
                </tr>
            </table>
        );
    }
});


var EditButton = React.createClass({
	render: function() {
		return (
			<div class="row">
				<a id="edit-image-btn" class="btn btn-primary pull-left" href={this.props.image_url}>
                <span class="glyphicon glyphicon-pencil"></span> Edit Image
                </a>
                <a id="edit-pi-btn" class="btn btn-primary pull-right" href={this.props.pi_url}>
					<span class="glyphicon glyphicon-pencil"></span> Edit Profile
				</a>
			</div>
		);
	}
});


var ProfileTop = React.createClass({
	render: function() {
        var user_profile = JSON.parse(this.props.user_profile);
        if (user_profile.photo != "/media/") {
            var image_url = user_profile.photo;
        }
        else {
            var image_url = this.props.default_image;
        }
		return (
			<div class="row">
				<table class="table col-md-8">
					<tr >
						<td width="30%">
							<img width="180px" height="180px" src={image_url} />
						</td>
						<td>
							<h2>{this.props.user_name}</h2>
							<p><i>{user_profile.about}</i></p><br/><br/>
							<p><b>Interests: </b>{user_profile.interests}</p>
						</td>
					</tr>
				</table>
			</div>
		);
	}
});

var OtherInfo = React.createClass({
	render: function() {
		return (
			<div id="course-list" class="row">
				<p><b>Courses: </b>{this.props.courses}</p>
			</div>
		);
	}
});

var Profile = React.createClass({
    render: function() {
        console.log('creating a profile div :'+this.props.user);
        return (
            <div class="container">
                <ProfileTop user_name={this.props.user_name} user_profile={this.props.user_profile}
                    default_image={this.props.default_image}/>
                <EditButton pi_url={this.props.pi_url} image_url={this.props.image_url}/>
                <PersonalInfo user_profile={this.props.user_profile}/>
            </div>
        );
    }
});
