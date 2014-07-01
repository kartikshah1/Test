/** @jsx React.DOM */

var GenericForm = React.createClass({
    handleSave: function() {
        //disable the save button
        //this.refs.submit.getDOMNode().disable()
        data = {
            title: this.refs.title.getDOMNode().value.trim(),
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
                            <label class="control-label">Title</label>
                            <input name="title" type="text" class="form-control" ref="title" defaultValue={this.props.title} placeholder="Title"></input>
                        </div>
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

var AddPageForm = React.createClass({
    handleSave: function() {
        //disable the save button
        //this.refs.submit.getDOMNode().disable()
        data = {
            title: this.refs.title.getDOMNode().value.trim(),
            description: this.refs.description.getDOMNode().value.trim()
        };
        this.props.saveCallBack(data);
    },

    render: function() {
        return (
            <div class="panel panel-default">
                <div class="panel-heading">
                    {this.props.heading}
                </div>
                <div class="panel-body">
                    <form role="form">
                        <div class="form-group">
                            <label class="control-label">Title</label>
                            <input name="title" type="text" class="form-control" ref="title" placeholder="Title"></input>
                        </div>
                        <div class="form-group">
                            <label class="control-label">Description</label>
                            <WmdTextarea ref="description" placeholder="Add description here..." />
                        </div>
                        <br></br>
                        <div class="col-md-1 no-padding">
                            <button ref="submit" class="btn btn-primary" type="button" onClick={this.handleSave}>
                                Save
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        );
    }
});

var validateDeleteBtn = React.createClass({
    handleYes: function() {
        $(".modal-backdrop").remove();
        $("body").removeClass("modal-open");
        this.props.callback();
    },

    render: function () {
        return (
            <div class="modal fade" id={this.props.modal} tabindex="-1" role="dialog" aria-labelledby={this.props.label} aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                        <h4 class="modal-title">Confirm Deletion</h4>
                        </div>
                        <div class="modal-body">
                            Sure about deleting the {this.props.heading}?
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-default" data-dismiss="modal">No
                            </button>
                            <button type="button" data-dismiss="modal" onClick={this.handleYes} class="btn btn-danger">
                                Yes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

var DeregisterModal = React.createClass({
    handleYes: function() {
        $("body").removeClass("modal-open");
        $(".modal-backdrop").remove();
        this.props.callback();
    },

     render: function () {
        return (
            <div class="modal fade" id={this.props.modal} tabindex="-1" role="dialog" aria-labelledby={this.props.label} aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                        <h4 class="modal-title">Confirm unregistration</h4>
                        </div>
                        <div class="modal-body">
                            Sure about unregistering from {this.props.title}?
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-default" data-dismiss="modal">No
                            </button>
                            <button type="button" data-dismiss="modal" onClick={this.handleYes} class="btn btn-danger">
                                Yes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

var CourseDeleteModal = React.createClass({
    handleYes: function() {
        $("body").removeClass("modal-open");
        $(".modal-backdrop").remove();
        this.props.callback();
    },

     render: function () {
        return (
            <div class="modal fade" id={this.props.modal} tabindex="-1" role="dialog" aria-labelledby={this.props.label} aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                        <h4 class="modal-title">Confirm Deletion</h4>
                        </div>
                        <div class="modal-body">
                            Sure about deleting  {this.props.title}?
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-default" data-dismiss="modal">No
                            </button>
                            <button type="button" data-dismiss="modal" onClick={this.handleYes} class="btn btn-danger">
                                Yes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});