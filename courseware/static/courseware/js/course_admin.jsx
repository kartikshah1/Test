/** @jsx React.DOM */

var CourseCreate = React.createClass({
    base_url: "/courseware/api/",

    getInitialState: function() {
        return {
            category: undefined
        };
    },

    handleCategoryChange: function(category) {
        oldState = this.state;
        oldState.category = category;
        this.setState(oldState)
    },

    add_course: function() {
        url = this.base_url + "course/?format=json";
        data = {
            category: this.state.category,
            title: this.refs.title.getDOMNode().value.trim(),
            is_public: this.refs.is_textbook.getDOMNode().checked,
            //image: this.refs.image.getDOMNode().files[0],
            enrollment_type: this.refs.enrollment_type.getDOMNode().value.trim()
        };
        request = ajax_json_request(url, "POST", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            window.location = "/courseware/course/" + response.id;
        }.bind(this));
        return false;
    },

    render: function() {
            return (
                <form id="addcourse" role="form" class="form-horizontal">
                    <fieldset>
                    <CategoryLoader callback={this.handleCategoryChange} />
                    <div class="form-group">
                        <label class="control-label col-md-2 col-md-offset-1">Title</label>
                        <div class="col-md-7 col-md-offset-1">
                            <input name="title" type="text" class="form-control" ref="title" placeholder="Title"></input>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-2 col-md-offset-1">File input</label>
                        <div class="col-md-7 col-md-offset-1">
                            <input name="image" type="file" class="form-control" ref="image"></input>
                            <p class="help-block">Some Help Text </p>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-md-2 col-md-offset-1">
                            <button ref="submit" class="btn btn-primary" type="button" onClick={this.add_course}>Add Course</button>
                        </div>
                    </div>
                    </fieldset>
                </form>
            );
        }
});

var CourseAdmin = React.createClass({
    render: function() {
        return (
            <div class="panel panel-default">
                <div class="panel-heading">
                    Add Course
                    <span class="pull-right course-text-mute">Admin Panel</span>
                </div>
                <div class="panel-body">
                    <CourseCreate />
                </div>
            </div>
        );
    }
});

React.renderComponent(
    <CourseAdmin />, document.getElementById('course-add')
);
