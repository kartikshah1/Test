/** @jsx React.DOM */

// TODO: Disable buttons when ajax request is sent
//          Enable back when request completes

/*
 *   |--------------------------------------|
 *   | QuestionModuleEditAdmin:             |
 *   |  |-----------------------------|     |
 *   |  |   QuestionCreate            |     |
 *   |  |   QuestionEditRow           |     |
 *   |  |-----------------------------|     |
 *   |                                      |
 *   | QuizEditAdmin:                       |
 *   |  |-----------------------------|     |
 *   |  |   QuestionModuleCreate      |     |
 *   |  |   QuestionModuleEditRow     |     |
 *   |  |-----------------------------|     |
 *   |                                      |
 *   | QuizAdmin:                           |
 *   |  |-----------------------------|     |
 *   |  |   QuizCreate                |     |
 *   |  |   QuizEditRow               |     |
 *   |  |-----------------------------|     |
 *   |--------------------------------------|
 */




var QUESTION_TYPES = {
    SINGLE_CHOICE_QUESTION: 'S',
    MULTIPLE_CHOICE_QUESTION: 'M',
    FIXED_ANSWER_QUESTION: 'F',
    DESCRIPTIVE_ANSWER_QUESTION: 'D',
    PROGRAMMING_QUESTION: 'P'
};

function add_error_to_element(element, errors) {
    element.attr('title', 'This field is required.');
    element.tooltip('show');
    element.focus(function() {
        element.tooltip('destroy');
    });
    element.parent().addClass("has-warning");
}

function remove_error_from_element(element) {
    element.parent().removeClass("has-warning");
}

function close_question_list() {
    $("#" + QuestionModuleEditId).hide().fadeOut(function() {
        $(this).html("");
    });
}

function close_question_module_list(QuizEditAdminId) {
    $("#" + QuizEditAdminId).hide().fadeOut(function() {
        $(this).html("");
    });
}







/* Option Plugin Code Starts here - DO NOT MODIFY */

var ChoiceBox = React.createClass({
    getDefaultProps: function() {
        return {
            checked: false,
            text: '',
            changeCallback: function(){},
            closeCallback: function(){
                console.log(this.getDOMNode());
                $(this.getDOMNode()).hide();
            }.bind(this)
        }
    },

    getInitialState: function() {
        return {
            checked: this.props.checked,
            text: this.props.text
        };
    },

    onCheckChange: function(event) {
        this.setState({checked: event.target.checked});
    },

    onTextChange: function(event) {
        this.setState({text: event.target.value});
    },

    componentDidUpdate: function() {
        this.props.changeCallback(this.state);
    },

    render: function() {
        return(
          <li>
          <div>
              <div class="input-group">
                <span class="input-group-addon">
                  <input type={this.props.type}
                    name={this.props.name}
                    ref="select"
                    checked={this.state.checked}
                    onChange={this.onCheckChange}/>
                </span>
                <WmdTextarea class="form-control option-list-text"
                    placeholder="Type Something Here.."
                    value={this.state.text}
                    ref="text"
                    onChange={this.onTextChange}>
                </WmdTextarea>
                <span class="input-group-btn">
                  <button class="btn btn-default"
                    type="button"
                    onClick={this.props.closeCallback}>
                    <span class="glyphicon glyphicon-remove"></span>
                  </button>
                </span>
              </div>
          </div>
          </li>
        );
    }
});


var OptionsBox = React.createClass({
  getData: function() {
    optionNodes = $(this.refs.optionList.getDOMNode()).children("li").filter(":visible");
    type = this.props.type;
    data = []
    //data['multiple'] = type == "checkbox";
    data['options'] = JSON.stringify($(optionNodes).map(function(i,node) {
      return $($(node).find("textarea")[0]).val();
    }).get());
    optionList = $(optionNodes).map(function(i,node) {
          query = "input[type=" + type + "]";
          elmt = $(node).find(query)[0];
          return elmt.checked;
        }).get();
    if (type == 'checkbox'){
        data['selected'] = JSON.stringify(optionList);
        data['answer'] = JSON.stringify(optionList);
    }
    else {
        for (i = 0; i < optionList.length; i++){
            if (optionList[i]) data['answer'] = i;
        }
    }
    //console.log(data);
    return data;

  },
  addChoice: function(checked, text) {
    state = this.state;
    state.choiceBoxes.push(<ChoiceBox type={this.props.type} name={this.props.name}
        id={state.lastId.toString()} checked={checked} text={text} changeCallback={this.onDataChange} />);
    state.lastId++;
    this.setState(state, this.onDataChange);
  },
  getInitialState: function() {
    return {
      choiceBoxes: [],
      lastId: 0
    };
  },
  getDefaultProps: function() {
    return {
        changeCallback: $.noop
    };
  },

  onDataChange: function() {
    this.props.changeCallback(this.getData());
  },

  componentDidMount: function() {
    console.log(this.props);
    if (this.props.data && this.props.data['options']){
        data = this.props.data;
        //console.log(this.props.data);
        options = jQuery.parseJSON(data['options']);
        if (data.type=='S') {
            for (var i = 0; i < options.length; i++){
                this.addChoice(i==data.answer, options[i]);
                console.log("Added choice");
                console.log(this.state);
            }
        } else {
            selected = jQuery.parseJSON(data['selected']);
            for (var i = 0; i < options.length; i++){
                this.addChoice(selected[i], options[i]);
                console.log("Added choice");
                console.log(this.state);
            }
        }
    }
    else this.addChoice(true,'');
    $(this.refs.optionList.getDOMNode()).sortable({
        axis: "y",
        update: this.onDataChange
    });
  },

  render: function() {
    console.log("Render Options List");
    console.log(this.props);
    console.log(this.state);
    return (
    <div class="form-group">
        <label class="control-label col-md-2">Options</label>
        <div class="col-md-9">
            <ul ref="optionList" class="list-unstyled option-module-list">
                {this.state.choiceBoxes}
            </ul>
            <button type="button" class="btn btn-default" onClick={this.addChoice.bind(this,false,'')}>
                Add Option
            </button>
        </div>
    </div>
    );
  },
  componentWillReceiveProps: function(props) {
    for (var i = 0; i < this.state.choiceBoxes.length; i++){
      this.state.choiceBoxes[i].props.type = props.type;
    }
  }
});


var OptionsBoxWithType = React.createClass({
  getInitialState: function() {
    return {
      type: "radio"
    };
  },
  getData: function() {
    return this.refs.box.getData();
  },
  changeType: function() {
    state = this.state;
    if (this.refs.type.getDOMNode().checked) state.type = "checkbox";
    else state.type = "radio";
    this.setState(state);
  },
  render: function() {
    return (
      <div>
        <div class="checkbox">
          <label>
            <input type="checkbox" ref="type" onChange={this.changeType} />
            Allow selection of multiple options
          </label>
        </div>
        <OptionsBox type={this.state.type} name={this.props.name} ref="box" data={this.props.data}/>
      </div>
    );
  }
});


/* Options Plugin Code Ends Hre */







var confirmDeleteMixin = {

    getInitialState: function() {
        return {
            delete_stage: false
        };
    },

    resetDelete: function() {
        state = this.state;
        state.delete_stage = false;
        this.setState(state);
    },

    getDeleteBar: function() {
        delete_bar =
            <button type="submit" class="btn btn-danger btn-sm" onClick={this.deleteObject}>
                Delete
            </button>;
        if (this.state.delete_stage) {
            delete_bar =
                <div>
                    <button type="submit" class="btn btn-warning btn-sm quiz-right-margin" onClick={this.resetDelete}>No</button>
                    <button type="submit" class="btn btn-danger btn-sm" onClick={this.deleteObject}>Yes</button>
                </div>;
        }
        return delete_bar;
    },

    checkDeleteStage: function() {
        if (!this.state.delete_stage) {
            state = this.state;
            state.delete_stage = true;
            this.setState(state);
            return true;
        }
        return false;
    }

};

var ListCreator = React.createClass({

    componentWillReceiveProps: function(nextProps) {
        console.log("Recieve new props for ListCreator");
        this.setState({list: nextProps.defaultValue});
        console.log("Changing List for ListCreator")
    },

    getInitialState: function() {
        list = [];
        if (this.props.defaultValue != undefined) {
            list = this.props.defaultValue;
        }
        max = this.maxInRow;
        if (this.props.maxInRow != undefined) {
            max = this.props.maxInRow;
        }
        return {
            list: list,
            maxInRow: max
        };
    },

    onChange: function() {
        if (this.props.onChange != undefined) {
            this.props.onChange(this.state.list);
        }
    },

    addItem: function() {
        list = this.state.list;
        item_node = this.refs.item.getDOMNode();
        item = item_node.value.trim();
        this.refs.item.getDOMNode().value = '';
        item_node.focus();
        check = this.props.check;
        if (check == undefined) {
            check = function(item) {return !isNaN(item);};
        }
        if (item != '' && check(item)) {
            list.push(item);
        }
        state = this.state;
        state.list = list;
        this.setState(state);
        this.onChange();
    },

    removeItem: function() {
        this.refs.item.getDOMNode().focus();
        list = this.state.list;
        if (list.length != 0) {
            list.pop();
        }
        state = this.state;
        state.list = list;
        this.setState(state);
        this.onChange();
    },

    maxInRow: 6,

    render: function() {
        all_values = this.state.list.map(function(l) {
            return <span class="input-group-addon">{l}</span>;
        });
        values = new Array();
        rows = Math.floor(all_values.length / this.state.maxInRow);
        extra = all_values.length % this.state.maxInRow;
        counter = 0;
        for (var i = 0; i < rows; i++) {
            this_row = new Array();
            for (var j = 0; j < this.state.maxInRow; j++) {
                this_row.push(all_values[counter]);
                counter++;
            }
            values.push(this_row);
        }
        more_values = new Array();
        for (var i = 0; i < extra; i++) {
            more_values.push(all_values[counter]);
            counter++;
        }
        div_values = values.map(function(v) {
            return(
                <div class="input-group">
                    {v}
                </div>);
        });
        id = '';
        if (this.props.id != undefined) {
            id = this.props.id;
        }
        remove_button = <div></div>;
        if (this.state.list.length != 0) {
            remove_button =
                <span class="input-group-btn">
                    <button class="btn btn-default" type="button" onClick={this.removeItem}>
                        <span class="glyphicon glyphicon-remove"></span>
                    </button>
                </span>;
        }
        return (
            <div>
                {div_values}
                <div class="input-group">
                    {remove_button}
                    {more_values}
                    <input type="text" class="form-control" ref="item" id={id} />
                    <span class="input-group-btn">
                        <button class="btn btn-default" type="button" onClick={this.addItem}>
                            <span class="glyphicon glyphicon-plus"></span>
                        </button>
                    </span>
                </div>
            </div>
        );
    }

});

var ChoiceQuestionCreate = OptionsBox;


var FixedAnswerQuestionCreate = React.createClass({

    setAnswer: function(answer) {
        this.props.onChange({'answer': JSON.stringify(answer)});
    },

    getInitialState: function() {
        answer = [];
        if (this.props.defaults != undefined) {
            if (this.props.defaults.answer != undefined) {
                answer = [].concat(this.props.defaults.answer);
            }
        }
        return {answer: answer};
    },

    check: function(text) {
        return true;
    },

    render: function() {
        // Important to call setAnswer here once, so that parent gets correct
        //  default value of answer
        console.log("Render Fixed answer here");
        console.log(this.props);
        this.setAnswer(this.state.answer);
        id = this.props.answerId;
        return (
            <div class="form-group">
                <label class="control-label col-md-2">Correct Answer</label>
                <div class="col-md-9">
                    <ListCreator
                        id={id}
                        check={this.check}
                        onChange={this.setAnswer}
                        defaultValue={this.state.answer} />
                </div>
            </div>
        );
    }

});

var QuestionCreate = React.createClass({
    // CAUTION: This class modifies this.state directly at some places

    // TODO: FETCH answers

    // mixins: [ScrollToElementMixin],

    base_url: '/quiz/api/',

    answer_box_id: 'answer_box',
    // The name createQuestion is slightly misleading. It is used for both create and edit
    createQuestion: function() {

        console.log(this.state);

        if (this.state['answer'] == undefined || this.state['answer'].length == 0) {
            add_error_to_element($("#" + this.answer_box_id), 'This field is required.');
            console.log("answer not defined");
            return;
        }
        if (this.state['answer'] == '[]') {
            if (! confirm("Continue without any answer ?")) {
                return;
            }
        }

        var url_map ={
            'F': "fixed_answer_question",
            'S': "single_choice_question",
            'M': "multiple_choice_question",
            'D': "descriptive_question"
        };

        var url = '';
        var method = '';
        var type = this.refs.type.getDOMNode().value;


        console.log("will send a request now");

        if (this.props.edit) {
        //remove the question from the database
            console.log("will delete first");

            url = this.base_url + "question/" + this.props.defaults.id +"/?format=json";
            method = 'DELETE';
            request = ajax_json_request(url, method, {});
        }

        url = this.base_url + "question_module/" + this.props.question_module.id + '/add_' +
        url_map[type] +'/?format=json';

        method = 'POST';



        data = {};
        for (var i = 0; i < this.validationFields.length; i++) {
            if (this.refs[this.validationFields[i]] != undefined) {
                data[this.validationFields[i]] = this.refs[this.validationFields[i]].getDOMNode().value.trim();
            }
        }
        data["granularity"] = this.state.defaults.granularity.toString();
        data["granularity_hint"] = this.state.defaults.granularity_hint.toString();

        if (data["granularity"] == "") {
            data["granularity"] = "undefined";
        }
        if (data["granularity_hint"] == "") {
            data["granularity_hint"] = "undefined";
        }

        if (this.state.answer_props != undefined) {
            for (var attrname in this.state.answer_props) {
                data[attrname] = this.state[attrname];
            }
        }

        console.log(data);

        request = ajax_json_request(url, method, data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            data = response;
            data['answer_fields'] = {};
            for (var attrname in this.state.answer_props) {
                data.answer_fields[attrname] = this.state[attrname];
            }
            data['prev_id'] = -1;
            if (this.props.defaults) {
                data['prev_id'] = this.props.defaults.id;
            }
            this.props.callback(data);
        }.bind(this));
        request.complete(function(response) {
            if (response.status == 400) {
                // BAD REQUEST - Data Validation failed
                response = jQuery.parseJSON(response.responseText);
                this.validation(response);
            }
            else {
                this.removeValidation();
            }
        }.bind(this));
        return false;
    },

    changeType: function() {
        type = this.refs.type.getDOMNode().value;
        state = this.state;
        state.type = type;
        this.setState(state);
    },

    setAnswer: function(obj) {
        //console.log("setAnswer got ");
        //console.log(obj);
        state = this.state;
        state["answer_props"] = obj;
        for (var attrname in obj) {
            state[attrname] = obj[attrname];
        }
        // WARNING: modifying this.state directly here
        this.state = state;
    },

    getInitialState: function() {
        state = {
            description: '',
            answer_description: '',
            granularity: '',
            granularity_hint: '',
            type: QUESTION_TYPES.FIXED_ANSWER_QUESTION,
            marks: 0,
            grader_type: 'D',
            hint: '',
            attempts: 1,
            answer_fields: {}
        }
        main_state = {'answer_props': {}};
        main_state['type'] = state.type;
        console.log(this.props.defaults);
        if (this.props.defaults != undefined) {
            // There may be a better way to do this
            for (var i = 0; i < this.validationFields.length; i++) {
                if (this.props.defaults[this.validationFields[i]] != undefined) {
                    state[this.validationFields[i]] = this.props.defaults[this.validationFields[i]];
                }
            }
            if (this.props.defaults.answer_fields != undefined) {
                state['answer_fields'] = this.props.defaults.answer_fields;
                for (var attr in this.props.defaults.answer_fields) {
                    main_state[attr] = this.props.defaults.answer_fields[attr];
                    main_state.answer_props[attr] = this.props.defaults.answer_fields[attr];
                }
            }
        }
        if (this.props.defaults && this.props.defaults.type){
            main_state['type'] = state['type'] = this.props.defaults.type;
        }
        if (state.granularity == '' || state.granularity == "0,0") {
            state.granularity = [];
        }
        else {
            state.granularity = state.granularity.split(",");
        }
        if (state.granularity_hint == '' || state.granularity_hint == "0,0") {
            state.granularity_hint = [];
        }
        else {
            state.granularity_hint = state.granularity_hint.split(",");
        }
        main_state['defaults'] = state;
        return main_state;
    },

    onGranularityChange: function(list) {
        // WARNING: modifying this.state directly here
        this.state.defaults.granularity = list;
    },

    onHintGranularityChange: function(list) {
        // WARNING: modifying this.state directly here
        this.state.defaults.granularity_hint = list;
    },

    onMarksChange: function() {
        console.log("clearing granularity");
        this.onGranularityChange([]);
        this.onHintGranularityChange([]);
        this.setState(this.state);
    },

    validationFields: new Array('description', 'answer_description', 'hint', 'granularity',
        'granularity_hint', 'marks', 'grader_type', 'type', 'attempts'),

    removeValidation: function() {
        // this may not be needed because after creation, the parent of QuestionCreate should
        // be re-rendered and hence this module
        if (this.refs == undefined) {
            return;
        }
        for (var i = 0; i < this.validationFields.length; i++) {
            if (this.refs[this.validationFields[i]] != undefined) {
                input = $(this.refs[this.validationFields[i]].getDOMNode());
                remove_error_from_element(input);
            }
        }
    },

    validation: function(response) {
        for (var i = 0; i < this.validationFields.length; i++) {
            if (response[this.validationFields[i]] != undefined) {
                input = $(this.refs[this.validationFields[i]].getDOMNode());
                add_error_to_element(input, response[this.validationFields[i]]);
            }
        }
    },

    checkGranularity: function(text) {
        return !isNaN(text);
    },

    componentDidMount: function() {
        console.log("Initial Props to a question");
        console.log(this.props);
        selected = $(this.refs.type.getDOMNode()).children("option[value="+this.state.type+"]")[0]
        $(selected).attr("selected","selected");
        this.changeType();
        /*$('html,body').animate({
            scrollTop: $(this.getDOMNode()).offset().top - 100
        }, 1000).bind(this);*/
    },

    render: function() {
        console.log("State of Question before render");
        console.log(this.state)
        console.log(this.state.type == QUESTION_TYPES.FIXED_ANSWER_QUESTION);
        console.log(this.state.type == QUESTION_TYPES.SINGLE_CHOICE_QUESTION);
        console.log(this.state.type == QUESTION_TYPES.MULTIPLE_CHOICE_QUESTION);
        answer_box = <div></div>;
        if (this.state.type == QUESTION_TYPES.FIXED_ANSWER_QUESTION) {
            console.log("In Fixed Answer Question");
            answer_box = <FixedAnswerQuestionCreate defaults={this.state.defaults.answer_fields}
                onChange={this.setAnswer} answerId={this.answer_box_id} />
        }
        else if (this.state.type == QUESTION_TYPES.SINGLE_CHOICE_QUESTION ||
                    this.state.type == QUESTION_TYPES.MULTIPLE_CHOICE_QUESTION) {
            console.log("In Choice Question");
            answer_box = <ChoiceQuestionCreate data={this.state.defaults.answer_fields}
                 name={this.answer_box_id}
                type={this.state.type== QUESTION_TYPES.SINGLE_CHOICE_QUESTION ? "radio" : "checkbox"}
                changeCallback={this.setAnswer} />
        }
        if (this.state.defaults.type == QUESTION_TYPES.FIXED_ANSWER_QUESTION) {
            select_type = <select class="form-control" ref="type" onChange={this.changeType} >
                                <option value={QUESTION_TYPES.FIXED_ANSWER_QUESTION} selected="selected">
                                    Fixed Answer Question</option>
                                <option value={QUESTION_TYPES.SINGLE_CHOICE_QUESTION}>Single Choice Question</option>
                                <option value={QUESTION_TYPES.MULTIPLE_CHOICE_QUESTION}>Multiple Choice Question</option>
                            </select>
        } else if (this.state.defaults.type == QUESTION_TYPES.SINGLE_CHOICE_QUESTION) {
            select_type = <select class="form-control" ref="type" onChange={this.changeType} >
                                <option value={QUESTION_TYPES.FIXED_ANSWER_QUESTION}> Fixed Answer Question</option>
                                <option value={QUESTION_TYPES.SINGLE_CHOICE_QUESTION} selected="selected">
                                    Single Choice Question</option>
                                <option value={QUESTION_TYPES.MULTIPLE_CHOICE_QUESTION}>Multiple Choice Question</option>
                            </select>
        } else {
            select_type = <select class="form-control" ref="type" onChange={this.changeType} >
                                <option value={QUESTION_TYPES.FIXED_ANSWER_QUESTION}> Fixed Answer Question</option>
                                <option value={QUESTION_TYPES.SINGLE_CHOICE_QUESTION}> Single Choice Question</option>
                                <option value={QUESTION_TYPES.MULTIPLE_CHOICE_QUESTION} selected="selected">
                                    Multiple Choice Question</option>
                            </select>
        }

        return (
            <form role="form" class="form-horizontal">
                <div class="form-group">
                    <label class="control-label col-md-2">Description</label>
                    <div class="col-md-9">
                        <WmdTextarea ref="description" placeholder="Description"
                            defaultValue={this.state.defaults.description} rows="2" />
                    </div>
                </div>
                <div class="form-group">
                    <label class="control-label col-md-2">Marks</label>
                    <div class="col-md-4">
                        <input type="number" class="form-control" ref="marks"
                            placeholder="Maximum marks"
                            defaultValue={""+this.state.defaults.marks}
                            onChange={this.onMarksChange}/>
                    </div>
                    <label class="control-label col-md-1">Attempts</label>
                    <div class="col-md-4">
                        <input type="number" class="form-control" ref="attempts"
                            placeholder="Maximum attempts"
                            defaultValue={this.state.defaults.attempts} />
                    </div>
                </div>
                <div class="form-group">
                    <label class="control-label col-md-2">Type</label>
                    <div class="col-md-4">
                        {select_type}
                    </div>
                </div>
                {answer_box}
                <div class="form-group">
                    <label class="control-label col-md-2">Hint</label>
                    <div class="col-md-9">
                        <WmdTextarea ref="hint" placeholder="Hint"
                            defaultValue={this.state.defaults.hint} rows="2"/>
                    </div>
                </div>
                <div class="form-group">
                    <label class="control-label col-md-2">Answer Description</label>
                    <div class="col-md-9">
                        <WmdTextarea ref="answer_description"
                            placeholder="Answer Description" rows="2"
                            defaultValue={this.state.defaults.answer_description} />
                    </div>
                </div>
                <div class="form-group">
                    <label class="control-label col-md-2">Granularity</label>
                    <div class="col-md-4">
                        <ListCreator check={this.checkGranularity}
                            onChange={this.onGranularityChange}
                            defaultValue={this.state.defaults.granularity} />
                        <span class="help-block">Leave blank for default value</span>
                    </div>
                    <label class="control-label col-md-1">With hint</label>
                    <div class="col-md-4">
                        <ListCreator check={this.checkGranularity}
                            onChange={this.onHintGranularityChange}
                            defaultValue={this.state.defaults.granularity_hint} />
                        <span class="help-block">Leave blank for default value</span>
                    </div>
                </div>
                <div class="form-group">
                    <label class="control-label col-md-2">Grading Type</label>
                    <div class="col-md-4">
                        <select class="form-control" ref="grader_type"
                            defaultValue={this.state.defaults.grader_type}>
                            <option value='D'>Direct</option>
                            <option value='M'>Manual</option>
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-md-offset-2 col-md-2">
                        <button type="button" class="btn btn-primary"
                            onClick={this.createQuestion}>Save</button>
                    </div>
                    <div class="col-md-2 col-md-offset-3">
                        <button type="button" class="btn btn-danger"
                            onClick={this.props.closeCallback}>Close</button>
                    </div>
                </div>
            </form>
        );
    }

});

var QuestionEditRow = React.createClass({

    mixins: [confirmDeleteMixin],

    base_url: '/quiz/api/',

    editQuestion: function() {
        this.props.editCallback(this.props.data);
        return false;
    },

    deleteObject: function() {
        if (this.checkDeleteStage()) return;
        url = this.base_url + "question/" + this.props.data.id + "/?format=json";
        request = ajax_json_request(url, "DELETE", {});
        request.done(function(response) {
            this.props.deleteCallback(this.props.data);
        }.bind(this));
        request.complete(function(response) {
            this.resetDelete();
        }.bind(this));
    },

    render: function() {
        delete_bar = this.getDeleteBar();
        var _description = converter.makeHtml(this.props.data.description);
        return (
            <tr>
                <td>
                    <button type="button" class="btn btn-default btn-sm" onClick={this.editQuestion}>
                        Edit
                    </button>
                </td>
                <td>
                    <span dangerouslySetInnerHTML={{__html: _description}} />
                </td>
                <td>{this.props.data.marks}</td>
                <td>{this.props.data.attempts}</td>
                <td>
                    {delete_bar}
                </td>
            </tr>
        );
    }

});

var QuestionModuleEditAdmin = React.createClass({

    closePanel: function() {
        close_question_list();
    },

    base_url: "/quiz/api/",

    openQuestion: null,

    componentDidMount: function() {
        this.getQuestions();
        $(this.getDOMNode()).hide().fadeIn();
        $('html,body').animate({
            scrollTop: $(this.getDOMNode()).offset().top - 100
        }, 1000).bind(this);

    },

    getInitialState: function() {
        return {
            loaded: false,
            create: false,
            edit: false,
            title_edit: false,
            question_module: this.props.question_module
        };
    },

    editQuestion: function(data) {
        this.openQuestion = data.id;
        state = this.state;
        state.create = false;
        state.edit = true;
        state.defaults = data;
        this.setState(state);
        window.scrollTo(0, document.getElementById(QuestionModuleEditId).offsetTop-75);
    },

    createQuestion: function(data) {
        console.log("Create Question in QuestionModuleEditAdmin");
        console.log(this.state);
        console.log(data);
        oldState = this.state;
        if (this.state.edit) {
            for (var i = 0; i < oldState.questions.length; i++) {
                if (oldState.questions[i]['id'] == data['prev_id']) {
                    oldState.questions[i] = data;
                    break;
                }
            }
        }
        else if (this.state.create) { // Either one must be true
            oldState.questions.push(data);
        }
        oldState.create = false;
        oldState.edit = false;
        this.setState(oldState);
        window.scrollTo(0, document.getElementById(QuestionModuleEditId).offsetTop-75);
    },

    deleteQuestion: function(data) {
        questions = this.state.questions;
        index = questions.indexOf(data);
        if (index > -1) {
            questions.splice(index, 1);
        }
        oldState = this.state;
        oldState.questions = questions;
        if (this.openQuestion == data.id) {
            oldState.create = false;
            oldState.edit = false;
            window.scrollTo(0, document.getElementById(QuestionModuleEditId).offsetTop-75);
        }
        this.setState(oldState);
    },

    getQuestions: function() {
        url = this.base_url + "question_module/" + this.props.question_module.id + "/get_questions_admin/?format=json";
        //console.log("getting questions");
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            //console.log(response);
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState.questions = response;
            oldState.loaded = true;
            this.setState(oldState);
            //alert("return from getQuestions ajax");
        }.bind(this));
        request.fail(function(response) {
            //alert("Get Questions failed");
        });
        //alert("return from getQuestions");
    },

    showQuestionCreate: function() {
        oldState = this.state;
        oldState.create = true;
        this.setState(oldState);
    },

    closeCreate: function() {
        oldState = this.state;
        oldState.create = false;
        oldState.edit = false;
        // Change this to suit the application of this component
        window.scrollTo(0, document.getElementById(QuestionModuleEditId).offsetTop-75);
        this.setState(oldState);
    },

    editQuestionModule: function(data) {
        state = this.state;
        if ( state.question_module.title != data.title) {
            console.log(state.question_module);
            console.log(data);
            display_global_message("Successfully saved", "success");
            state.question_module = data;
            state.title_edit = false;
            this.setState(state);
            this.props.refreshCallback();
        } else {
            console.log("No change to description of module");
            state.title_edit = false;
            this.setState(state);
        }
    },

    showTitleEdit: function() {
        state = this.state;
        state.title_edit = true;
        this.setState(state);
    },

    render: function() {
        if (!this.state.loaded) {
            return (
                <div class="panel panel-default">
                    <div class="panel-heading text-center"><LoadingBar /></div>
                </div>
            );
        }
        //alert("procesing question module");
        question_create = <button type="button" class="btn btn-primary" onClick={this.showQuestionCreate}> Add new Question </button>;
        if (this.state.create) {
            question_create =
                <QuestionCreate
                    callback={this.createQuestion}
                    question_module={this.state.question_module}
                    closeCallback={this.closeCreate} />;
        }
        else if (this.state.edit) {
            question_create =
                <QuestionCreate
                    key={this.state.question_module.id + "/" + this.state.defaults.id}
                    edit={true}
                    callback={this.createQuestion}
                    defaults={this.state.defaults}
                    question_module={this.props.question_module}
                    closeCallback={this.closeCreate} />;
        }
        //alert("Listing all questions");
        question_edit = this.state.questions.map(function(q) {
            return <QuestionEditRow editCallback={this.editQuestion} deleteCallback={this.deleteQuestion} data={q} />;
        }.bind(this));
        title_edit = '';
        if (this.state.title_edit) {
            title_edit =
                <ul class="list-group">
                    <li class="list-group-item question-module-edit">
                        <QuestionModuleCreate data={this.state.question_module} callback={this.editQuestionModule} />
                    </li>
                </ul>;
        }
        else {
            title_edit =
                <ul class="list-group">
                    <li class="list-group-item question-module-edit">
                        <button type="button" class="btn btn-default" onClick={this.showTitleEdit} >Edit Description</button>
                    </li>
                </ul>;
        }
        //alert("rendering Question Module Edit");
        return (
            <div class="panel panel-default">
                <div class="panel-heading">
                    <span class="quiz-text-mute quiz-right-margin">Editing</span>
                    <strong class="quiz-right-margin">
                        {this.props.quiz.title}
                    </strong>
                    <span class="glyphicon glyphicon-arrow-right quiz-right-margin"></span>
                    <strong>
                        Module ID {this.state.question_module.id}
                    </strong>
                    <span class="pull-right">
                        <button type="button" class="close" onClick={this.closePanel}>&times;</button>
                    </span>
                </div>
                <div class="panel-body" ref="create">
                    {question_create}
                </div>
                {title_edit}
                <table class="table table-hover quiz-table">
                    <tbody>
                        <tr>
                            <th width="11%"></th>
                            <th>Description</th>
                            <th>Points</th>
                            <th>Attempts</th>
                            <th class="confirm-delete"></th>
                        </tr>
                        {question_edit}
                    </tbody>
                </table>
            </div>
        );
    }

});


var QuestionModuleCreate = React.createClass({

    base_url: "/quiz/api/",

    // always return false
    createQuestionModule: function() {
        url = this.base_url + "quiz/" + this.props.quiz_id + "/add_question_module/?format=json";
        method = "POST";
        data = {
            quiz: this.props.quiz_id,
            title: this.refs.title.getDOMNode().value.trim()
        };
        if (this.props.data != undefined) {
            url = this.base_url + "question_module/" + this.props.data.id + "/?format=json";
            method = "PATCH";
        }
        request = ajax_json_request(url, method, data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            data = response;
            this.props.callback(data);
        }.bind(this));
        title_input = this.refs.title.getDOMNode();
        request.complete(function(response) {
            if (response.status == 400) {
                // BAD REQUEST - Data Validation failed
                response = jQuery.parseJSON(response.responseText);
                if (response.title != undefined) {
                    // TODO: replace with foreach (this.refs)
                    //title_input = $(this.refs.title.getDOMNode());
                    add_error_to_element($(title_input), response.title);
                }
            }
            else {
                //title_input = $(this.refs.title.getDOMNode());
                remove_error_from_element($(title_input));
            }
            if (this.props.data == undefined) {
                //this.refs.title.getDOMNode().value = '';
                title_input.value = ''
            }
        }.bind(this));
        this.cancelCreate();
        return false;
    },

    returnWithoutCreate: function() {
        console.log("return without save");
        this.props.callback(this.props.data);
        return false;
    },

    showCreate: function() {
        $("#add-button-container").hide();
        $("#title-container").show();
        return false;
    },

    cancelCreate: function() {
        $("#add-button-container").show();
        $("#title-container").hide();
        return false;
    },

    getInitialState: function() {
        return {
            errors: {
                title: "",
                description: ""
            }
        };
    },

    render: function() {
        if (this.props.data != undefined) {
            return (
                <div id="title-container" class="panel panel-default">
                    <div class="panel-heading" data-toggle="collapse" data-parent="#title-container"
                        data-target="#module-title">
                        <span class="heading"> Question Module Description </span>
                    </div>
                    <div class="panel-body" id="module-title">
                        <div>
                            <div class="col-md-12 form-group">
                                <WmdTextarea ref="title" placeholder="Question Module Description"
                                    defaultValue={this.props.data.title} />
                            </div>
                        </div>
                        <div>
                            <div class="col-md-3 col-md-offset-2">
                                <button onClick={this.createQuestionModule}
                                    type="submit" class="btn btn-primary">Save</button>
                            </div>
                            <div class="col-md-3 col-md-offset-2">
                                <button onClick={this.returnWithoutCreate} class="btn btn-danger">
                                    Cancel</button>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
        return (
            <div>
                <div class="row" id="add-button-container">
                    <div class="col-md-2 col-md-offset-8">
                        <button onClick={this.showCreate} class="btn btn-primary">
                            Add Question Module
                        </button>
                    </div>
                </div>
                <div id="title-container" class="panel panel-default" style={{'display': 'none'}}>
                    <div class="panel-heading" >
                        <span class="heading"> Question Module Description </span>
                    </div>
                    <div class="panel-body" id="module-title">
                        <div class="col-md-12 form-group">
                            <WmdTextarea ref="title" placeholder="Question Module Description" />
                        </div>
                        <div class="col-md-2 col-md-offset-3">
                            <button onClick={this.createQuestionModule}
                                type="submit" class="btn btn-primary">Save</button>
                        </div>
                        <div class="col-md-2 col-md-offset-2">
                            <button onClick={this.cancelCreate} class="btn btn-danger">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

});

var QuestionModuleEditRow = React.createClass({

    mixins: [confirmDeleteMixin],

    base_url: "/quiz/api/",

    editQuestionModule: function() {
        this.props.editCallback(this.props.data);
        return false;
    },

    deleteObject: function() {
        if (this.checkDeleteStage()) return;
        url = this.base_url + "question_module/" + this.props.data.id + "/?format=json";
        request = ajax_json_request(url, "DELETE", {});
        request.done(function(response) {
            this.props.deleteCallback(this.props.data);
        }.bind(this));
        request.complete(function(response) {
            this.resetDelete();
        }.bind(this));
    },

    render: function() {
        delete_bar = this.getDeleteBar();
        var _title = converter.makeHtml(this.props.data.title);
        return (
            <tr>
                <td>
                    <button type="button" class="btn btn-default btn-sm" onClick={this.editQuestionModule}>
                        Edit
                    </button>
                </td>
                <td>{this.props.data.id}</td>
                <td><span dangerouslySetInnerHTML={{__html: _title}} /></td>
                <td>
                    {delete_bar}
                </td>
            </tr>
        );
    }

});

var QuizEditAdmin = React.createClass({

    // TODO: Use a mixin to implement functionality of QuizEditAdmin and QuizAdmin
    //        when the course module is completed and quizzes are fetched from the
    //        course instead of list(quiz)

    closePanel: function() {
        close_question_list();
        close_question_module_list(QuizEditAdminId);
    },

    base_url: "/quiz/api/",

    openQuestionModule: null,

    getInitialState: function() {
        this.getQuestionModules();
        console.log(this.props.quiz);
        return {
            loaded: false
        };
    },

    editQuestionModule: function(data) {
        this.openQuestionModule = data.id;
        $("#" + QuestionModuleEditId).html("");
        React.renderComponent(
            <QuestionModuleEditAdmin question_module={data} quiz={this.props.quiz}
                refreshCallback={this.refresh}/>,
            document.getElementById(QuestionModuleEditId)
        );
        $("#" + QuestionModuleEditId).hide().fadeIn();
    },

    createQuestionModule: function(data) {
        oldState = this.state;
        oldState.question_modules.push(data);
        this.setState(oldState);
        this.editQuestionModule(data);
    },

    deleteQuestionModule: function(data) {
        if (this.openQuestionModule == data.id) {
            close_question_list();
            window.scrollTo(0, document.getElementById(QuizEditAdminId).offsetTop-75);
        }
        question_modules = this.state.question_modules;
        index = question_modules.indexOf(data);
        if (index > -1) {
            question_modules.splice(index, 1);
        }
        oldState = this.state;
        oldState.question_modules = question_modules;
        this.setState(oldState);
    },

    getQuestionModules: function() {
        url = this.base_url + "quiz/" + this.props.quiz.id + "/get_question_modules/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState.question_modules = response;
            oldState.loaded = true;
            this.setState(oldState);
        }.bind(this));
    },

    refresh: function() {
        this.getQuestionModules();
    },

    componentDidMount: function() {
        $('html,body').animate({
            scrollTop: $(this.getDOMNode()).offset().top - 100
        }, 1000).bind(this);
    },

    render: function() {
        if (!this.state.loaded) {
            return (
                <div class="panel panel-default">
                    <div class="panel-heading text-center"><LoadingBar /></div>
                </div>
            );
        }
        qm_edit = this.state.question_modules.map(function(q) {
            return <QuestionModuleEditRow editCallback={this.editQuestionModule} deleteCallback={this.deleteQuestionModule} data={q} />;
        }.bind(this));
        return (
            <div class="panel panel-default">
                <div class="panel-heading">
                    <span class="quiz-text-mute quiz-right-margin">Editing</span>
                    <strong>{this.props.quiz.title}</strong>
                    <span class="pull-right">
                        <button type="button" class="close" onClick={this.closePanel}>&times;</button>
                    </span>
                </div>
                <div class="panel-body">
                    <QuestionModuleCreate quiz_id={this.props.quiz.id} callback={this.createQuestionModule}/>
                </div>
                <table class="table table-hover quiz-table">
                    <tbody>
                        <tr>
                            <th width="11%"></th>
                            <th>ID</th>
                            <th>Title</th>
                            <th class="confirm-delete">
                                <span class="pull-right">
                                    <button class="btn btn-default" title="Refresh">
                                        <span class="glyphicon glyphicon-refresh" onClick={this.refresh}></span>
                                    </button>
                                </span>
                            </th>
                        </tr>
                        {qm_edit}
                    </tbody>
                </table>
            </div>
        );
    }

});


var QuizCreate = React.createClass({

    base_url: "/quiz/api/",

    // always return false
    createQuiz: function() {
        url = this.base_url + "quiz/?format=json";
        data = {
            title: this.refs.title.getDOMNode().value.trim()
        };
        this.refs.title.getDOMNode().value = '';
        request = ajax_json_request(url, "POST", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            data = response;
            this.props.callback(data);
        }.bind(this));
        request.complete(function(response) {
            if (response.status == 400) {
                // BAD REQUEST - Data Validation failed
                response = jQuery.parseJSON(response.responseText);
                if (response.title != undefined) {
                    // TODO: replace with foreach (this.refs)
                    title_input = $(this.refs.title.getDOMNode());
                    add_error_to_element(title_input, response.title);
                }
            }
            else {
                title_input = $(this.refs.title.getDOMNode());
                remove_error_from_element(title_input);
            }
        }.bind(this));
        return false;
    },

    getInitialState: function() {
        return {
            errors: {
                title: ""
            }
        };
    },

    render: function() {
        return (
            <form role="form" class="form-inline" onSubmit={this.createQuiz}>
                <div class="col-md-2 form-group">
                    <button type="submit" class="btn btn-primary">Add Quiz</button>
                </div>
                <div class="col-md-4 form-group">
                    <input type="text" class="form-control" ref="title" placeholder="Quiz Title" />
                </div>
            </form>
        );
    }

});

var QuizEditRow = React.createClass({

    mixins: [confirmDeleteMixin],

    base_url: "/quiz/api/",

    editQuiz: function() {
        this.props.editCallback(this.props.data);
        return false;
    },

    deleteObject: function() {
        if (this.checkDeleteStage()) return;
        url = this.base_url + "quiz/" + this.props.data.id + "/?format=json";
        request = ajax_json_request(url, "DELETE", {});
        request.done(function(response) {
            this.props.deleteCallback(this.props.data);
        }.bind(this));
        request.complete(function(response) {
            this.resetDelete();
        }.bind(this));
    },

    render: function() {
        delete_bar = this.getDeleteBar();
        return (
            <tr>
                <td>
                    <button type="submit" class="btn btn-default btn-sm" onClick={this.editQuiz}>
                        Edit
                    </button>
                </td>
                <td>{this.props.data.title}</td>
                <td>{this.props.data.marks}</td>
                <td>{this.props.data.question_modules}</td>
                <td>{this.props.data.questions}</td>
                <td>
                    {delete_bar}
                </td>
            </tr>
        );
    }

});

var QuizAdmin = React.createClass({

    /*
     * We do not update the question stats in this component using callbacks
     * since we want to be able to include any component anywhere on the platform
     * and doing so will make it more complex for reusablity. Hence we provide
     * a REFRESH button
     */

    base_url: "/quiz/api/",

    openQuiz: null,

    getInitialState: function() {
        this.getQuizzes();
        return {
            loaded: false
        };
    },

    editQuiz: function(data) {
        this.openQuiz = data.id;
        $("#" + QuizEditAdminId).html("");
        React.renderComponent(
            <QuizEditAdmin quiz={data} />,
            document.getElementById(QuizEditAdminId)
        );
        $("#" + QuizEditAdminId).hide().fadeIn();
    },

    createQuiz: function(data) {
        oldState = this.state;
        oldState.quizzes.push(data);
        this.setState(oldState);
        this.editQuiz(data);
    },

    deleteQuiz: function(data) {
        if (this.openQuiz == data.id) {
            close_question_list();
            close_question_module_list();
            window.scrollTo(0, document.getElementById(QuizAdminId).offsetTop-75);
        }
        quizzes = this.state.quizzes;
        index = quizzes.indexOf(data);
        if (index > -1) {
            quizzes.splice(index, 1);
        }
        oldState = this.state;
        oldState.quizzes = quizzes;
        this.setState(oldState);
    },

    getQuizzes: function() {
        url = this.base_url + "quiz/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState.quizzes = response;
            oldState.loaded = true;
            this.setState(oldState);
        }.bind(this));
    },

    refresh: function() {
        this.getQuizzes();
    },

    render: function() {
        if (!this.state.loaded) {
            return (
                <div class="panel panel-default">
                    <div class="panel-heading text-center"><LoadingBar /></div>
                </div>
            );
        }
        else {
            quiz_edit = this.state.quizzes.map(function(q) {
                return <QuizEditRow editCallback={this.editQuiz} deleteCallback={this.deleteQuiz} data={q} />;
            }.bind(this));

            return (
                <div class="panel panel-default">
                    <div class="panel-heading">
                        Course Quizzes
                        <span class="pull-right quiz-text-mute">Admin Panel</span>
                    </div>
                    <div class="panel-body">
                        <QuizCreate callback={this.createQuiz} />
                        <span class="pull-right">
                            <button class="btn btn-default" title="Refresh">
                                <span class="glyphicon glyphicon-refresh" onClick={this.refresh}></span>
                            </button>
                        </span>
                    </div>
                    <table class="table table-hover quiz-table">
                        <tbody>
                            <tr>
                                <th></th>
                                <th>Title</th>
                                <th>Maximum points</th>
                                <th>Question modules</th>
                                <th>Questions</th>
                                <th class="confirm-delete"></th>
                            </tr>
                            {quiz_edit}
                        </tbody>
                    </table>
                </div>
            );
        }
    }
});



