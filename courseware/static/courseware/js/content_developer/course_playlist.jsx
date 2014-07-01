/** @jsx React.DOM */

var AddGroupForm = React.createClass({
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
                    Add Group
                    <span class="pull-right">
                        <button type="button" onClick={this.props.closeCallBack} class="close">&times;</button>
                    </span>
                </div>
                <div class="panel-body">
                    <form id='addGroupsForm' role="form">
                        <div class="form-group">
                            <label class="control-label">Title</label>
                            <input name="title" type="text" class="form-control" ref="title" placeholder="Title"></input>
                        </div>
                        <div class="form-group">
                            <label class="control-label">Description</label>
                            <WmdTextarea class="form-control" rows="2" ref="description" placeholder="Add description here..." />
                        </div>
                        <div class="col-md-1 no-padding">
                        <button ref="submit" class="btn btn-primary" type="button" onClick={this.handleSave}>
                            Save
                        </button></div>
                        <div class="col-md-1">
                        <button type="button" onClick={this.props.closeCallBack} class="btn btn-danger">
                            Close
                        </button></div>
                    </form>
                </div>
            </div>
        );
    }
});

var AddConcept = React.createClass({
    addConcept: function(data) {
        url = "/courseware/api/group/" + this.props.id + "/add_concept/?format=json";
        request = ajax_json_request(url, "POST", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            this.props.callback(response);
            display_global_message("Successfully added the concept at the bottom", "success");
            this.setState({showform: false});
        }.bind(this));
    },

    getInitialState: function() {
        return {
            showform: false
        };
    },

    handleAddClick: function() {
        this.setState({showform: true});
    },

    handleCancelAdd: function() {
        this.setState({showform: false});
    },

    render: function() {
        if(this.state.showform) {
            content = <GenericForm heading="Add Concept" saveCallBack={this.addConcept} cancelCallBack={this.handleCancelAdd}/>;
        }
        else {
            content = (
                <button onClick={this.handleAddClick} class="btn addSectionButton">
                    <span class="glyphicon glyphicon-plus-sign"></span>
                    Add Concept
                </button>
            );
        }
        return (
            <span>{content}</span>
        );
    }
});

var Concept = React.createClass({
    publishConcept: function() {
        url = "/courseware/api/concept/" + this.props.concept.id + "/publish/?format=json";
        request = ajax_json_request(url, "POST",{});
        request.done(function(response) {
            response = JSON.parse(response);
            display_global_message(response.msg, "success");
            this.setState({published: ! this.state.published});
        }.bind(this));
    },

    deleteConcept: function() {
        url = "/courseware/api/concept/" + this.props.concept.id + "/?format=json";
        request = ajax_json_request(url, "DELETE",{});
        request.done(function(response) {
            display_global_message("Successfully deleted the concept", "success");
            conceptid = "concept_"+this.props.concept.id;
            this.props.deleteCallBack(conceptid);
        }.bind(this));
    },

    getInitialState: function() {
        return {published: this.props.concept.is_published};
    },

    render: function() {
        if (! this.state.published) {
            publish_button = "Publish"
        } else {
            publish_button = "Un-Publish"
        }
        return (
            <li id={"concept_"+this.props.concept.id} class={"concept"+this.props.group + " concept"}>
                <div class="row">
                    <div class="col-md-9 concept-title">
                        <a href={'/concept/'+this.props.concept.id +'/'}>
                            {this.props.concept.title}
                        </a>
                    </div>
                    <div class="col-md-2">
                        <a class="publish-text" href="#" onClick={this.publishConcept}>
                            {publish_button}
                        </a>
                    </div>
                    <div class="col-md-1">
                        <validateDeleteBtn label={"concept_"+this.props.concept.id+"Label"}
                            modal={"concept_"+this.props.concept.id+"Modal"}
                            callback={this.deleteConcept} heading="Concept" />
                        <a data-toggle="modal" href={"#concept_"+this.props.concept.id+"Modal"}>
                            <span class="glyphicon glyphicon-trash icon"></span>
                        </a>
                    </div>
                </div>
            </li>
        );
    }
});

var Group = React.createClass({
    mixins: [EditableMixin, SortableMixin],

    getInitialState: function() {
        return {
            loaded: false,
            concepts: undefined,
            title: this.props.group.title,
            description: this.props.group.description,
            order: false
        };
    },

    loadConcepts: function() {
        url = "/courseware/api/group/" + this.props.group.id + "/concepts/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState['concepts'] = response;
            oldState['loaded'] = true;
            this.setState(oldState);
        }.bind(this));
    },

    handleEdit: function(data) {
        url = "/courseware/api/group/" + this.props.group.id + "/?format=json";
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            display_global_message("Successfully updated the group", "success");
            oldState = this.state;
            oldState['title'] = response.title;
            oldState['description'] = response.description;
            oldState['showform'] = false;
            this.setState(oldState);
        }.bind(this));
    },

    deleteGroup: function() {
        url = "/courseware/api/group/" + this.props.group.id + "/?format=json";
        request = ajax_json_request(url, "DELETE",{});
        request.done(function(response) {
            display_global_message("Successfully deleted the group", "success");
            groupid = "group_"+this.props.group.id;
            this.props.deleteCallBack(groupid);
        }.bind(this));
    },

    componentDidMount: function() {
        if(!this.state.loaded) {
            this.loadConcepts();
        }
        else {
            $("#conceptOrderSave"+this.props.group.id).hide();
        }
    },

    componentDidUpdate: function() {
        if(!this.state.loaded) {
            this.loadConcepts();
        }
        else {
            if(this.state.order)
            {
                $("#conceptReorder"+this.props.group.id).hide();
                $("#conceptOrderSave"+this.props.group.id).show();
                $(".concept"+this.props.group.id).addClass("sortable-items");
            }
            else {
                $("#conceptReorder"+this.props.group.id).show();
                $("#conceptOrderSave"+this.props.group.id).hide();
                $(".concept"+this.props.group.id).removeClass("sortable-items");
            }
        }
    },

    handleAddConcept: function(concept) {
        oldState = this.state;
        oldState['concepts'].push(concept);
        this.setState(oldState);
    },

    handleDeleteConcept: function(conceptid) {
        //$("#"+conceptid).remove();
        v = parseInt(conceptid.substring(8));
        newconcepts = this.state.concepts.filter(function (concept) {
            return (parseInt(concept.id) != v);
        });
        oldState = this.state;
        oldState['concepts']=newconcepts;
        this.setState(oldState);
    },

    saveOrder: function(data) {
        url = "/courseware/api/group/" + this.props.group.id + "/reorder_concepts/?format=json";
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response) {
            display_global_message("Successfully reordered the pages", "success");
            this.saveOrderSuccess("#concepts"+this.props.group.id);
        }.bind(this));
    },

    render: function() {
        if(!this.state.loaded) {
            content = <LoadingBar />;
        }
        else if(this.state.showform) {
            content = <GenericForm heading="Edit Group" title={this.state.title} description={this.state.description} saveCallBack={this.handleEdit} cancelCallBack={this.handleCancelEdit}/>
        }
        else {
            var concepts = this.state.concepts.map(function (concept) {
                    return <Concept key={concept.id} concept={concept} group={this.props.group.id} deleteCallBack={this.handleDeleteConcept}/>;
                }.bind(this));
            var groupid = 'gr_' + this.props.group.id;
            content = (
                <div id={"group_"+this.props.group.id} class="panel panel-default group">
                    <div class="panel-heading" data-toggle="collapse" data-parent="#groups" data-target={"#"+groupid}>
                        <div class="panel-title group-heading">
                            {this.state.title}
                            <span class="glyphicon glyphicon-edit icon" onClick={this.handleEditClick}></span>
                            <validateDeleteBtn label={"group_"+this.props.group.id+"Label"} modal={"group_"+this.props.group.id+"Modal"} callback={this.deleteGroup} heading="Group" />
                            <a data-toggle="modal" href={"#group_"+this.props.group.id+"Modal"}>
                                <span class="glyphicon glyphicon-trash icon"></span>
                            </a>
                        </div>
                        <div class="muted">
                            <span dangerouslySetInnerHTML={{__html: converter.makeHtml(this.state.description)}} />
                        </div>
                    </div>
                    <div id={groupid} class="panel-collapse collapse">
                        <div class="panel-body group-inner">
                            <AddConcept id={this.props.group.id} callback={this.handleAddConcept}/>
                            <button id={"conceptReorder"+this.props.group.id} onClick={this.handleSortClick.bind(this, "#concepts"+this.props.group.id,"li.concept"+this.props.group.id)} class="btn btn-default sort-btn">
                                <span class="glyphicon glyphicon-sort"></span>
                                Reorder Concepts
                            </button>
                            <button id={"conceptOrderSave"+this.props.group.id} onClick={this.handleSaveOrder.bind(this, "#concepts"+this.props.group.id, 8)} class="btn btn-primary sort-btn">
                                <span class="glyphicon glyphicon-save"></span>
                                Save Current Order
                            </button>
                            <ul id={"concepts"+this.props.group.id} class="concepts">
                                {concepts}
                            </ul>
                        </div>
                    </div>
                </div>
            );
        }
        return content;
    }
});

var CoursePlaylist = React.createClass({
    mixins: [SortableMixin],

    addgroupform: function() {
        oldState = this.state;
        oldState['showform'] = true;
        oldState['showMessage'] = false;
        this.setState(oldState);
    },

    addGroup: function(data) {
        url = "/courseware/api/course/" + this.props.courseid + "/add_group/?format=json";
        request = ajax_json_request(url, "POST", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState['showform'] = false;
            oldState['showMessage'] = true;
            oldState['groups'].push(response);
            this.setState(oldState);
        }.bind(this));
    },

    handleDeleteGroup: function(groupid) {
        //$("#"+groupid).remove();
        v = parseInt(groupid.substring(6));
        newgroups = this.state.groups.filter(function (group) {
            return (parseInt(group.id) != v);
        });
        oldState = this.state;
        oldState['groups']=newgroups;
        this.setState(oldState);
    },

    closePanel: function() {
        oldState = this.state;
        oldState['showform'] = false;
        this.setState(oldState);
    },

    loadGroups: function() {
        url = "/courseware/api/course/" + this.props.courseid + "/groups?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState['groups'] = response;
            oldState['loaded'] = true;
            this.setState(oldState);
        }.bind(this));
    },

    getInitialState: function() {
        return {
            loaded: false,
            groups: undefined,
            showform: false,
            showMessage: false,
            order: false
        };
    },

    componentDidMount: function() {
        if(!this.state.loaded) {
            this.loadGroups();
        }
        $("#groupOrderSave").hide();
    },

    componentDidUpdate: function() {
        if(this.state.order) {
            $("#groupReorder").hide();
            $("#groupOrderSave").show();
        }
        else {
            $("#groupReorder").show();
            $("#groupOrderSave").hide();
        }
        if(this.state.loaded) {
            //$("#groups li").disableSelection();
            if(this.state.order) {
                /*
                $("#groups").sortable({
                axis: "y",
                handle: ".group-heading"
                });
                */
                $(".group").addClass("sortable-items");
            }
            else {
                $(".group").removeClass("sortable-items");
            }
        }
        else {
            this.loadGroups();
        }
    },

    saveOrder: function(data) {
        url = "/courseware/api/course/" + this.props.courseid + "/reorder_groups/?format=json";
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response) {
            display_global_message("Successfully reordered the pages", "success");
            this.saveOrderSuccess("#groups");
        }.bind(this));
    },

    myhandleSortClick: function() {
        this.handleSortClick("#groups", ".group");
    },

    myhandleSaveOrder: function() {
        this.handleSaveOrder("#groups", 6);
    },

    render: function() {
        message = '';
        addgroupform = '';
        if(this.state.showMessage) {
            message = (
                <div class="alert alert-success alert-dismissable">
                    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                    You have successfully added the group at the bottom.
                </div>);
        }
        if(this.state.showform) {
            addgroupform = <AddGroupForm courseid={this.props.courseid} saveCallBack={this.addGroup} closeCallBack={this.closePanel}/>;
        }
        if(!this.state.loaded) {
            groups = <LoadingBar />;
        }
        else {
            if (this.state.groups == "")
                groups = (
                    <div class="alert alert-danger alert-dismissable">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                        No content found in this course
                    </div>);
            else {
                groups = this.state.groups.map(
                function (group) {
                    return <Group key={group.id} deleteCallBack={this.handleDeleteGroup} group={group}/>;
                }.bind(this));
            }
        }
        return (
            <div>
                <div class="row">
                    <div class="col-md-8">
                        <h3>
                            Course Content
                        </h3>
                    </div>
                    <div class="col-md-4">
                        <button class="btn btn-primary addgroup-button pull-right" onClick={this.addgroupform}>
                            <span class="glyphicon glyphicon-plus-sign"></span>
                            &nbsp;&nbsp;&nbsp;Add Group
                        </button>
                    </div>
                </div>
                <div>{message}</div>
                <div id="addgroupform">
                    {addgroupform}
                </div>
                <div>
                    <button id="groupReorder" onClick={this.myhandleSortClick} class="btn btn-default group-sort-btn">
                            <span class="glyphicon glyphicon-sort"></span>
                            Reorder Groups
                    </button>
                    <button id="groupOrderSave" onClick={this.myhandleSaveOrder} class="btn btn-primary group-sort-btn">
                        <span class="glyphicon glyphicon-save"></span>
                        Save Current Order
                    </button>
                </div>
                <div class="panel-group" id="groups">
                    {groups}
                </div>
            </div>
        );
    }
});
