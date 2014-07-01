/** @jsx React.DOM */

/* File Created by : Aakash N S */


/*
This component encapsulates all the content
related to a concept. It's structure is:
([R] at the end denotes that the object is a
React Component and may have further substructure)

    Concept [R]
        courseTitle
        conceptInfoPanel
            groupTitle + conceptTitle
            ConceptDetails [R]
            ConceptPlaylist [R]
        LearningElement [R]
        ConceptInstructorArea [R]
*/

var EditConcept = React.createClass({
    base_url: "/concept/api/",

    mixins: [EditableMixin],

    /* Set which item (if any) is to be highlighted in the playlist */
    highlightItem: function(id, focus) {
        state = this.state;
        state.highlight = id;
        this.setState(state);
    },

    /* Set the current learning element */
    changeCurrent: function(new_data) {
        //console.log("Changing current");
        //console.log(new_data);
        state = this.state;
        state.current_item_data = new_data;
        this.setState(state);
        return false;
    },

    /* Loads the data for the concept from server */
    loadData: function() {
        url = this.base_url + "concept/" + this.props.conceptId + "/get_concept_page_data";
        $.ajax({
            url: url,
            dataType: 'json',
            mimeType: 'application/json',
            data: {format: 'json'},
            success: function(data) {
                state = this.state;
                state.loaded = true;
                state.data = data
                //state.current_item_data = state.data.playlist[state.data.current_element];
                this.setState(state);
            }.bind(this)
        });
    },

    changeTitle: function(data){
        state = this.state;
        state.data.title = data.title;
        this.setState(state);
    },

    reloadData: function() {
        state = this.state;
        state.loaded = false;
        this.setState(state);
        this.loadData();
    },

    getInitialState: function() {
        return {
            loaded: false,
            data: undefined,
            highlight: undefined,
            showform: true,
            current_item_data: undefined
        };
    },

    onPressEdit: function() {
        this.toggleEdit();
        this.reloadData();
    },

    render: function() {
        if (!this.state.loaded){
            return (
                <div>
                    <LoadingBar />
                </div>
            );
        }
        else{

            conceptNodes = this.state.data.group_playlist.map(function(item, i) {
                if (item.id != this.state.data.id)
                    return (
                        <li key={i}>
                            <a href={"/concept/" + item.id + "/"}>
                                {item.title}
                            </a>
                        </li>
                    );
                else
                    return (
                        <li key={i}>
                            <span>{item.title}</span>
                        </li>
                    );
            }.bind(this));

            groupNodes = this.state.data.course_playlist.map(function(item, i) {
                if (item.id != this.state.data.group)
                    return (
                        <li key={i}>
                            <a href={"/courseware/course/" + this.state.data.course}>
                                {item.title}
                            </a>
                        </li>
                    );
                else
                    return (
                        <li key={i}>
                            <span>{item.title}</span>
                        </li>
                    );
            }.bind(this));
            console.log('will render concept now');
            //console.log('curent item data is');
            //console.log(this.state.current_item_data);
            return (
                <div>
                    <h3 id="course-title">
                        <a href={"/courseware/course/"+ this.state.data.course}>
                            {this.state.data.course_title}
                        </a>
                    </h3>

                    <div class="panel panel-default" id="concept-info-panel">
                        <div class="panel-heading">
                            <ol class="breadcrumb concept-breadcrumb">
                              <li class="dropdown">
                                <a href={"/courseware/course/" + this.state.data.course}>
                                    {this.state.data.group_title}
                                </a>
                                <ul class="dropdown-menu">
                                        <li class="dropdown-header">Other Topics</li>
                                        <li class="divider"></li>
                                        {groupNodes}
                                </ul>
                              </li>
                              <li class="active dropdown">
                                {this.state.data.title}
                                <ul class="dropdown-menu">
                                        <li class="dropdown-header">Other Sections</li>
                                        <li class="divider"></li>
                                        {conceptNodes}
                                </ul>
                              </li>
                              <li id="concept-breadcrumb-caret" class="pull-right">
                                <div class="btn-group">
                                    {/*<button type="button"
                                        onClick={this.onPressEdit}
                                        class={"btn btn-default btn-xs " +
                                                (this.state.showform ? "active": "")} >
                                        Edit
                                    </button>*/null}
                                    <button type="button"
                                        onClick={this.reloadData}
                                        class="btn btn-default btn-xs">
                                        <span class="glyphicon glyphicon-refresh" />
                                    </button>
                                </div>
                              </li>
                            </ol>
                        </div>
                        <EditConceptDetails data={this.state.data}
                            clickCallback={this.changeCurrent}
                            focusCallback={this.highlightItem}
                            edit={this.state.showform}
                            changeTitleCallback={this.changeTitle} />
                        {/*<div class="panel-footer">
                            <ConceptPlaylist
                                conceptId={this.props.conceptId}
                                list={this.state.data.playlist}
                                current={this.state.data.current_element}
                                clickCallback={this.changeCurrent}
                                highlight = {this.state.highlight} />
                        </div>*/null}
                    </div>
                        {this.state.current_item_data ?
                            <LearningElementEdit data={this.state.current_item_data} />
                            : null
                        }
                    {/*<ConceptInstructorArea />
                    */""}
                </div>
            );
        }
    },

    /* Load the data when the component mounts */
    componentDidMount: function() {
        if (!this.state.loaded) this.loadData();
    }
});


/*  This component contains the description etc. for
    the concept. It is initially hidden, and can be shown
    by clicking on the caret on the top-right
    Strucure:
        ConceptDetails [R]
            conceptDescription | conceptImage
            learningElementsList
            conceptTitleDocument
            prevLink | nextLink
*/
var EditConceptDetails = React.createClass({
    /* Get the data for the "Prev" concept link */
    getPrevConcept: function() {
        list = this.props.data.group_playlist
        for (i = 1; i < list.length; i++){
            if (list[i].id == this.props.data.id) return i-1;
        }
    },

    /* Get the data for the "Next" concept link */
    getNextConcept: function() {
            list = this.props.data.group_playlist
            for (i = 0; i < list.length - 1; i++){
                if (list[i].id == this.props.data.id) return i+1;
        }
    },

    /*  Execute callback to highlight the PlaylistItem
        corresponding to the focussed element in LearingElementList
    */
    handleFocus: function(id) {
        this.props.focusCallback(id);
    },
    handleBlur: function(id) {
        this.props.focusCallback();
    },

    /* Execute callback to change the current learning element */
    handleClick: function(new_data) {
        this.props.clickCallback(new_data);
    },

    capitaliseFirstLetter: function(string){
        return string.charAt(0).toUpperCase() + string.slice(1);
    },

    getInitialState: function(){
        return {
            image: this.props.data.image,
        };
    },

    changeImage: function() {
        getExtension = function (filename) {
            var parts = filename.split('.');
            return parts[parts.length - 1];
        }

        isImage = function (filename) {
            var ext = getExtension(filename);
            switch (ext.toLowerCase()) {
            case 'jpg':
            case 'gif':
            case 'bmp':
            case 'png':
                //etc
                return true;
            }
            return false;
        }

        var progressHandlingFunction = function (e){
            if(e.lengthComputable){
                percent = 100*(e.loaded/e.total)+"%";
                this.refs.imageUploadProgress.getDOMNode().style.width = percent;
            }
        }.bind(this);

        var formData = new FormData(this.refs.imageForm.getDOMNode());

        if(!isImage(this.refs.imageUploadInput.getDOMNode().files[0].name)) {
            display_global_message("Invalid File Format", "error");
            $(this.refs.resetImageUploader.getDOMNode()).click();
            return false;
        }

        url = "/courseware/api/concept/" + this.props.data.id + "/?format=json";
        csrftoken = getCookie('csrftoken');
        formData["csrfmiddlewaretoken"] = csrftokenValue;

        console.log(formData);
        $.ajax({
            url: url,  //Server script to process data
            type: 'PATCH',
            xhr: function() {  // Custom XMLHttpRequest
                var myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload){ // Check if upload property exists
                    myXhr.upload.addEventListener('progress', progressHandlingFunction, false); // For handling the progress of the upload
                }
                return myXhr;
            },
            //Ajax events
            beforeSend: function(xhr, settings){
                this.refs.imageUploadProgressBar.getDOMNode().style.display = 'block';
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                console.log('about to send image');
            }.bind(this),
            success: function(response){
                console.log('image uploaded');
                state = this.state;
                state.image = '/media/' + response['image'];
                this.setState(state);
                setTimeout(function(){
                    this.refs.imageUploadProgressBar.getDOMNode().style.display = 'none';
                    this.refs.imageUploadProgress.getDOMNode().style.width = 0;
                    $(this.refs.resetImageUploader.getDOMNode()).click();

                }.bind(this), 1000);

            }.bind(this),
            error: function(){
                display_global_message("Unable to upload image", "error");
            },
            // Form data
            data: formData,
            //Options to tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false
        });
    },

    render: function() {
        if (!this.props.edit) {
            prev = this.props.data.group_playlist[this.getPrevConcept()];
            next = this.props.data.group_playlist[this.getNextConcept()];

            if (prev) prev = (
                <div class="pull-left" id="concept-details-prev">
                    <a href={"/concept/" + prev.id}>&laquo; Previous ({prev.title})</a>
                </div>
            );
            else prev = null

            if (next) next = (
                <div class="pull-right" id="concept-details-next">
                    <a href={"/concept/" + next.id}>Next ({next.title}) &raquo;</a>
                </div>
            );
            else next = null

            learningElementList = this.props.data.playlist.map(function(item, i) {
                return (
                    <li key={i}>
                        <a href={"#item"+i} onMouseEnter={this.handleFocus.bind(this, i)}
                        onMouseLeave={this.handleBlur.bind(this, i)}
                        onClick={this.handleClick.bind(this, item)} >
                            {item.content.title + " (" + this.capitaliseFirstLetter(item.type) + ")"}
                        </a>
                    </li>
                );
            }.bind(this));

            otherSections = this.props.data.title_document.sections.map(function(item, i){
                _desc = converter.makeHtml(item.description);
                return (
                    <li key={i}>
                        <h4>{item.title}</h4>
                        <div>
                            <span dangerouslySetInnerHTML={{__html: _desc}} />
                        </div>
                    </li>
                );
            });
            _conceptDesc = converter.makeHtml(this.props.data.description);
            return (
                <div id="concept-details">
                    <img src={this.props.data.image} class="pull-right concept-image"/>
                    <ul class="list-unstyled">
                        <li>
                            <h4>Summary</h4>
                            <div class="concept-summary">
                                <span dangerouslySetInnerHTML={{__html: _conceptDesc}} />
                            </div>
                        </li>
                        <li>
                            <h4>Contents</h4>
                            <ol>
                                {learningElementList}
                            </ol>
                        </li>
                        {otherSections}
                    </ul>
                    <div class="row">
                        {prev}
                        {next}
                    </div>
                </div>
            );
        }
        else {
            // EDIT MODE
            conceptSummary = <EditSection title={this.props.data.title}
                description={this.props.data.description}
                titleLabel="Concept Title"
                descriptionLabel="Concept Summary"
                noDelete={true}
                baseUrl="/courseware/api/concept/"
                id={this.props.data.id}
                changeCallback={this.props.changeTitleCallback} />;

            return(
                    <ul class="list-group">
                        <li class="list-group-item" style={{'overflow': 'auto'}}>
                            <div class="col-md-8">
                                <h4>Concept Details</h4>
                                {conceptSummary}
                            </div>
                            <div class="col-md-4">
                                <h4> Concept Image </h4>
                                <ImageUploader image={this.props.data.image}
                                    url = {"/courseware/api/concept/" + this.props.data.id + "/?format=json"}
                                    showProgress={true} />
                            </div>
                        </li>
                        {/*<li class="list-group-item">
                            <h4>Other Sections</h4>
                            <EditSections document={this.props.data.title_document} />
                        </li>*/null}
                        <li class="list-group-item">
                            <h4>Contents</h4>
                            <LearningElementsEdit
                                playlist={this.props.data.playlist}
                                focusCallback={this.props.focusCallback}
                                conceptId={this.props.data.id}
                                clickCallback={this.props.clickCallback} />
                        </li>
                    </ul>
            );
        }
    }
});




var LearningElementsEdit = React.createClass({
    mixins: [SortableMixin, SavedStatusMixin, BackgroundTransitionMixin],

    handleFocus: function(id) {
        this.props.focusCallback(id);
    },
    handleBlur: function(id) {
        this.props.focusCallback();
    },

    /* Execute callback to change the current learning element */
    handleClick: function(id) {
        this.props.clickCallback(id);
    },

    getInitialState: function() {
        return {
            order: false,
            add: false,
            playlist: this.props.playlist
        }
    },

    capitaliseFirstLetter: function(string){
        return string.charAt(0).toUpperCase() + string.slice(1);
    },

    addElement: function() {
        this.setState({add: true});
    },

    cancelAdd: function () {
        this.setState({add: false});
    },

    saveAdded: function(type, content) {
        playlist = this.state.playlist;
        playlist.push({
            type: type,
            content: content
        });
        this.setState({playlist : playlist, add: false});
    },

    sortClick: function() {
        this.handleSortClick("#learning-elements-ol", ".element_");
        this.toUnsaved();
    },

    handleSaveOrder2: function(id, keylength) {
        v = $(id).sortable("toArray");
        a = v.length;
        for(i=0; i< a;i++){
            tmp=v[i].substring(keylength);
            v[i] = []
            v[i].push(parseInt(tmp.substring(2)));
            v[i].push(parseInt(tmp[0]));
        }
        data = {
            playlist: JSON.stringify(v)
        }
        this.saveOrder(data);
    },
    /*
    saveOrder: function(data){
        console.log(data);
        this.saveOrderSuccess("#learning-elements-ol");
        this.toSaved();
    },
    */
    saveOrder: function(data){
        url = "/courseware/api/concept/" + this.props.conceptId + "/reorder/?format=json"
        this.toSaving();
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response){
            response = jQuery.parseJSON(response);
            console.log('reorderd learning elements are : ');
            console.log(response);
            this.setState({playlist: []});
            setTimeout(function() {this.setState({playlist: response})}.bind(this), 10);
            this.saveOrderSuccess("#learning-elements-ol");
            this.toSaved();
        }.bind(this));

        request.fail(function(){
            this.toUnsaved();
        }.bind(this));
    },

    onDelete: function(type, id) {
        playlist = this.state.playlist;
        playlist = playlist.filter(function(item) {
            return (item.type != type || item.content.id != id);
        });
        this.setState({playlist: playlist});
    },

    render: function() {
        /*
        learningElementList = this.state.playlist.map(function(item, i) {
            return (
                <li key={i}>
                    <a href={"#item"+i} onMouseEnter={this.handleFocus.bind(this, i)}
                    onMouseLeave={this.handleBlur.bind(this, i)}
                    onClick={this.handleClick.bind(this, i)} >
                        {item.content.title + " (" + this.capitaliseFirstLetter(item.type) + ")"}
                    </a>
                </li>
            );
        }.bind(this));
        */
        learningElementList = this.state.playlist.map(function(item, i){
            var id = {
                'video': 0,
                'quiz': 1,
                'document': 2
            };
            return (
                <li key={id[item.type]+ "_" + item.content.id}
                    id={"element_" + id[item.type]+ "_" + item.content.id} class="element_">
                    <LearningElementWithControls
                        data = {item}
                        content={item.content}
                        type={item.type}
                        conceptId={this.props.conceptId}
                        selectMode={this.state.order}
                        clickCallback={this.props.clickCallback}
                        deleteCallback={this.onDelete.bind(this,
                            item.type, item.content.id)} />
                </li>
            );
        }.bind(this));
        return(
            <div class="concept-learning-elements">
                <span class="help-block">
                    Click 'Add Content' to add Learning
                    Elements (Videos, Documents or Quizzes) to the Concept. <br/>
                    Click 'Reorder' to change the order in which the
                    elements are shown.
                </span>
                <div style={this.getBackgroundTransitionStyle()}>
                    <ol style={{overflow: 'auto'}}
                        id="learning-elements-ol"
                        class={this.state.order ? "list-unstyled" : ""} >
                        {learningElementList}
                    </ol>
                </div>
                {this.state.add ?
                    <AddLearningElement class="form-control"
                        conceptId={this.props.conceptId}
                        cancelCallback={this.cancelAdd}
                        saveCallback={this.saveAdded} /> :
                    (this.state.order ?
                        <div class="elements-control">
                            <button type="button"
                                class="btn btn-primary"
                                onClick={this.handleSaveOrder2.bind(this,
                                    "#learning-elements-ol", 8)} >
                            Save
                            </button>
                        </div> :
                        <div class="elements-control">
                            <button type="button"
                                class="btn btn-primary"
                                onClick={this.sortClick} >
                                Reorder
                            </button>
                            <button type="button"
                                class="btn btn-primary"
                                onClick={this.addElement}>
                                Add Content
                            </button>
                        </div>
                     )
                }
            </div>
        );
    }
});


var LearningElementWithControls = React.createClass({

    capitaliseFirstLetter: function(string){
        return string.charAt(0).toUpperCase() + string.slice(1);
    },

    onDelete: function(string){
        console.log('will delete now!');
        url = '/courseware/api/concept/' + this.props.conceptId +
            "/delete_element/?format=json";
        var id = {
                'video': 0,
                'quiz': 1,
                'document': 2
        };
        data = {
            'type' : id[this.props.type],
            'id' : this.props.content.id
        }
        console.log(data);
        request = ajax_json_request(url, "POST", data);
        request.done(function() {
            this.props.deleteCallback();
            this.props.clickCallback(undefined);
        }.bind(this));
    },

    handleClick: function(new_data) {
        return this.props.clickCallback(new_data);
    },

    render: function() {
        if (this.props.selectMode){
            rootStyle = {
                border: "1px solid #ddd",
                width: 400,
                padding: 5,
                margin: 5,
                backgroundColor: "#ffffff",
                boxSizing: 'border-box',
                WebkitTouchCallout: 'none',
                WebkitUserSelect: 'none',
                KhtmlUserSelect: 'none',
                MozUserSelect: 'none',
                MsUserSelect: 'none',
                userSelect: 'none'
            }

            return (
                <div style={rootStyle}>
                    {this.props.content.title + " (" +
                        this.capitaliseFirstLetter(this.props.type) + ")"}
                </div>
            );
        }
        modalId = "myModal_element_" + this.props.type+this.props.content.id;
        return (
            <div class="learning-element-control">
                <div class="element-title">
                <a href="#"
                        onClick={this.handleClick.bind(this, this.props.data)}>
                            {this.props.content.title + " (" +
                                this.capitaliseFirstLetter(this.props.type) + ")"}
                </a>
                </ div>
                <div class="controls">
                    <a href="#"
                        onClick={this.handleClick.bind(this, this.props.data)}>
                        <span class="glyphicon glyphicon-edit"> </span>
                    </a>
                    <a href={"#"+modalId}
                        data-toggle="modal">
                        <span class="glyphicon glyphicon-remove"> </span>
                    </a>
                    <validateDeleteBtn
                        modal={modalId}
                        label="myModalLabel"
                        callback={this.onDelete}
                        heading="element"/>
                </div>
            </div>
        );
    }
});


var AddLearningElement = React.createClass({
    mixins: [SavedStatusMixin, BackgroundTransitionMixin],

    getInitialState: function() {
        return {
            type: 'video'
        };
    },

    componentDidMount: function() {
        this.toUnsaved();
    },

    changeType: function(event) {
        this.setState({type: event.target.value})
    },

    onSubmit: function() {
      this.onSave();
      return false;
    },

    onSave: function() {
        var formData = new FormData(this.refs.form.getDOMNode());
        var url = '/courseware/api/concept/' + this.props.conceptId +
            '/add_' + this.state.type +'/?format=json';
        console.log(url);
        ajax_custom_request({
            url: url,
            type: 'POST',
            data: formData,
            beforeSend: function(xhr, settings){
                this.toSaving();
            }.bind(this),
            success: function(response){
                //console.log(response);
                //response = jQuery.parseJSON(response);
                this.toSaved();
                this.props.saveCallback(this.state.type, response);
            }.bind(this),
            error: function(xhr, textStatus){
                msg = "Unable to add learning element";
                display_global_message(msg, "error");
                this.toUnsaved();
            }.bind(this)
        });

    },

    render: function() {
        return(
            <div class="add-learning-element" style={this.getBackgroundTransitionStyle()}>
                <form class="form-horizontal" ref="form" onSubmit={this.onSubmit}>
                    <div class="mytablefull">
                        <div class="row">
                            <div class="col-md-8">
                                <div class="form-group">
                                    <label class="control-label col-sm-3">Content Type</label>
                                    <div class="col-sm-9">
                                        <select class="form-control"
                                            style={{width: 250}}
                                            onChange={this.changeType} >
                                          <option value="video"> Video</option>
                                          <option value="document"> Document</option>
                                          <option value="quiz"> Quiz</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label class="control-label col-sm-3">
                                        Title
                                    </label>
                                    <div class="col-sm-9">
                                        <input
                                            ref="title"
                                            type="text"
                                            name="title"
                                            class="form-control"
                                            placeholder="Enter title here.." />
                                    </div>
                                </div>
                                { this.state.type == 'video'?
                                    <div class="form-group">
                                        <label class="control-label col-sm-3">
                                            Video File
                                        </label>
                                        <div class="col-sm-9">
                                            <div class="fileinput fileinput-new"
                                                data-provides="fileinput">
                                                <span class="btn btn-primary btn-file">
                                                    <span class="fileinput-new">
                                                        Select file
                                                    </span>
                                                    <span class="fileinput-exists">
                                                        Change
                                                    </span>
                                                    <input type="file" name="video_file" />
                                                </span>
                                                <span class="fileinput-filename"></span>
                                                <a href="#"
                                                    class="close fileinput-exists"
                                                    data-dismiss="fileinput"
                                                    style={{float: 'none'}}>
                                                    &times;
                                                </a>
                                            </div>
                                        </div>
                                        <label class="control-label col-sm-3">
                                            Camtasia Config File
                                        </label>
                                        <div class="col-sm-9">
                                            <div class="fileinput fileinput-new"
                                                data-provides="fileinput">
                                                <span class="btn btn-primary btn-file">
                                                    <span class="fileinput-new">
                                                        Select file
                                                    </span>
                                                    <span class="fileinput-exists">
                                                        Change
                                                    </span>
                                                    <input type="file" name="video_config_file" />
                                                </span>
                                                <span class="fileinput-filename"></span>
                                                <a href="#"
                                                    class="close fileinput-exists"
                                                    data-dismiss="fileinput"
                                                    style={{float: 'none'}}>
                                                    &times;
                                                </a>
                                            </div>
                                        </div>
                                        <label class="control-label col-sm-3">
                                            Slides etc.
                                        </label>
                                        <div class="col-sm-9">
                                            <div class="fileinput fileinput-new"
                                                data-provides="fileinput">
                                                <span class="btn btn-primary btn-file">
                                                    <span class="fileinput-new">
                                                        Select file
                                                    </span>
                                                    <span class="fileinput-exists">
                                                        Change
                                                    </span>
                                                    <input type="file" name="other_file" />
                                                </span>
                                                <span class="fileinput-filename"></span>
                                                <a href="#"
                                                    class="close fileinput-exists"
                                                    data-dismiss="fileinput"
                                                    style={{float: 'none'}}>
                                                    &times;
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                    : null }
                            </div>
                            <div class="col-md-3">
                                <div class="pull-right control-btn">
                                    <button type="button"
                                        class={"btn " + this.selectBySavedStatus({
                                            'saved': "btn-success disabled",
                                            'saving': "btn-primary disabled",
                                            'unsaved': "btn-primary"
                                        })}
                                        onClick={this.onSave}>
                                        {this.selectBySavedStatus({
                                            'unsaved': "Save",
                                            'saving': "Saving..",
                                            'saved': "Saved"
                                        })}
                                    </button>
                                    <button type="button"
                                        class="btn btn-danger"
                                        onClick={this.props.cancelCallback} >
                                        Cancel
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    {this.state.type != 'quiz' ?
                        <div class="form-group">
                            <label class="control-label col-sm-2">Description</label>
                            <div class="col-sm-9">
                                <WmdTextarea
                                placeholder="Enter a short description here.."
                                name={this.state.type == 'video' ? 'content' : 'description'}/>
                            </div>
                        </div>
                        : null
                    }
                </form>
            </div>
        );
    }
});





var EditSections = React.createClass({
    mixins: [SortableMixin, SavedStatusMixin, BackgroundTransitionMixin],

    getInitialState: function() {
        return {
            order: false,
            sections: this.props.document.sections,
        }
    },

    getDefaultProps: function() {
        return {
            divId : "other-sections"
        };
    },

    addSection: function(){
        url = "/document/api/page/" + this.props.document.id + "/add_section/?format=json";
        data = {
            title: ' ',
            description: ' '
        }
        request = ajax_json_request(url, "POST", data);
        request.done(function(response){
            response = jQuery.parseJSON(response);
            data['id'] = response['id'];
            data['title'] = '';
            data['description'] = '';
            state = this.state;
            state.sections.push(data);
            this.setState(state);
            console.log('added section with id' + data['id']);
        }.bind(this));
    },

    saveOrder: function(data){
        url = "/document/api/page/" + this.props.document.id + "/reorder_sections/?format=json"
        this.toSaving();
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response){
            response = jQuery.parseJSON(response);
            //console.log(response);
            this.setState({sections: []});
            setTimeout(function() {
                console.log('new sections  will be');
                console.log(response['sections']);
                this.setState({sections: response['sections']});
            }.bind(this), 0);
            this.toSaved();
            this.saveOrderSuccess("#"+this.props.divId);
        }.bind(this));

        request.fail(function(){
            this.toUnsaved();
        });
    },

    sortClick: function(id, myclass) {
        this.handleSortClick(id, myclass);
        this.toUnsaved();
    },

    deleteSection: function(id) {
        console.log('got delete from '+ id);
        state = this.state;
        newSections = state.sections.filter(function(item){
            return (item.id != id);
        });
        console.log("the new sections are : ")
        console.log(newSections);
        this.setState({sections : newSections});
    },

    render: function() {
        console.log("Sections in this set are :");
        console.log(this.state.sections);
        sections = this.state.sections.map(function(item, i){
            return (
                <li key={item.id} id={"other-section-"+item.id} class={"other-sections-section"+this.props.divId}>
                    <EditSection key={item.id} id={item.id}
                        title={item.title}
                        description={item.description}
                        file={item.file}
                        preview={this.state.order}
                        deleteCallback={this.deleteSection.bind(this, item.id)}
                        showFileField={this.props.showFileField}/>
                </li>
            );
        }.bind(this));

        listStyle = this.getBackgroundTransitionStyle();
        listStyle.overflow = 'auto';
        if (this.state.order){
            listStyle.padding = 10;
            listStyle.marginBottom = 10;
        };

        btnStyle = {
            margin: 10,
            marginLeft: 0,
            width: 77
        }

        return (
            <div>
                {this.selectBySavedStatus({
                    'saved':
                    <button type="button"
                        class="btn btn-primary"
                        style={btnStyle}
                        onClick={this.sortClick.bind(this, "#"+this.props.divId, ".other-sections-section"+this.props.divId)}>
                        Reorder
                    </button>,
                    'unsaved':
                    <button type="button"
                        style={btnStyle}
                        class="btn btn-primary"
                        onClick={this.handleSaveOrder.bind(this, "#"+this.props.divId, this.props.divId.length)}>
                        Save
                    </button>,
                    'saving':
                    <button type="button"
                        style={btnStyle}
                        class="btn btn-primary disabled">
                        Saving..
                    </button>
                })}
                {/*<button type="button"
                    class="btn btn-primary" onClick={this.addSection}>
                    Add Section
                </button>*/null}
                <ul class="list-unstyled" id={this.props.divId} style={listStyle}>
                    {sections}
                </ul>
                <button type="button"
                    class="btn btn-primary" onClick={this.addSection}>
                    Add Section
                </button>
            </div>
        );
    }
})

var EditSection = React.createClass({
    mixins: [SavedStatusMixin, BackgroundTransitionMixin, StyleTransitionMixin],

    getInitialState: function(){
        return {
            title: this.props.title,
            description: this.props.description,
            newTitle: this.props.title,
            newDescription: this.props.description,
            file: this.props.file
        };
    },

    onSavedStatusUpdate: function() {
        this.props.changeCallback({
            title: this.refs.title.getDOMNode().value,
            description: this.refs.description.getDOMNode().value
        });
    },

    onTitleChange: function (event) {
        this.setState({newTitle: this.refs.title.getDOMNode().value});
        this.toUnsaved();
    },

    onDescriptionChange: function (event) {
        this.setState({newDescription: event.target.value});
        this.toUnsaved();
    },

    getDefaultProps: function() {
        return {
          titleLabel: 'Section Title',
          descriptionLabel: 'Section Content',
          baseUrl: "/document/api/section/",
          changeCallback: function(){},
          preview: false,
          deleteCallback: function(){},
          showFileField: false
        };
    },

    onSave: function() {
        if (!this.props.showFileField){
            this.toSaving();
            data = {
                title: this.state.newTitle,
                description: this.state.newDescription
            }
            url = this.props.baseUrl + this.props.id + "/?format=json";
            request = ajax_json_request(url, "PATCH", data);
            request.done(function(response) {
                this.setState({
                    title: data['title'],
                    description: data['description']
                });
                this.toSaved();
            }.bind(this));
            request.fail(function(response) {
                this.toUnsaved();
                display_global_message("Unable to save data", "error");
            }.bind(this));
        } else {
            var formData = new FormData(this.refs.form.getDOMNode());
            var url = this.props.baseUrl + this.props.id + "/?format=json";
            ajax_custom_request({
                url: url,
                type: 'PATCH',
                data: formData,
                beforeSend: function(xhr, settings){
                    this.toSaving();
                }.bind(this),
                success: function(response){
                    console.log(response['file']);
                    //response = jQuery.parseJSON(response);
                    this.setState({
                        title: response['title'],
                        description: response['description'],
                        file: response['file']
                    });
                    this.toSaved();
                }.bind(this),
                error: function(xhr, textStatus){
                    msg = "Unable to save data";
                    display_global_message(msg, "error");
                    this.toUnsaved();
                }.bind(this)
            });
        }
    },

    onDelete: function(){
        var url = this.props.baseUrl + this.props.id + "/?format=json";
        console.log('will DELETE to ' + url);
        request = ajax_json_request(url, "DELETE", {});
        request.done(this.props.deleteCallback);
    },

    onSubmit: function() {
      this.onSave();
      return false;
    },

    onRevert: function(event){
        this.setState({
            newTitle: this.state.title,
            newDescription: this.state.description
        });
        this.toSaved();
        $(this.refs.description.getDOMNode()).focus();
    },

    render: function(){
        rootStyle = this.getBackgroundTransitionStyle();
        rootStyle.padding = 10;
        rootStyle.marginBottom = 10;

        //Style for Save Button
        saveButtonStyle = this.getStyleTransition('all');
        saveButtonStyle.width = 77;

        if (this.props.preview){
            rootStyle.marginBottom = 0;
            rootStyle.border = "1px solid #ddd";
            rootStyle.width = 500;
            rootStyle.minHeight = 42;
            return (
                <div style={{padding:"5px 0"}}>
                    <div style={rootStyle}>
                        {this.state.newTitle}
                    </div>
                </div>
            );
        }
        savedStatus = this.state.savedStatus;
        return (
            <div style={rootStyle}>
                <form ref="form" onSubmit={this.onSubmit}>
                    <div class="mytablefull">
                        <div class="mytablerow">
                            <div class="mytablecell">
                                <div class="form-group">
                                    <label>
                                        {this.props.titleLabel}
                                    </label>
                                    <input
                                        value={this.state.newTitle}
                                        ref="title"
                                        type="text"
                                        name="title"
                                        class="form-control"
                                        placeholder="Section Title"
                                        onChange={this.onTitleChange}/>
                                </div>
                            </div>
                            <div class="mytablecell concept-section-edit-btns">
                                <div style={{height: '100%', position: 'relative'}}>
                                <div>
                                    {savedStatus == 'saved' ?
                                        <button style={saveButtonStyle} type="button"
                                            class="btn btn-success disabled">
                                            Saved
                                        </button> :
                                        (savedStatus == 'saving' ?
                                            <button style={saveButtonStyle} type="button"
                                                class="btn btn-primary disabled">
                                                Saving..
                                            </button> :
                                            <button style={saveButtonStyle} type="button"
                                                class="btn btn-primary" onClick={this.onSave}>
                                                Save
                                            </button>
                                        )
                                    }
                                    <button type="button"
                                        class={"btn btn-warning" +
                                            (this.state.savedStatus == 'saved' ?
                                                " disabled" : "")}
                                        onClick={this.onRevert} >
                                        Revert
                                    </button>
                                    {this.props.noDelete ? null :
                                        <button type="button"
                                            data-toggle="modal"
                                            data-target={"#myModal_section"+this.props.id}
                                            class="btn btn-danger">Delete</button>}
                                    {this.props.noDelete ? null :
                                        <validateDeleteBtn modal={"myModal_section"+this.props.id}
                                            label="myModalLabel"
                                            callback={this.onDelete}
                                            heading="section"/>}
                                </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    {this.props.showFileField ?
                        <div class="form-group">
                            <label >
                                File
                            </label>
                            <span class="help-block">
                                This field is optional. If you upload a file,
                                then a link to the file will be provided, with
                                the description below it.
                            </span>
                            {this.state.file ?
                                <div>
                                    <a href={this.state.file} target="_blank">
                                        {this.state.title}
                                    </a>
                                </div>:
                                <div>No file uploaded yet</div>
                            }
                            <div >
                                <div class="fileinput fileinput-new"
                                    data-provides="fileinput">
                                    <span class="btn btn-primary btn-file">
                                        <span class="fileinput-new">
                                            {this.state.file ? "Change file" : "Select File"}
                                        </span>
                                        <span class="fileinput-exists">
                                            Change
                                        </span>
                                        <input type="file"
                                            name="file"
                                            ref="file"
                                            onChange={this.toUnsaved} />
                                    </span>
                                    <span class="fileinput-filename"></span>
                                    <a href="#"
                                        class="close fileinput-exists"
                                        data-dismiss="fileinput"
                                        style={{float: 'none'}}>
                                        &times;
                                    </a>
                                </div>
                            </div>
                        </div>
                        : null
                    }
                    <div class="form-group">
                        <label>
                            {this.props.descriptionLabel}
                        </label>
                        <WmdTextarea ref="description"
                            placeholder="Section Contents"
                            value={this.state.newDescription}
                            name="description"
                            onChange={this.onDescriptionChange} />
                    </div>
                </form>
            </div>
        );
    }
});




/************ Integratiosn *************/



/*
    This contains the currently selected learning element
    in the concept. It is of one of three types:
    1. Video
    2. Quiz
    3. Document
    It simply checks the type and renders the corresponding element
*/

var QuestionModuleEditId = "concept-learning-element-quiz";

var LearningElementEdit = React.createClass({

    getInitialState: function() {
        return {loaded: true};
    },

    setLoaded: function(value){
        this.setState({loaded: value});
    },

    componentDidUpdate: function() {
        if (!this.state.loaded)
            setTimeout(this.setLoaded.bind(this, true), 20);
    },

    componentWillReceiveProps: function() {
        this.setLoaded(false);
    },

    render: function() {
        //console.log('ready to render video');
        //console.log(this.props.data);
        if (!this.state.loaded){
            return <div>Loading...</div>;
        }

        elementNode = null;
        if (!this.props.data) return <div></div>;
        if (this.props.data.type == 'video'){
            //return (<ConceptVideoBox data={this.props.data.content} />);
            //console.log(this.props.data);
            elementNode = <ConceptVideoBox data={this.props.data} />;
        }
        else if (this.props.data.type == 'quiz'){
            elementNode = (
                <div>
                    <div id={QuestionModuleEditId} />
                    <QuizEditAdmin quiz={this.props.data.content} />;
                </div>
            );
        }
        else if (this.props.data.type == 'document'){
            elementNode = <ConceptDocumentEdit data={this.props.data} />;
        }
        return (
            <div class="concept-learning-element-edit">
            {elementNode}
            </div>
        );
    }
});


/*
    Component to display a document learning element
*/
var ConceptDocumentEdit = React.createClass({
    mixins: [ScrollToElementMixin],

    getInitialState: function() {
        return {
            title: this.props.data.content.title
        };
    },

    onTitleChange: function(data) {
        this.setState({title: data.title});
    },

    render: function() {
        content = this.props.data.content;
        return (
           <div class="concept-document">
                <div class="concept-document-title">
                    <h3>
                        {this.state.title}
                    </h3>
                    <EditSection title={content.title}
                        description={content.description}
                        titleLabel="Document Title"
                        descriptionLabel="Document description"
                        noDelete={true}
                        baseUrl="/document/api/page/"
                        id={content.id}
                        changeCallback={this.onTitleChange} />
                </div>
                <div class="concept-document-sections">
                    <h4> Sections and Files </h4>
                    <EditSections document={this.props.data.content} showFileField={true} divId="ather-sections" />
                </div>
            </div>
        );
    }
})






/***********END Integration *********/






var ConceptMain = React.createClass({
    render: function() {
        return <EditConcept conceptId={$("#concept").attr('conceptId')} />
    }
});

React.renderComponent(
    <ConceptMain />,
    document.getElementById('concept')
);
