/** @jsx React.DOM */

var PendingStudents = React.createClass({
    mixins: [LoadMixin],

    base_url: '/courseware/api/course/',

    getUrl: function() {
        url = this.base_url + this.props.courseid + "/pending_students/?format=json";
        return url;
    },

    approveStudents: function() {
        students = []
        pending_students = this.state.data.students;
        selected = $('input[name=student]').map(function(node, i) {
            return this.checked
        });
        for (var i = 0; i < selected.length; i++) {
            if (selected[i]) {
                students.push(pending_students[i]["user"]);
            }
        }
        data = {students: JSON.stringify(students)};
        url = this.base_url + this.props.courseid + "/approve/?format=json";
        request = ajax_json_request(url, "POST", data);
        request.done(function(response) {
            this.loadData();
            this.forceUpdate();
            this.props.updateApprovedStudents();
            console.log("Student List should reload now")
        }.bind(this));
        request.fail(function(response) {
            display_global_message("Error completing request. Try again later")
        }.bind(this));
    },

    toggleAll: function() {
        check = $('input[name=heading]')[0].checked;
        nodes = $('input[name=student]');
        for (var i = 0; i < nodes.length; i++) {
            nodes[i].checked = check;
        };
    },

    handleChange: function(event) {
        if (! event.target.checked) {
            $('input[name=heading]')[0].checked = false;
        }
    },

    getInitialState: function() {
        return {
            loaded: false,
            data: undefined
        };
    },

    render: function() {
        if (this.state.loaded) {
            if (! this.state.data.response) {
                return (
                    <div class="row" style={{'margin-top':'15px'}}>
                        <div class="col-md-10 col-md-offset-1">
                            <div class="alert alert-danger">
                                TextBook Course does not have Students
                            </div>
                        </div>
                    </div>
                );
            }
            pending_students = this.state.data.students;
            pending_students = pending_students.map( function(student, i) {
                return (
                    <div class="checkbox-row">
                        <div class="col-md-1  col-md-offset-0  checkbox-container">
                            <input onChange={this.handleChange} type="checkbox" name="student" key={"pending_student_" + i}> </input>
                        </div>
                        <div class="col-md-3  col-md-offset-0 username"> {student["username"]} </div>
                        <div class="col-md-4  col-md-offset-0 fullname"> {student["fullname"]} </div>
                        <div class="col-md-4  col-md-offset-0 email"> {student["email"]} </div>
                    </div>
                );
            }.bind(this));
            if (pending_students.length > 0) {
                return (
                    <div class="panel-collapse collapse in" id="pending-students">
                        <div class="row">
                            <div class="col-md-offset-9 col-md-2 no-padding">
                                <button ref="approve" onClick={this.approveStudents}
                                    class="btn btn-primary approve-btn" type="button"> Approve </button>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-10 col-md-offset-1 no-padding student-container">
                                <div class="student-heading">
                                    <div class="col-md-1 col-md-offset-0 checkbox-container">
                                        <input type="checkbox" name="heading" key="student_heading"
                                            onChange={this.toggleAll}>
                                        </input>
                                    </div>
                                    <div class="col-md-3 col-md-offset-0 username">
                                        User Name </div>
                                    <div class="col-md-4  col-md-offset-0 fullname">
                                        Full Name </div>
                                    <div class="col-md-4 col-md-offset-0 email">
                                        Email </div>
                                </div>
                                {pending_students}
                            </div>
                        </div>
                    </div>
                );
            } else {
                return (
                    <div class="panel-collapse collapse in" id="pending-students">
                        <div class="col-md-offset-9 col-md-2">
                            <button ref="approve" onClick={this.approveStudents}
                                class="btn btn-primary approve-btn" type="button"> Approve </button>
                        </div>
                        <div class="row">
                            <div class="col-md-10 col-md-offset-1">
                                <div class="alert alert-danger alert-dismissable">
                                    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                                    No pending Student to approve.
                                </div>
                            </div>
                        </div>
                    </div>
                );
            }
        } else {
            return <LoadingBar />
        }
    }

});

var ApprovedStudents = React.createClass({
    mixins: [LoadMixin],

    base_url: '/courseware/api/course/',

    getUrl: function() {
        url = this.base_url + this.props.courseid + "/approved_students/?format=json";
        return url;
    },

    componentWillReceiveProps: function(nextProps) {
        if (this.state.loaded){
            this.loadData();
            console.log("Updated Approved Students");
        }
    },

    getInitialState: function() {
        return {
            loaded: false,
            data: undefined
        };
    },

    render: function() {
        if (this.state.loaded) {
            if (!this.state.data.response){
                return (
                    <div class="row" style={{'margin-top':'15px'}}>
                        <div class="col-md-10 col-md-offset-1">
                            <div class="alert alert-danger">
                                TextBook Course does not have Students
                            </div>
                        </div>
                    </div>
                );
            }
            approved_students = this.state.data.students;
            approved_students = approved_students.map( function(student, i) {
                return (
                    <div class="student-row">
                        <span class="col-md-3 username"> {student["username"]} </span>
                        <span class="col-md-5 fullname"> {student["fullname"]} </span>
                        <span class="col-md-4 email"> {student["email"]} </span>
                    </div>
                );
            });
            if (approved_students.length > 0) {
                return (
                    <div class="row">
                        <div class="col-md-10 col-md-offset-1  student-container no-padding">
                            <div class="student-heading">
                                <span class="col-md-3 username"> User Name </span>
                                <span class="col-md-5 fullname"> Full Name </span>
                                <span class="col-md-4 email"> Email </span>
                            </div>
                            {approved_students}
                        </div>
                    </div>
                );
            } else {
                return (
                    <div class="row">
                        <div class="col-md-10 col-md-offset-1">
                            <div class="alert alert-danger alert-dismissable">
                                <button type="button" class="close"
                                    data-dismiss="alert" aria-hidden="true">&times;</button>
                                No Student registered yet.
                            </div>
                        </div>
                    </div>
                );
            }
        } else {
            return <LoadingBar />
        }
    }

});


var CourseStudent = React.createClass({

    updateApprovedStudents: function() {
        console.log("Sending signal to Approved Students");
        this.setState({loaded: false});
    },

    getInitialState: function(){
        return {
            loaded:false,
        };
    },

    render: function() {
        approved_students = <div>Some other content</div>;
        return (
        <div id="student" class="col-md-12">
            <div class="panel panel-default pending-students" id="pending-student-container">
                <div class="panel-heading" data-toggle="collapse" data-parent="#student"
                    data-target="#pending-students" id="pending-student-heading">
                    <span class="heading"> Pending Students </span>
                </div>
                <PendingStudents courseid={this.props.courseid} updateApprovedStudents={this.updateApprovedStudents}/>
            </div>
            <div class="panel panel-default approved-students" id="approved-student-container">
                <div class="panel-heading" data-toggle="collapse" data-parent="#student"
                    data-target="#approved-students" id="approved-student-heading">
                    <span class="heading"> Approved Students </span>
                </div>
                <div class="panel-collapse collapse" id="approved-students">
                    <ApprovedStudents courseid={this.props.courseid} loaded={this.state.loaded}/>
                </div>
            </div>
        </div>);
    }
});