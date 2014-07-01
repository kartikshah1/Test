/** @jsx React.DOM */

/**
  * This allows instructor/content_developer to change the settings for course
  */

var CourseDetail = React.createClass ({

    base_url: '/courseware/api/course/',

    handleCategoryChange: function(category) {
        this.setState({category: category});
        return false;
    },

    getInitialState: function() {
        return {
            category: undefined,
        };
    },

    update_course: function() {
        url = this.base_url + this.props.data.id + "/?format=json";
        var fd = new FormData();
        fd.append('category', this.state.category);
        fd.append('title', this.refs.title.getDOMNode().value.trim());
        if(this.refs.image.getDOMNode().files[0]){
            fd.append('image', this.refs.image.getDOMNode().files[0]);
        }
        if (this.props.data.type == 'O') {
            fd.append('enrollment_type', this.refs.enrollment_type.getDOMNode().value.trim());
        }
        request = ajax_custom_request({
            url: url,
            type: "PATCH",
            data: fd,
            mimeType: 'multipart/form-data',
        });
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            window.location = "/courseware/course/" + response.id;
        }.bind(this));
        return false;
    },

    render: function() {
        data = this.props.data;
        return (
            <div class="panel panel-default">
                <div class="panel-heading">
                    Update Details
                </div>
                <div class="panel-body">
                    <form id="update_course" role="form" class="form-horizontal">
                        <fieldset>
                        <CategoryLoader callback={this.handleCategoryChange}
                            defaultCategory={data.category}/>
                        </fieldset>
                        <div class="form-group">
                            <label class="control-label col-md-2 col-md-offset-1">
                                Title</label>
                            <div class="col-md-7 col-md-offset-1">
                                <input name="title" type="text" class="form-control"
                                    ref="title" placeholder="Title"
                                    defaultValue={data.title}></input>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="control-label col-md-2 col-md-offset-1">
                                Course Image</label>
                            <div class="col-md-7 col-md-offset-1">
                                <input name="image" type="file" class="form-control"
                                    ref="image"></input>
                            </div>
                        </div>
                        {data.type == 'O' ?
                            <div class="form-group">
                                <label class="control-label col-md-3 col-md-offset-0">
                                    Enrollment Type</label>
                                <div class="col-md-7 col-md-offset-1">
                                    {data.enrollment_type == 'O'?
                                        <select ref="enrollment_type"
                                            name="enrollment_type"
                                            class="form-control">
                                                <option value="O" selected="selected">
                                                    Open</option>
                                                <option value="M">Moderated</option>
                                        </select>
                                    :
                                        <select ref="enrollment_type"
                                            name="enrollment_type"
                                            class="form-control">
                                            <option value="O">Open</option>
                                            <option value="M" selected="selected">
                                                Moderated</option>
                                        </select>
                                    }
                                </div>
                            </div>
                            : null
                        }
                        <div class="form-group">
                            <div class="col-md-2 col-md-offset-5  addcoursebutton">
                                <button ref="submit" class="btn btn-primary"
                                    type="button" onClick={this.update_course}>
                                    Update</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        );
    },
});

var CourseInfoEdit = React.createClass({
    base_url: '/courseware/api/courseinfo/',

    componentDidMount: function() {
        course_info = this.props.data.course_info;
        start_time = course_info.start_time? course_info.start_time : "+0d";
        end_time = course_info.end_time? course_info.end_time : "+0d";
        end_enrollment_date = course_info.end_enrollment_date? course_info.end_enrollment_date : "+0d";
        $(function() {
            $( "#start_time" ).datepicker({
                dateFormat: "yy-mm-dd",
                defaultDate: start_time,
                minDate: "+0d",
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
                onClose: function( selectedDate ) {
                    $( "#end_time" ).datepicker( "option", "minDate", selectedDate );
                    $( "#end_enrollment_date" ).datepicker( "option", "minDate", selectedDate );
                }
            });
            $( "#end_time" ).datepicker({
                dateFormat: "yy-mm-dd",
                defaultDate: end_time,
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
                onClose: function( selectedDate ) {
                    $( "#start_time" ).datepicker( "option", "maxDate", selectedDate );
                    $( "#end_enrollment_date" ).datepicker( "option", "maxDate", selectedDate );
                }
            });
            $( "#end_enrollment_date" ).datepicker({
                dateFormat: "yy-mm-dd",
                defaultDate: end_enrollment_date,
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
            });
        });
    },

    update_info: function() {
        url = this.base_url + this.props.data.course_info.id + "/?format=json";
        data = {
            start_time: this.refs.startTime.getDOMNode().value,
            end_time: this.refs.endTime.getDOMNode().value,
            end_enrollment_date: this.refs.endEnrollmentDate.getDOMNode().value,
            description: this.refs.courseDescription.getDOMNode().value,
        };
        request = ajax_json_request(url, "PATCH", data)
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            display_global_message("Updated Course Information", "success");
        });
        request.fail(function() {
            response = jQuery.parseJSON(response);
            display_global_message("Unable to update. Check input or try later", "error");
        });
    },

    render: function() {
        course_info = this.props.data.course_info;
        return (
            <div class="panel panel-default">
                <div class="panel-heading">
                    Update Settings
                </div>
                <div class="panel-body">
                    <form id="update_course" role="form" class="form-horizontal">
                        <fieldset>
                            <div class="form-group">
                                <label class="control-label col-md-2 col-md-offset-1">
                                    Start Date</label>
                                <div class="col-md-7 col-md-offset-1">
                                    <input type="text" id="start_time" name="start_time"
                                        class="form-control" ref="startTime"> </input>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="control-label col-md-2 col-md-offset-1">
                                    End Date</label>
                                <div class="col-md-7 col-md-offset-1">
                                    <input type="text" id="end_time" name="end_time"
                                        class="form-control" ref="endTime"> </input>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="control-label col-md-3 col-md-offset-0">
                                    Enrollment End Date</label>
                                <div class="col-md-7 col-md-offset-1">
                                    <input type="text" id="end_enrollment_date"
                                        name="end_enrollment_date"
                                        class="form-control" ref="endEnrollmentDate"> </input>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="control-label col-md-2 col-md-offset-1">
                                    Description</label>
                                <div class="col-md-7 col-md-offset-1">
                                    <div class="wmd-toolbox"></div>
                                    <div>
                                        <WmdTextarea name="course-description"
                                            ref="courseDescription" style={{height: '150px'}}
                                            placeholder="Description"
                                            defaultValue={course_info.description} />
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="col-md-2 col-md-offset-5  addcoursebutton">
                                    <button ref="submit" class="btn btn-primary"
                                        type="button" onClick={this.update_info}>
                                        Update</button>
                                </div>
                            </div>
                        </fieldset>
                    </form>
                </div>
            </div>
        );
    },
});

var CourseSettings = React.createClass({
    mixins: [LoadMixin],

    base_url: '/courseware/api/course/',

    getUrl: function() {
        url = this.base_url + this.props.courseid + "/?format=json";
        return url;
    },

    getInitialState: function() {
        return {
            loaded: false,
            data: undefined,
        };
    },

    publish_course: function() {
        url = this.base_url + this.props.courseid + "/publish/?format=json";
        request = ajax_json_request(url, "POST", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            display_global_message(response.msg, "success");
            $("#publish-course").fadeOut();
        });
        request.fail(function(response) {
            response = jQuery.parseJSON(response);
            display_global_message(response.error, "error");
        })
        return false;
    },

    render: function() {
        if (this.state.loaded) {
            data = this.state.data;
            course_info = data.course_info;
            return (
                <div>
                    {!course_info.is_published ?
                        <div class="row">
                            <div class="col-md-2 col-md-offset-10">
                                <button class="btn btn-primary addgroup-button pull-right"
                                    onClick={this.publish_course} id="publish-course">
                                    Publish </button>
                            </div>
                        </div>
                    :
                        null
                    }
                    <div class="row">
                        <div class="col-md-12">
                            <CourseDetail data={data} />
                            <CourseInfoEdit data={data} />
                        </div>
                    </div>
                </div>
            );
        } else {
            return <LoadingBar />;
        }
    },
});
