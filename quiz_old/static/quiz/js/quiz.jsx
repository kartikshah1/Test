/** @jsx React.DOM */

var Paginator = React.createClass({
	setPage: function(event) {
		element_a = $(event.target);
		element_li = element_a.parent();
		pos = element_li.index();
		if (this.props.totalPages <= this.props.maxPages) {
			this.props.callback(this.state.start + pos);
		}
		else {
			if (pos == 0) {
				start_ = (this.state.start == 1) ? 1 : (this.state.start - 1);
				end_ = start_ + this.props.maxPages - 1;
				this.setState({start: start_, end: end_});
			}
			else if (pos == (this.props.maxPages + 1)) {
				end_ = (this.state.end == this.props.totalPages) ? this.state.end : (this.state.end + 1);
				start_ = end_ - this.props.maxPages + 1;
				this.setState({start: start_, end: end_});
			}
			else {
				this.props.callback(this.state.start + pos - 1);
			}
		}
	},
	getInitialState: function() {
		return {
			start: 0,
			end: 0
		};
	},
	componentWillMount: function() {
		start_ = 1;
		end_ = this.props.totalPages > this.props.maxPages ?
				this.props.maxPages :
				this.props.totalPages;
		this.setState({start: start_, end: end_});
	},
	render: function() {
		// parameters:
		//   maxPages
		//   totalPages
		//   callback function
		var prev;
		var next;
		if (this.props.totalPages > this.props.maxPages) {
			prev = <li><a href="javascript:void(0);" refs="prev" onClick={this.setPage}>&laquo;</a></li>;
			next = <li><a href="javascript:void(0);" refs="next" onClick={this.setPage}>&raquo;</a></li>;
		}
		pages = [];
		for (var i = this.state.start; i <= this.state.end; i++) {
			element = <li><a href="javascript:void(0);" refs={i} onClick={this.setPage}>{i}</a></li>;
			pages[i-1] = element;
		}
		return (
			<ul class="pagination">
				{prev}
				{pages}
				{next}
			</ul>
		);
	}
});

var QUESTION_TYPES = {
    SINGLE_CHOICE_QUESTION: 'S',
	MULTIPLE_CHOICE_QUESTION: 'M',
	FIXED_ANSWER_QUESTION: 'F',
	DESCRIPTIVE_ANSWER_QUESTION: 'D',
	PROGRAMMING_QUESTION: 'P'
};

var FixedAnswerQuestion = React.createClass({

	disableSubmit: function() {
		$(this.refs.submit.getDOMNode()).attr('disabled','disabled');
	},

	enableSubmit: function() {
		$(this.refs.submit.getDOMNode()).removeAttr('disabled');
	},

	submitAnswer: function() {
		answer = this.refs.answer.getDOMNode().value.trim();
		if (answer == '') return;
		this.disableSubmit();
		this.props.submitCallback(answer, this.enableSubmit);
	},

    render: function() {
        return (
        	<form role="form">
				<div class="col-md-4 no-padding">
					<div class="input-group">
						<input type="text" class="form-control" ref="answer" placeholder="Answer" />
						<span class="input-group-btn">
							<button ref="submit" onClick={this.submitAnswer} class="btn btn-primary" type="button">Submit</button>
						</span>
					</div>
				</div>
    		</form>
        );
    }
});

var StatusBar = React.createClass({

	getInitialState: function() {
		show = true;
		if (this.props.show != undefined) {
			show = this.props.show;
		}
		return {
			show: show
		};
	},
	
	show: function() {
		state = this.state;
		state.show = true;
		this.setState(state);
	},

	render: function() {
		class_name = "alert alert-sm alert-" + this.props.type;
		text = "";
		bold_text = <strong>{this.props.bold_text}</strong>;
		if (this.state.show) {
			text = this.props.text;
		}
		else {
			bold_text =
				<a href="javascript:void(0)" class="link-normal-text" onClick={this.show}>
					{bold_text}
				</a>;
		}
		
		return (
			<div class={class_name}>
				{bold_text}
				<br/>
				{text}
			</div>
		);
	}

});

var Question = React.createClass({

	base_url: "/quiz/api/",

	loadHint: function() {
		url = this.base_url + "question/" + this.props.data.id + "/get_hint/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState["hint"] = response;
            this.setState(oldState);
        }.bind(this));
	},

	loadAnswer: function() {
		url = this.base_url + "question/" + this.props.data.id + "/get_answer/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState["answer"] = response;
            this.setState(oldState);
        }.bind(this));
    },

    submitAnswer: function(answer, callback) {
    	url = this.base_url + "question/" + this.props.data.id + "/submit_answer/?format=json";
    	request = ajax_json_request(url, "POST", {"answer": answer});
    	request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState.data.attempts += 1;
            oldState.data.marks = response.result;
            if (response.status == 'D') { // correct answer
            	oldState.answer = {};
            	if (response.is_correct) {
            		oldState.answer["bold_text"] = 'Correct!';
                	oldState.answer["text"] = response.answer;
                	oldState.answer["type"] = 'success';
            	}
            	else {
                	oldState.answer["bold_text"] = 'Wrong answer!';
                	oldState.answer["text"] = '';
                	oldState.answer["type"] = 'danger';
            	}
            	if (response.attempts_remaining == 0 || response.is_correct) {
	            	oldState.answer["answer"] = response.answer;
	            	oldState.answer["answer_description"] = response.answer_description;
					prefix = "The correct answer is ";
					if ((oldState.answer["answer"].split(",").length - 1) > 1) {
						prefix = "The correct answers are ";
					}
					oldState.answer["text"] = prefix + response.answer;
            	}
            	oldState["showRefresh"] = false;
            	this.setState(oldState);
            }
            else if (response.status == 'A') { // Awaiting results
            	oldState.answer = {};
            	oldState.answer["bold_text"] = 'Awaiting evaluation!';
            	oldState.answer["text"] = '';
            	oldState.answer["type"] = 'info';
            	oldState["showRefresh"] = true;
            	this.setState(oldState);
            }
    	}.bind(this));
    	request.complete(function() {
    		if (callback != undefined) {
            	callback();
            }
    	}.bind(this));
    },

	getInitialState: function() {
        state = {
        	data: {
        		attempts: this.props.data.user_attempts,
        		marks: this.props.data.user_marks,
        	},
        	status: this.props.data.user_status
        };
        if (this.props.data.answer_shown) {
        	state["answer"] = {
        		//text: "Already answered",
        		//type: "info",
        		answer: this.props.data.answer,
        		answer_description: this.props.data.answer_description
        	};
        }
        if (this.props.data.hint_taken) {
        	state["hint"] = {
    			hint: this.props.data.hint
        	};
        }
		return state;
	},

	render: function() {
		answer_box = <div></div>;
		if (this.props.data.type == QUESTION_TYPES.FIXED_ANSWER_QUESTION) {
			answer_box = <FixedAnswerQuestion submitCallback={this.submitAnswer}/>
		}
        answer_status = <div></div>;
    	answer_description = <div></div>;
    	hint = <div></div>;
    	hint_button = <div></div>;
    	// If there exists some status message for the answer then show it
    	// If there exists the answer_description then show it
        if (this.state.answer != undefined && this.state.answer.text != undefined) {
        	if (this.state.answer.bold_text == undefined) this.state.answer.bold_text = '';
    		answer_status = <StatusBar type={this.state.answer.type} text={this.state.answer.text} bold_text={this.state.answer.bold_text} />;
    		if (this.state.answer.answer != undefined && this.state.answer.answer_description != undefined) {
    			answer_description = <StatusBar type="info" text={this.state.answer.answer_description} bold_text="Answer Description" />;
    		}
        }
        // If the answer has been shown, show the answer and the description
        if (this.props.data.answer_shown) {
        	answer_status = <StatusBar show={false} type="success" text={this.props.data.answer} bold_text="Answer" />
			answer_description = <StatusBar show={false} type="info" text={this.props.data.answer_description} bold_text="Answer Description" />;
        }
        if (this.state.hint != undefined && this.state.hint.hint != undefined) {
			if (this.props.data.hint != undefined) {
				hint = <StatusBar type="warning" text={this.state.hint.hint} bold_text="Hint" show={false} />;
			}
        	else {
				hint = <StatusBar type="warning" text={this.state.hint.hint} bold_text="Hint" />;
			}
        }
        else if (this.props.data.is_hint_available) {
        	hint_button = <button type="button" class="btn btn-warning" onClick={this.loadHint} >Hint</button>
        }

        var _description = converter.makeHtml(this.props.data.description);
    	return (
    		<div class="question">
    			<div class="question-metadata quiz-text-mute">
    				{this.state.data.marks} / {this.props.data.marks} points
    				<div class="pull-right">
    					{this.state.data.attempts} / {this.props.data.attempts} attempts
    				</div>
    			</div>
    			<div class="question-text">
    				<span dangerouslySetInnerHTML={{__html: _description}} />
				</div>
    			<div class="question-submit">
    				{answer_box}
    				<div class="pull-right">
    					{hint_button}
					</div>
				</div>
				<div class="question-hint">
					{hint}
				</div>
				<div class="question-status">
					{answer_status}
					{answer_description}
				</div>
			</div>
        );
    }
});


var QuestionModule = React.createClass({

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
        return (
			<ul class="list-group">
				<li class="list-group-item">
					<span dangerouslySetInnerHTML={{__html: _title}} />
				</li>
				{questions}
			</ul>
        );
    }
});


var Quiz = React.createClass({

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

	render: function() {
		if (this.state.quiz_loaded) {
			if (this.state.loaded) {
				currentId = this.state.questionModules[this.state.current]["id"];
				modules = this.state.questionModules.map(function(module) {
					visible = false;
					if (module.id == currentId) visible = true;
					return (<QuestionModule data={module} visible={visible}/>);
				}.bind(this));
			}
			else {
				modules =
					<div class="panel panel-default">
	    				<div class="panel-heading text-center"><LoadingBar /></div>
    				</div>;
				this.loadQuestionModules();
			}
			return (
	    		<div class="panel panel-default">
	    			<div class="panel-heading">
    					{this.state.data.title}
    					<div class="pull-right">
    						Maximum points: {this.state.data.marks}
						</div>
	    			</div>
	    			<div class="panel-body text-center">
	    				<Paginator
	    					totalPages={this.state.data.question_modules}
	    					maxPages={5}
	    					callback={this.setPage} />
	    			</div>
					{modules}
				</div>
	        );
		}
		else {
			this.loadQuiz();
			return (
	    		<div class="panel panel-default">
	    			<div class="panel-heading text-center"><LoadingBar /></div>
	    		</div>
			);
		}
    }
});


React.renderComponent(
    <Quiz id="1" />,
    document.getElementById('quiz')
);


