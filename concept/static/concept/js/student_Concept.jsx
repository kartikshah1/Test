/** @jsx React.DOM */

/* File Created by : Aakash N S */

var ConceptInstructorArea = React.createClass({
    render: function() {
        return (
            <div></div>
        );
    }
});

var InVideoQuestionModule = React.createClass({

    base_url: "/quiz/api/",

    loadQuestions: function(callback) {
        url = this.base_url + "question_module/" + this.props.data.id + "/get_questions/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState["questions"] = response;
            oldState["loaded"] = true;
            this.setState(oldState);
            if (callback != undefined) {
                callback();
            }
        }.bind(this));
    },

    getInitialState: function() {
        return {loaded: false};
    },

    render: function() {
        if (!this.props.visible) {
            return (<div></div>);
        }
        else if (!this.state.loaded) {
            this.loadQuestions();
            return (
                <ul class="list-group">
                    <li class="list-group-item text-center">
                        <LoadingBar />
                    </li>
                </ul>
            );
        }
        questions = this.state.questions.map(function(q) {
            return <li class="list-group-item"><Question data={q} /></li>;
        });
        var _title = converter.makeHtml(this.props.data.title);
        var titlenode = null;
        if (!this.props.data.dummy)
            titlenode = (
                <li class="list-group-item">
                    <span dangerouslySetInnerHTML={{__html: _title}} />
                </li>
            );
        return (
            <ul class="list-group">
                {titlenode}
                {questions}
            </ul>
        );
    }
});


var InVideoQuiz = React.createClass ({
    base_url: "/quiz/api/",

    setPage: function(action) {
        oldState = this.state;
        oldState.current = (action - 1);
        this.setState(oldState);
    },

    loadQuiz: function() {
        url = this.base_url + "quiz/" + this.props.id + "/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState.data = response;
            oldState.current = 0;
            oldState.quiz_loaded = true;
            if (this.state.questionModules != undefined) {
                oldState.loaded = true;
            }
            else {
                oldState.loaded = false;
            }
            this.setState(oldState);
        }.bind(this));
    },

    loadQuestionModules: function() {
        url = this.base_url + "quiz/" + this.props.id + "/get_question_modules/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            // Do NOT name it question_modules
            oldState.questionModules = response;
            oldState.loaded = true;
            this.setState(oldState);
        }.bind(this));
    },

    getInitialState: function() {
        return {
            loaded: false,
            quiz_loaded: false,
            current: undefined,
            questionModules: undefined,
            data: undefined
        };
    },

    close: function(){
        $(this.getDOMNode()).hide();
    },

    render: function() {
        if (this.state.quiz_loaded) {
            if (this.state.loaded) {
                currentId = this.state.questionModules[this.state.current]["id"];
                modules = this.state.questionModules.map(function(module) {
                    visible = false;
                    if (module.id == currentId) visible = true;
                    return (<InVideoQuestionModule data={module} visible={visible}/>);
                }.bind(this));
            }
            else {
                modules =
                    <div class="panel panel-default">
                        <div class="panel-heading text-center"><LoadingBar /></div>
                    </div>;
                this.loadQuestionModules();
            }
            var paginator = null;
            if (this.state.data.question_modules > 1)
                paginator = (
                    <div class="panel-body text-center">
                        <Paginator
                            totalPages={this.state.data.question_modules}
                            maxPages={5}
                            callback={this.setPage} />
                    </div>
                );

            return (
                <div class="panel panel-default quiz-panel in-video-quiz">
                    {paginator}
                    {modules}
                </div>
            );
        }
        else {
            this.loadQuiz();
            return (
                <div class="panel panel-default quiz-panel in-video-quiz">
                    <div class="panel-heading text-center"><LoadingBar /></div>
                </div>
            );
        }
    },
    componentDidMount: function() {
        $(this.getDOMNode()).hide().fadeIn();
        $('html,body').animate({
            scrollTop: $(this.getDOMNode()).offset().top - 60
        }, 1000).bind(this);
    }
});


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
var Concept = React.createClass({
    base_url: "/concept/api/",

    /* Set which item (if any) is to be highlighted in the playlist */
    highlightItem: function(id, focus) {
        state = this.state;
        state.highlight = id;
        this.setState(state);
    },

    /* Set the current learning element */
    changeCurrent: function(id) {
        state = this.state;
        state.data.current_element = id;
        this.setState(state);
    },

    /* Loads the data for the concept from server */
    loadData: function() {
        url = this.base_url + "concept/" + this.props.conceptId + "/get_concept_page_data/";
        $.ajax({
            url: url,
            dataType: 'json',
            mimeType: 'application/json',
            data: {format: 'json'},
            success: function(data) {
                state = this.state;
                state.loaded = true;
                state.data = data
                this.setState(state);
            }.bind(this)
        });
    },

    getInitialState: function() {
        return {
            loaded: false,
            data: undefined,
            highlight: undefined,
        };
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
            current_item_data = this.state.data.playlist[this.state.data.current_element];

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
                                <a href="#" data-toggle="collapse"
                                    data-target="#concept-info-body">
                                    <span class="caret"></span>
                                </a>
                              </li>
                            </ol>
                        </div>
                        <div class="panel-body collapse in" id="concept-info-body">
                            <ConceptDetails data={this.state.data}
                                clickCallback={this.changeCurrent}
                                focusCallback={this.highlightItem} />
                        </div>
                        <div class="panel-footer">
                            <ConceptPlaylist
                                conceptId={this.props.conceptId}
                                list={this.state.data.playlist}
                                current={this.state.data.current_element}
                                clickCallback={this.changeCurrent}
                                highlight = {this.state.highlight} />
                        </div>
                    </div>

                    <LearningElement data={current_item_data}/>
                    <ConceptInstructorArea />
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
var ConceptDetails = React.createClass({
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
    handleClick: function(id) {
        this.props.clickCallback(id);
    },

    capitaliseFirstLetter: function(string){
        return string.charAt(0).toUpperCase() + string.slice(1);
    },

    render: function() {
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
                    <a href={"#item"+i}
                    onMouseEnter={this.handleFocus.bind(this, i)}
                    onMouseLeave={this.handleBlur.bind(this, i)}
                    onClick={this.handleClick.bind(this, i)} >
                        {item.content.title + " (" + this.capitaliseFirstLetter(item.type) + ")"}
                    </a>
                </li>
            );
        }.bind(this));

        otherSections = this.props.data.title_document.sections.map(function(item, i){
            return (
                <li key={i}>
                    <h4>{item.title}</h4>
                    <div><span dangerouslySetInnerHTML={{__html: converter.makeHtml(item.description)}} /></div>
                </li>
            );
        });
        return (
            <div id="concept-details">
                <img src={this.props.data.image} class="pull-right concept-image"/>
                <ul class="list-unstyled">
                    <li>
                        <h4>Summary</h4>
                        <div class="concept-summary">
                            {this.props.data.description}
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
});


/*
    Contains a row of buttons (links actually) which
    convecy some information about the corresponding
    learning element, and load that element on click
    Structure:

    ConceptPlaylist [R]
        [ConceptPlaylistItem [R]]
*/
var ConceptPlaylist = React.createClass({
    render: function() {
        current = this.props.current;
        callback = this.props.clickCallback;
        itemNodes = this.props.list.map(function(item, i) {
            return (
                <li key={i}>
                    <ConceptPlaylistItem status={
                            (i == current) ?
                                'current' :
                                (item.history.seen_status ? 'seen' : 'unseen')
                            }
                        index={i}
                        type={item.type}
                        title={item.title} id={item.id}
                        highlight={this.props.highlight == i}
                        clickCallback={callback}/>
                </li>
            );
        }.bind(this));
        return (
            <div>
                <ul class="list-inline concept-playlist">
                    {itemNodes}
                </ul>
            </div>
        );
    }
});


/*
    ConceptPlaylistItem
    This is a small clickable box that acts as a
    link to the corresponding learning element
    (video, quiz or document) in the concept.

    Props:
    type, status, id, title, clickCallback
*/
var ConceptPlaylistItem = React.createClass({
    handleClick: function(id){
        console.log("here we are", id);
        this.props.clickCallback(id);
    },

    render: function() {
        isVideo = this.props.type == "video";
        isQuiz = this.props.type == "quiz";
        console.log(this.props.status + " " + (this.props.highlight ? "highlight" : ""));
        return (
            <div class="concept-playlist-item">
                <a href={"#item"+this.props.index} data-container="body" data-toggle="popover"
                    data-trigger="hover" data-placement="bottom"
                    title="" data-original-title=""
                    data-content={this.props.title} ref="linkBlock"
                    onClick={this.handleClick.bind(this, this.props.index)}
                    class={this.props.status + " " + (this.props.highlight ? "highlight" : "")}>
                    <span class={"glyphicon glyphicon-" +
                        (isVideo ? "film" : ( isQuiz ? "question-sign" : "file"))}></span>
            </a>
            </div>
        );
    }
});


/*
    This contains the currently selected learning element
    in the concept. It is of one of three types:
    1. Video
    2. Quiz
    3. Document
    It simply checks the type and renders the corresponding element
*/
var LearningElement = React.createClass({
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

    componentWillReceiveProps: function(nextProps) {
        if (this.props.data.type != nextProps.data.type
            || this.props.data.content.id != nextProps.data.content.id)
            this.setLoaded(false);
    },

    render: function() {
        if (!this.state.loaded){
            return <div style={{marginTop: 15}}><LoadingBar /></div>;
        }

        elementNode = null;
        if (!this.props.data) return <div></div>;
        if (this.props.data.type == 'video'){
            //return (<ConceptVideoBox data={this.props.data.content} />);
            console.log(this.props.data);
            elementNode = <ConceptVideoBox data={this.props.data}/>;
        }
        else if (this.props.data.type == 'quiz'){
            elementNode =  <ConceptQuiz id={this.props.data.content.id} />;
        }
        else if (this.props.data.type == 'document'){
            elementNode = <ConceptDocument data={this.props.data} />;
        }
        return (
            <div id="concept-learning-element">
            {elementNode}
            </div>
        );
    }
});


/*
    Component to display a document learning element
*/
var ConceptDocument = React.createClass({
    render: function() {
        content = this.props.data.content;
        sectionNodes = content.sections.map(function(item, i) {
            if (!item.file){
                return(
                    <li key={i}>
                        <h4>{item.title}</h4>
                        <p><span dangerouslySetInnerHTML={{__html: converter.makeHtml(item.description)}} /></p>
                    </li>
                );
            } else {
                return(
                    <li key={i}>
                        <a href={item.file} target="_blank">{item.title}</a>
                        <p><span dangerouslySetInnerHTML={{__html: converter.makeHtml(item.description)}} /></p>
                    </li>
                );
            }
        });
        return (
           <div class="concept-document">
                <div class="concept-document-title">
                    <h3>
                        {content.title}
                    </h3>
                    <p><span dangerouslySetInnerHTML={{__html: converter.makeHtml(content.description)}} /></p>
                </div>
                <ul class="list-unstyled concept-document-sections">
                    {sectionNodes}
                </ul>
            </div>
        );
    }
})


var ConceptMain = React.createClass({
    render: function() {
        return <Concept conceptId={$("#concept").attr('conceptId')} />
    }
});

React.renderComponent(
    <ConceptMain />,
    document.getElementById('concept')
);
