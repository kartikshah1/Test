/** @jsx React.DOM */

var QuizAdminId = 'quiz-admin';
var QuizEditAdminId = 'quiz-edit-admin';
var QuestionModuleEditId = 'question-module-edit-admin';

React.renderComponent(
    <QuizAdmin id="1" />,
    document.getElementById(QuizAdminId)
);
$("#" + QuizAdminId).hide().fadeIn();