/** @jsx React.DOM */
var skipRules = skipRules || {};
skipRules.subsection = "";

var Responses = React.createClass({
    render: function() {
        var options = this.props.responses.map(function(r) {
            return (
                <label><input type="radio" name="responses" value="{r.pk}" />{r.fields.text}</label>
            );
        });
        return (
            <div>
                <label for="responses">Select Response</label>
                {options}
            </div>
        );
    }
});


var AllQuestions = React.createClass({
    render: function() {
        var options = this.props.questions
                .map(function(q) {
            return (
                <option value={q.pk}>{q.fields.text}</option>
            );
        });
        return (
            <div>
                <label for="root-question">{this.props.label}</label>
                <select name="root-question" id="root-question">
                {options}
                </select>
        </div>
        );
    }
});

var Question = React.createClass({
    getInitialState: function() {
        return (
            { selectedQuestion: {} }
        );
    },
    updateSelectedQuestion: function(event) {
        var e = document.getElementById("root-question");
        var v = e.options[e.selectedIndex].value;
        var question = this.props.questions.filter(function(q) { return q.pk == v; })[0];
        this.setState({selectQuestion: question});
        this.props.selectQuestion(question);
    },
    filterQuestions: function(q) { return q.fields.answer_type == "MultiChoice"; },
    render: function() {
        var options = this.props.questions
                .filter(this.filterQuestions)
                .map(function(q) {
            return (
                <option value={q.pk}>{q.fields.text}</option>
            );
        });
        if (this.props.questions.length > 0) {
            var responses = this.props.questions[0].options;
        }   
        return (
            <div>
                <label for="root-question">{this.props.label}</label>
                <select name="root-question" id="root-question" onChange={this.updateSelectedQuestion} value={this.state.selectedOption}>
                {options}
                </select>
                <Responses responses={responses || []} />
        </div>
        );
    }
});

var AddSkipRule = React.createClass({
    dummyFunction: function(a) { return true; },
    selectQuestion: function(question) {
        this.setState({selectedQuestion: question});
    },
    getInitialState: function() {
        return {
            selectedQuestion: {},
            questions: []};
    },

    render: function() {
        var selectedQuestion = this.state.selectedQuestion;
        var qs = this.state.questions.filter(function(q) { return q != selectedQuestion; });
        return (
            <div>
                <Question questions={this.state.questions} selectQuestion={this.selectQuestion} label="Select Root Question"/>
                <AllQuestions questions={qs} label="Select Question to Skip"/>
            </div>
        );
    }
});

var component = React.renderComponent(<AddSkipRule />, document.getElementById('id_create-skip-rule'));

var output= {};
skipRules.updateSubsection = function(subsectionId) {
    skipRules.subsection = subsectionId;
    $.get( "/questionnaire/subsection/" + subsectionId + "/questions/", function( data ) {
        var questions = data.questions;

        output = data; //questions.filter(function(q) { return q.fields.answer_type == "MultiChoice"; });
        component.setState({questions: questions});
        component.setState({selectedQuestion: questions[0]});
    }, dataType="json");
    // var questions = [ {id: 10, responses: [{value:"yes", text:"yes"}, {value:"no", text:"no"}]},
    //                     {id: 20, responses: [{value:"yes", text:"yes"}, {value:"no", text:"no"}]},
    //                     {id: 30, responses: [{value:"yes", text:"yes"}, {value:"no", text:"no"}]}];  //make get request
    // component.setState({questions: questions});
};
