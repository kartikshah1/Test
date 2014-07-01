/** @jsx React.DOM */

// TODO: Disable buttons when ajax request is sent
//			Enable back when request completes

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


var QuizAdminId = 'quiz-admin';
var QuizEditAdminId = 'quiz-edit-admin';
var QuestionModuleEditId = 'question-module-edit-admin';

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
	$("#" + QuestionModuleEditId).fadeOut(function() {
		$(this).html("");
	});
}

function close_question_module_list() {
	$("#" + QuizEditAdminId).fadeOut(function() {
		$(this).html("");
	});
}

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

var FixedAnswerQuestionCreate = React.createClass({

	setAnswer: function(answer) {
		answer = answer.toString();
		this.props.onChange({answer: answer});
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
		//	default value of answer
		this.setAnswer(this.state.answer);
		id = this.props.answerId;
		return (
			<div class="form-group">
				<label class="control-label col-md-2">Correct Answer</label>
				<div class="col-md-7">
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

	base_url: '/quiz/api/',

	answer_box_id: 'answer_box',

	createQuestion: function() {

		console.log(this.state);
	
		if (this.state['answer'] == undefined || this.state['answer'] == '') {
			add_error_to_element($("#" + this.answer_box_id), 'This field is required.');
			return;
		}

		url = '';
		method = '';
		if (this.refs.type.getDOMNode().value == QUESTION_TYPES.FIXED_ANSWER_QUESTION) {
			if (this.props.edit) {
				url = this.base_url + "fixed_answer_question/" + this.props.defaults.id + "/?format=json";
				method = 'PATCH';
			}
			else {
				url = this.base_url + "question_module/" + this.props.question_module.id + '/add_fixed_answer_question/?format=json';
				method = 'POST';
			}
		} // Add more types here


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

        request = ajax_json_request(url, method, data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            data = response;
			data['answer_fields'] = {};
			for (var attrname in this.state.answer_props) {
				data.answer_fields[attrname] = this.state[attrname];
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
		console.log("setAnswer");
		console.log(obj);
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
		if (state.granularity == '') {
			state.granularity = [];
		}
		else {
			state.granularity = state.granularity.split(",");
		}
		if (state.granularity_hint == '') {
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

	validationFields: new Array('description', 'answer_description', 'hint', 'granularity', 'granularity_hint', 'marks', 'grader_type', 'type', 'attempts'),

	removeValidation: function() {
		// this may not be needed because after creation, the parent of QuestionCreate should be re-rendered and hence this module
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
	
	render: function() {
		answer_box = <div></div>;
		if (this.state.defaults.type == QUESTION_TYPES.FIXED_ANSWER_QUESTION) {
			answer_box = <FixedAnswerQuestionCreate defaults={this.state.defaults.answer_fields} onChange={this.setAnswer} answerId={this.answer_box_id} />
		}

		return (
			<form role="form" class="form-horizontal">
				<div class="form-group">
					<label class="control-label col-md-2">Description</label>
					<div class="col-md-7">
						<WmdTextarea ref="description" placeholder="Description" defaultValue={this.state.defaults.description} />
					</div>
				</div>
				<div class="form-group">
					<label class="control-label col-md-2">Marks</label>
					<div class="col-md-4">
						<input type="number" class="form-control" ref="marks" placeholder="Maximum marks" defaultValue={this.state.defaults.marks} />
					</div>
				</div>
				<div class="form-group">
					<label class="control-label col-md-2">Attempts</label>
					<div class="col-md-4">
						<input type="number" class="form-control" ref="attempts" placeholder="Maximum attempts" defaultValue={this.state.defaults.attempts} />
					</div>
				</div>
				<div class="form-group">
					<label class="control-label col-md-2">Granularity</label>
					<div class="col-md-6">
						<ListCreator check={this.checkGranularity} onChange={this.onGranularityChange} defaultValue={this.state.defaults.granularity} />
						<span class="help-block">Leave blank for default value</span>
					</div>
				</div>
				<div class="form-group">
					<label class="control-label col-md-2">Type</label>
					<div class="col-md-4">
						<select class="form-control" ref="type" onChange={this.changeType}  defaultValue={this.state.defaults.type}>
							<option value='F'>Fixed Answer Question</option>
						</select>
					</div>
				</div>
				{answer_box}
				<div class="form-group">
					<label class="control-label col-md-2">Hint</label>
					<div class="col-md-7">
						<WmdTextarea ref="hint" placeholder="Hint"  defaultValue={this.state.defaults.hint} />
					</div>
				</div>
				<div class="form-group">
					<label class="control-label col-md-2">Granularity after hint</label>
					<div class="col-md-6">
						<ListCreator check={this.checkGranularity} onChange={this.onHintGranularityChange}  defaultValue={this.state.defaults.granularity_hint} />
						<span class="help-block">Leave blank for default value</span>
					</div>
				</div>
				<div class="form-group">
					<label class="control-label col-md-2">Answer Description</label>
					<div class="col-md-7">
						<WmdTextarea ref="answer_description" placeholder="Answer Description"  defaultValue={this.state.defaults.answer_description} />
					</div>
				</div>
				<div class="form-group">
					<label class="control-label col-md-2">Grading Type</label>
					<div class="col-md-4">
						<select class="form-control" ref="grader_type" defaultValue={this.state.defaults.grader_type}>
							<option value='D'>Direct</option>
							<option value='M'>Manual</option>
						</select>
					</div>
				</div>
				<div class="form-group">
					<div class="col-md-offset-2 col-md-2">
						<button type="button" class="btn btn-primary" onClick={this.createQuestion}>Save Question</button>
					</div>
					<div class="col-md-4">
						<button type="button" class="btn btn-danger" onClick={this.props.closeCallback}>Close</button>
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
					<button type="submit" class="btn btn-default btn-sm" onClick={this.editQuestion}>
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

	getInitialState: function() {
		this.getQuestions();
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
		oldState = this.state;
		if (this.state.edit) {
			for (var i = 0; i < oldState.questions.length; i++) {
				if (oldState.questions[i]['id'] == data['id']) {
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
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState.questions = response;
            oldState.loaded = true;
            this.setState(oldState);
        }.bind(this));
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
		state.question_module = data;
		state.title_edit = false;
		display_global_message("Successfully saved", "success");
		this.setState(state);
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
			if (this.props.data == undefined) {
				this.refs.title.getDOMNode().value = '';
			}
		}.bind(this));
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
				<div>
					<div class="col-md-4 form-group">
						<button onClick={this.createQuestionModule} type="submit" class="btn btn-primary">Save Description</button>
					</div>
					<div class="col-md-8 form-group">
						<WmdTextarea ref="title" placeholder="Question Module Description" defaultValue={this.props.data.title} />
					</div>
				</div>
			);
		}
		return (
			<div>
				<div class="col-md-4 form-group">
					<button onClick={this.createQuestionModule} type="submit" class="btn btn-primary">Add Question Module</button>
				</div>
				<div class="col-md-8 form-group">
					<WmdTextarea ref="title" placeholder="Question Module Description" />
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
					<button type="submit" class="btn btn-default btn-sm" onClick={this.editQuestionModule}>
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
	//		  when the course module is completed and quizzes are fetched from the
	//		  course instead of list(quiz)

	closePanel: function() {
		close_question_list();
		close_question_module_list();
	},

	base_url: "/quiz/api/",

	openQuestionModule: null,

	getInitialState: function() {
		this.getQuestionModules();
		return {
        	loaded: false
    	};
	},

	editQuestionModule: function(data) {
		this.openQuestionModule = data.id;
		$("#" + QuestionModuleEditId).html("");
		React.renderComponent(
			<QuestionModuleEditAdmin question_module={data} quiz={this.props.quiz}/>,
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


React.renderComponent(
    <QuizAdmin id="1" />,
    document.getElementById(QuizAdminId)
);
$("#" + QuizAdminId).hide().fadeIn();
