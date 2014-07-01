/** @jsx React.DOM */

var AddSection = React.createClass({
    addSection: function(data) {
        url = "/document/api/page/" + this.props.pageid + "/add_section/?format=json";
        request = ajax_json_request(url, "POST", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            this.props.callback(response);
            display_global_message("Successfully added the section at the bottom", "success");
            this.setState({showform: false});
        }.bind(this));
        request.fail(function(response) {
            response = jQuery.parseJSON(response.responseText);
            console.log(response);
            msg = ''
            for (k in response) {
                if (msg != '') {
                    msg = msg + " \n" + k + ":" + response[k][0];
                } else {
                    msg = k + ":" + response[k][0];
                }
            }
            display_global_message(msg, "error");
        });
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
            content = <GenericForm heading="Add Section" saveCallBack={this.addSection} cancelCallBack={this.handleCancelAdd}/>;
        }
        else {
            content = (
                <button onClick={this.handleAddClick} class="btn addSectionButton">
                    <span class="glyphicon glyphicon-plus-sign"></span>
                    Add Section
                </button>
            );
        }
        return (
            <span>{content}</span>
        );
    }
});

var Section = React.createClass({
    getInitialState: function() {
        return {
            showform: false,
            title: this.props.section.title,
            description: this.props.section.description
        };
    },

    handleEdit: function(data) {
        url = "/document/api/section/" + this.props.section.id + "/?format=json";
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            display_global_message("Successfully updated the section", "success");
            oldState = this.state;
            oldState['title'] = response.title;
            oldState['description'] = response.description;
            oldState['showform'] = false;
            this.setState(oldState);
        }.bind(this));
    },

    handleEditClick: function() {
        this.setState({showform: true});
    },

    handleCancelEdit: function() {
        this.setState({showform: false});
    },

    deleteSection: function() {
        url = "/document/api/section/" + this.props.section.id + "/?format=json";
        request = ajax_json_request(url, "DELETE",{});
        request.done(function(response) {
            display_global_message("Successfully deleted the section", "success");
            sectionid = "section_"+this.props.section.id;
            this.props.deleteCallBack(sectionid);
        }.bind(this));
    },

    render: function() {
        sectionid = "section_"+this.props.section.id;
        modal = sectionid+"Modal";
        href = "#"+modal;
        label = modal + "Label";
        if(this.state.showform) {
            content = <GenericForm heading="Edit Section" title={this.state.title} description={this.state.description} saveCallBack={this.handleEdit} cancelCallBack={this.handleCancelEdit}/>;
        }
        else {
            content = (
                <div>
                    <h4>
                        {this.state.title}
                        <span class="glyphicon glyphicon-edit icon" onClick={this.handleEditClick}></span>
                        <validateDeleteBtn label={label} modal={modal} callback={this.deleteSection} heading="section" />
                        <a data-toggle="modal" href={href}>
                            <span class="glyphicon glyphicon-trash icon"></span>
                        </a>
                    </h4>
                    <p>
                        <span dangerouslySetInnerHTML={{__html: converter.makeHtml(this.state.description)}} />
                    </p>
                </div>
            );
        }
        return (
            <li id={sectionid} class="section">
                {content}
            </li>
        );
    }
});

var Page = React.createClass({
    handleSortClick: function() {
        $( "#sortablesections" ).sortable({
            axis: 'y',
            cursor: "move",
            //containment: "parent",
            placeholder: "ui-state-highlight",
            start: function( event, ui ) {
                $(ui.item).addClass("ui-state-movable");
                $(ui.placeholder).css("height", $(ui.item).css("height"));
            },
            stop: function( event, ui ) {
                $(ui.item).removeClass("ui-state-movable");
            }
        });
        $("#sortablesections").sortable("enable");
        $( "#sortablesections" ).disableSelection();
        oldState = this.state;
        oldState['sectionorder'] = true;
        this.setState(oldState);
    },

    saveOrder: function() {
        v = $("#sortablesections").sortable("toArray");
        a = v.length;
        for(i=0; i< a;i++){
            v[i]=v[i].substring(8);
            v[i]=parseInt(v[i]);
        }
        data = {
            playlist: JSON.stringify(v)
        }
        url = "/document/api/page/" + this.props.id + "/reorder_sections/?format=json";
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response) {
            display_global_message("Successfully reordered the sections", "success");
            $("#sortablesections").sortable("disable");
            oldState = this.state;
            oldState['sectionorder'] = false;
            this.setState(oldState);
        }.bind(this));
    },

    deletePage: function() {
        url = "/document/api/page/" + this.props.id + "/?format=json";
        request = ajax_json_request(url, "DELETE", {});
        request.done(function(response) {
            this.props.deleteCallBack(this.props.id);
            display_global_message("The page was successfully deleted", "success");
        }.bind(this));
        request.complete(function(response) {
            if (response.status != 204) {
                display_global_message("The page could not be deleted", "error");
            }
        }.bind(this));
    },

    loadPage: function() {
        url = "/document/api/page/" + this.props.id + "/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            this.setState({content: response, loaded: true});
        }.bind(this));
    },

    getInitialState: function() {
        return {
            loaded: false,
            content: undefined,
            pageedit: false,
            sectionorder: false
        };
    },

    componentDidMount: function() {
        if (!this.state.loaded) {
            this.loadPage();
        }
        else {
            $("#sectionOrderSave").hide();
        }
    },

    componentDidUpdate: function() {
        if (!this.state.loaded) {
            this.loadPage();
        }
        else {
            if(this.state.sectionorder)
            {
                $("#sectionReorder").hide();
                $("#sectionOrderSave").show();
                $(".section").addClass("sortable-items");
            }
            else {
                $("#sectionReorder").show();
                $("#sectionOrderSave").hide();
                $(".section").removeClass("sortable-items");
            }
        }
    },

    componentWillReceiveProps: function() {
        this.setState({
            loaded: false,
            content: undefined,
            pageedit: false,
            sectionorder: false
        });
    },

    handleCancelEdit: function() {
        oldState = this.state;
        oldState['pageedit'] = false;
        this.setState(oldState);
    },

    handleEdit: function(data) {
        url = "/document/api/page/" + this.props.id + "/?format=json";
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            display_global_message("Successfully updated the page", "success");
            oldState = this.state;
            oldState['content'].title = response.title;
            oldState['content'].description = response.description;
            oldState['pageedit'] = false;
            this.setState(oldState);
            $("#sideList [value="+response.id+"]").text(response.title);
        }.bind(this));
    },

    handleClickEdit: function() {
        oldState = this.state;
        oldState['pageedit'] = true;
        this.setState(oldState);
    },

    handleAddSection: function(section) {
        oldState = this.state;
        oldState['content'].sections.push(section);
        this.setState(oldState);
    },

    handleDeleteSection: function(sectionid) {
        $("#"+sectionid).remove();
    },

    render: function() {
        if (!this.state.loaded) {
            return (
                <LoadingBar />
            );
        }
        else {
            var sections = this.state.content.sections.map(function (section) {
                    return (
                        <Section section={section} deleteCallBack={this.handleDeleteSection}/>
                    );
                }.bind(this)
            );
            var onemorebutton="";
            if(sections.length > 4) {
                onemorebutton = <AddSection pageid={this.props.id} callback={this.handleAddSection}/>;
            }
            if (this.state.pageedit) {
                page_header = (
                    <div>
                    <GenericForm title={this.state.content.title} description={this.state.content.description} heading="Edit Page" saveCallBack={this.handleEdit} cancelCallBack={this.handleCancelEdit}/>
                    </div>
                );
            }
            else {
                page_header = (
                    <div>
                    <h3>{this.state.content.title}{" "}
                        <button onClick={this.handleClickEdit} class="btn btn-default">
                            <span class="glyphicon glyphicon-edit"></span>
                            Edit
                        </button>
                        <div class="pull-right">
                            <validateDeleteBtn modal="myModal" lable="myModalLabel" callback={this.deletePage} heading="page"/>
                            <a data-toggle="modal" href="#myModal" class="btn btn-danger">
                                <span class="glyphicon glyphicon-trash"></span>
                                Delete
                            </a>
                        </div>
                    </h3>
                    <div dangerouslySetInnerHTML={{__html: converter.makeHtml(this.state.content.description)}} />
                    </div>
                );
            }
            return (
                <div class="mydocument">
                    {page_header}
                    <AddSection pageid={this.props.id} callback={this.handleAddSection}/>
                    <button id="sectionReorder" onClick={this.handleSortClick} class="btn btn-default sort-btn">
                        <span class="glyphicon glyphicon-sort"></span>
                        Reorder Sections
                    </button>
                    <button id="sectionOrderSave" onClick={this.saveOrder} class="btn btn-primary sort-btn">
                        <span class="glyphicon glyphicon-save"></span>
                        Save Current Order
                    </button>
                    <ul id="sortablesections">
                        {sections}
                    </ul>
                    {onemorebutton}
                </div>
            );
        }
    }
});