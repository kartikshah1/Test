/** @jsx React.DOM */

var CourseInfo = React.createClass({
    mixins: [LoadMixin],

    getUrl: function() {
        return '/courseware/api/course/'+this.props.course+'/courseInfo/?format=json';
    },

    render: function() {
        if (!this.state.loaded) {
            return <LoadingBar />;
        }
        course_info = this.state.data;
        var st = '';
        var et = '';
        var eed = '';
        if (course_info.start_time) {
            st = (
                <div class="row">
                    <div class="col-md-4 lead no-margin">
                        Start Date
                    </div>
                    <div class="col-md-7">
                        {course_info.start_time}
                    </div>
                </div>
            );
        }
        if (course_info.end_time) {
            et = (
                <div class="row">
                    <div class="col-md-4 lead no-margin">
                        End Date
                    </div>
                    <div class="col-md-7">
                        {course_info.end_time}
                    </div>
                </div>
            );
        }
        if (course_info.end_enrollment_date) {
            eed = (
                <div class="row">
                    <div class="col-md-4 lead no-margin">
                        Enrollment End Date
                    </div>
                    <div class="col-md-7">
                        {course_info.end_enrollment_date}
                    </div>
                </div>
            );
        }
        return (
            <div class="panel panel-default">
                <div class="panel-heading lead no-margin">
                    Course Info
                </div>
                <div class="panel-body">
                    <div class="lead no-margin">
                        Description
                    </div>
                    <div>
                        <span dangerouslySetInnerHTML={{__html: converter.makeHtml(this.state.data.description)}} />
                    </div>
                    <br />
                    {st}
                    {et}
                    {eed}
                </div>
            </div>
        );
    },
});