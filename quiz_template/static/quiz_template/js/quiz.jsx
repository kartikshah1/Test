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
    SINGLE_CHOICE_QUESTION: 'scq',
	MULTIPLE_CHOICE_QUESTION: 'mcq',
	FIXED_ANSWER_QUESTION: 'fix',
	DESCRIPTIVE_ANSWER_QUESTION: 'des',
};


// FixedAnswerQuestion
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

//DescriptiveAnswerQuestion
var DescriptiveAnswerQuestion = React.createClass({

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
						<textarea class="form-control" ref="answer" placeholder="Answer" />
						<span class="input-group-btn">
							<button ref="submit" onClick={this.submitAnswer} class="btn btn-primary" type="button">Submit</button>
						</span>
					</div>
				</div>
    		</form>
        );
    }
});


// SingleChoiceQuestion
//*
var SingleChoiceQuestion = React.createClass({
	disableSubmit: function() {
		$(this.refs.submit.getDOMNode()).attr('disabled','disabled');
	},

	enableSubmit: function() {
		$(this.refs.submit.getDOMNode()).removeAttr('disabled');
	},

	submitAnswer: function() {
		//answer = this.refs.option_group.getDOMNode().getElementById("options_" + this.props.id);
		// TODO :temporary fix, figure out a way of doing using React
		answer = $('input[name=options_'+this.props.id+']:checked').val();
		console.log(answer)
		if (answer == '') return;
		this.disableSubmit();
		this.props.submitCallback(answer, this.enableSubmit);
	},
	render: function() {
		var group_name = "options_" + this.props.id
		var options = jQuery.parseJSON(this.props.options);
		var optionNodes = options.map(function(option, i) {
			 return <div class="radio"><label><input type="radio" name={group_name} value={i}>{option}</input></label></div>
		});
		return(
			<form role="form" ref="option_group">
				<div class="col-md-4 no-padding">
						{optionNodes}
							<button ref="submit" onClick={this.submitAnswer} class="btn btn-primary" type="button">Submit</button>
				</div>
			</form>
		);
	}
});
//*/

// MultipleChoiceQuestion
//*
var MultipleChoiceQuestion = React.createClass({
	disableSubmit: function() {
		$(this.refs.submit.getDOMNode()).attr('disabled','disabled');
	},

	enableSubmit: function() {
		$(this.refs.submit.getDOMNode()).removeAttr('disabled');
	},

	submitAnswer: function() {
		//answer = this.refs.option_group.getDOMNode().getElementById("options_" + this.props.id);
		// TODO :temporary fix, figure out a way of doing using React
		selected = $('input[name=options_'+this.props.id+']').map(function(node) {
			return this.checked;
		});
		var options = jQuery.parseJSON(this.props.options);
		answer = []
		for (var i = 0; i < options.length; i++){
			answer[i] = selected[i];
		}
		console.log(JSON.stringify(answer))
		if (answer == '') return;
		this.disableSubmit();
		this.props.submitCallback(JSON.stringify(answer), this.enableSubmit);
	},
	render: function() {
		var group_name = "options_" + this.props.id
		var options = jQuery.parseJSON(this.props.options);
		// console.log(options);
		var optionNodes = options.map(function(option, i) {
			 return <div class="checkbox"><label><input type="checkbox" name={group_name}>{option}</input></label></div>
		});
		return(
			<form role="form" ref="option_group">
				<div class="col-md-4 no-padding">
						{optionNodes}
							<button ref="submit" onClick={this.submitAnswer} class="btn btn-primary" type="button">Submit</button>
				</div>
			</form>
		);
	}
});
//*/

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

	base_url: "/quiz_template/api/",

	loadHint: function() {
		url = this.base_url + "question_master/" + this.props.data.id + "/get_hint/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState["hint"] = response;
            this.setState(oldState);
        }.bind(this));
	},

    submitAnswer: function(answer, callback) {
    	url = this.base_url + "question_master/" + this.props.data.id + "/submit_answer/?format=json";
    	request = ajax_json_request(url, "POST", {"answer": answer});
    	request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState.data.attempts += 1;
            oldState.data.marks = response.marks;
            if (response.status == 'C') { // correct answer
            	console.log('got correct answer');
            	oldState.answer = {};
                oldState["showRefresh"] = false;
                if (this.props.data.marks == 0) {
                    oldState.answer["bold_text"] = 'Did you get it right ?';
                    oldState.answer["text"] = 'The correct answer is ' + response.answer;;
                    oldState.answer["type"] = 'info';
                } else {
                    oldState.answer["bold_text"] = 'Correct!';
                    oldState.answer["text"] = "The correct answer is " + response.answer;
                    oldState.answer["type"] = 'success';
                }
                oldState.answer["answer"] = response.answer;
                this.setState(oldState); 
            }
        	else if(response.status == 'W'){
                oldState.answer = {};
                oldState["showRefresh"] = false;
                if (this.props.data.marks != 0) {
                	oldState.answer["bold_text"] = 'Wrong answer!';
                	oldState.answer["text"] = "The correct answer is " + response.answer;
                	oldState.answer["type"] = 'danger';
                } else {
                    oldState.answer["bold_text"] = 'Did you get it right ?';
                    oldState.answer["text"] = 'The correct answer is ' + response.answer;
                    oldState.answer["type"] = 'info';
                }
                oldState.answer["answer"] = response.answer;
                oldState.data["explaination"] = response.explaination;
                this.setState(oldState);
        	}
            else if (response.status == 'A') {
            	oldState.answer = {};
            	oldState.answer["bold_text"] = 'Attempt Wrong';
            	oldState.answer["text"] = '';
            	oldState.answer["type"] = 'info';
            	oldState["showRefresh"] = true;
                oldState.data["explaination"] = response.explaination;
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
                explaination: this.props.data.explaination
        	},
        	status: this.props.data.user_status
        };
        if (this.props.data.answer_shown) {
        	state["answer"] = {
        		answer: this.props.data.answer
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
			answer_box = <FixedAnswerQuestion submitCallback={this.submitAnswer}/>;
		}
		else if (this.props.data.type == QUESTION_TYPES.SINGLE_CHOICE_QUESTION){
			 answer_box = <SingleChoiceQuestion submitCallback={this.submitAnswer}
			 	options={this.props.data.options} id={this.props.data.id}/>;
		}
		else if (this.props.data.type == QUESTION_TYPES.MULTIPLE_CHOICE_QUESTION){
			 answer_box = <MultipleChoiceQuestion submitCallback={this.submitAnswer}
			 	options={this.props.data.options} id={this.props.data.id}/>;
		}
		else if (this.props.data.type == QUESTION_TYPES.DESCRIPTIVE_ANSWER_QUESTION){
			 answer_box = <DescriptiveAnswerQuestion submitCallback={this.submitAnswer}/>;
		}
        answer_status = <div></div>;
    	explaination = <div></div>;
    	hint = <div></div>;
    	hint_button = <div></div>;
    	// If there exists some status message for the answer then show it
    	// If there exists the answer_description then show it
        if (this.state.answer != undefined && this.state.answer.text != undefined) {
        	if (this.state.answer.bold_text == undefined) this.state.answer.bold_text = '';
    		answer_status = <StatusBar type={this.state.answer.type} text={this.state.answer.text} bold_text={this.state.answer.bold_text} />;
        }
        // If the answer has been shown, show the answer and the description
        if (this.props.data.answer_shown) {
            if(this.props.data.user_status == 'C')
        	   answer_status = <StatusBar show={true} type="success" text={this.props.data.answer} bold_text="Answer" />
            else if(this.props.data.user_status == 'W')
                answer_status = <StatusBar show={true} type="danger" text={this.props.data.answer} bold_text="Answer" />
        }
        if (this.state.hint != undefined && this.state.hint.hint != undefined) {
			if (this.props.data.hint != undefined) {
				hint = <StatusBar type="warning" text={this.state.hint.hint} bold_text="Hint" show={true} />;
			}
        	else {
				hint = <StatusBar type="warning" text={this.state.hint.hint} bold_text="Hint" />;
			}
        }
        else if (this.props.data.is_hint_available) {
        	hint_button = <button type="button" class="btn btn-warning" onClick={this.loadHint} >Hint</button>
        }
        if(this.state.data.explaination != "")
            explaination = <StatusBar show={true} type="info" text={this.state.data.explaination} bold_text="Explaination" />;

        var _text = converter.makeHtml(this.props.data.text);
    	return (
    		<div class="question">
    			<div class="question-metadata quiz-text-mute">
    				{this.state.data.marks} / {this.props.data.marks} points
    				<div class="pull-right">
    					{this.state.data.attempts} / {this.props.data.attempts} attempts
    				</div>
    			</div>
    			<div class="question-text">
    				<span dangerouslySetInnerHTML={{__html: _text}} />
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
                    {explaination}
				</div>
			</div>
        );
    }
});


var QuestionModule = React.createClass({

	base_url: "/quiz_template/api/",

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
    	titlenode = (
    		<li class="list-group-item text-center">
				<span dangerouslySetInnerHTML={{__html: _title}} />
			</li>
		);

		var _static_question = converter.makeHtml(this.props.data.static_text);
        var static_node = null;
        if(_static_question != ""){
	    	static_node = (
	    		<li class="list-group-item">
					<span dangerouslySetInnerHTML={{__html: _static_question}} />
				</li>
			);
	    }

        return (
			<ul class="list-group">
				{titlenode}
				{static_node}
				{questions}
			</ul>
        );
    }
});


/*
	Component : Quiz
*/
var Quiz = React.createClass({

	base_url: "/quiz_template/api/",

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
            var paginator = null;
			if (this.state.loaded) {
                if (this.state.questionModules.length > 1){
                    paginator = (
                        <div class="panel-body text-center">
                            <Paginator
                                totalPages={this.state.questionModules.length}
                                maxPages={5}
                                callback={this.setPage} />
                        </div>
                    );
                }
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
	    		<div class="panel panel-default quiz-panel">
	    			<div class="panel-heading">
    					{this.state.data.title}
    					<div class="pull-right">
    						Maximum points: {this.state.data.marks}
						</div>
	    			</div>
	    			{paginator}
					{modules}
				</div>
	        );
		}
		else {
			this.loadQuiz();
			return (
	    		<div class="panel panel-default quiz-panel">
	    			<div class="panel-heading text-center"><LoadingBar /></div>
	    		</div>
			);
		}
    }
});

//*
var QuizList = React.createClass({
	base_url : "/quiz_template/api/",
	loadQuizList: function() {
		url = this.base_url + "quiz/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState.quiz_list = response;
            oldState.list_loaded = true;
            this.setState(oldState);
        }.bind(this));
	},
	getInitialState: function() {
		return {
			list_loaded: false,
			quiz_list : []
		}
	},
	render: function() {
		if (this.state.list_loaded) {
			var quizNodes = this.state.quiz_list.map(function(quiz) {
				return <Quiz id={quiz.id} />
			});
			return (
				<div>
					{quizNodes}
				</div>
			)
		}
		else {
			this.loadQuizList();
			return(
				<div>
					<LoadingBar />
				</div>
			)
		}
	}
});
//*/

/*
React.renderComponent(
    <QuizList />,
    document.getElementById('quiz')
);
*/

var ConceptQuiz = React.createClass({

    base_url: "/quiz/api/",

    componentWillReceiveProps: function(nextProps) {
        this.setState({
            id: nextProps.id,
            loaded: false,
            quiz_loaded: false,
            current: undefined,
            questionModules: undefined,
            data: undefined
        });
    },

    setPage: function(action) {
        oldState = this.state;
        oldState.current = (action - 1);
        this.setState(oldState);
    },

    loadQuiz: function() {
        url = this.base_url + "quiz/" + this.state.id + "/?format=json";
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
        url = this.base_url + "quiz/" + this.state.id + "/get_question_modules/?format=json";
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
            id: this.props.id,
            loaded: false,
            quiz_loaded: false,
            current: undefined,
            questionModules: undefined,
            data: undefined
        };
    },

    close: function(){
        if (this.props.closeCallback) this.props.closeCallback();
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
            marksString = "Maximum points:" + this.state.data.marks;
            close_button = "";
            if (this.props.closeCallback) {
                close_button = <button type="button"
                                        class="btn btn-primary btn-sm"
                                        onClick={this.close}>
                                        Resume Video
                                    </button>;
            } else {
                close_button = <button type="button"
                                        class="btn btn-primary btn-sm"
                                        onClick={this.close}>
                                        Done
                                    </button>;
            }
            return (
                <div class="panel panel-default quiz-panel">
                    <div class="panel-heading" style={{"overflow":"auto"}}>
                        {this.state.data.title}
                        <div class="pull-right">
                            {this.props.inVideo ?
                                marksString :
                                close_button
                            }
                        </div>
                    </div>
                    {paginator}
                    {modules}
                </div>
            );
        }
        else {
            this.loadQuiz();
            return (
                <div class="panel panel-default quiz-panel">
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
