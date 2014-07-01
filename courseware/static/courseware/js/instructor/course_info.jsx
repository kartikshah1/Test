/** @jsx React.DOM */
var CourseDescriptionForm = React.createClass({
    handleSave: function() {
        data = {
            description: this.refs.description.getDOMNode().value.trim()
        };
        this.props.saveCallBack(data);
    },

    render: function() {
        return (
            <div class="panel panel-default">
                <div class="panel-heading">
                    {this.props.heading}
                    <span class="pull-right">
                        <button type="button" onClick={this.props.cancelCallBack} class="close">
                            &times;
                        </button>
                    </span>
                </div>
                <div class="panel-body">
                    <form role="form">
                        <div class="form-group">
                            <label class="control-label">Description</label>
                            <WmdTextarea class="form-control" rows="2" ref="description" defaultValue={this.props.description} placeholder="Add description here..." />
                        </div>
                        <div class="col-md-1 no-padding">
                            <button ref="submit" class="btn btn-primary" type="button" onClick={this.handleSave}>
                                Save
                            </button>
                        </div>
                        <div class="col-md-1">
                            <button type="button" onClick={this.props.cancelCallBack} class="btn btn-danger">
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        );
    }
});

var CourseInfo = React.createClass({
    base_url: '/courseware/api/courseinfo/',

    mixins: [LoadMixin],

    getInitialState: function() {
        return {
            loaded: false,
            showform: false,
            showMessage: false
        };
    },

    getUrl: function() {
        return '/courseware/api/course/'+this.props.course+'/courseInfo/?format=json';
    },

    handleEdit: function(){
        this.setState({showform: true});
    },

    handleCancel: function(){
        this.setState({showform: false});
    },

    updateDescription: function(data) {
        url = this.base_url + this.props.course + "/?format=json";
        oldState = this.state;
        desc = {
            description: data.description,
        };
        request = ajax_json_request(url, "PATCH", desc)
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            display_global_message("Updated Course Information", "success");
            oldState['showform'] = false;
            oldState['showMessage'] = true;
            oldState.data.description = desc.description;
            this.setState(oldState);
        }.bind(this));
        request.fail(function() {
            response = jQuery.parseJSON(response);
            display_global_message("Unable to update. Check input or try later", "error");
        });
    },

    render: function() {
        if (!this.state.loaded) {
            return <LoadingBar />;
        }
        if(this.state.showform) {
            content = <CourseDescriptionForm heading="Edit Description" description={course_info.description} saveCallBack={this.updateDescription} cancelCallBack={this.handleCancel}/>;
        }
        else{
        course_info = this.state.data;
        var st = '';
        var et = '';
        var eed = '';
            content = (
            <div class="panel panel-default">
                <div class="panel-heading lead no-margin">
                    Course Information
                </div>
                <div class="panel-body">
                    <div class="lead no-margin">
                        <span class='glyphicon glyphicon-edit pull-right icon' onClick={this.handleEdit}></span>
                    </div>
                    <div class="muted">
                        <span dangerouslySetInnerHTML={{__html: converter.makeHtml(this.state.data.description)}} />
                    </div>

                </div>
            </div>
            );
        }

        return (
            <span>{content}</span>
        );
    },
});
