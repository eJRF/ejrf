/** @jsx React.DOM */
var skipRules = skipRules || {};
skipRules.subsection = "";

var Responses = React.createClass({
    render: function() {
        var options = this.props.responses.map(function(r) {
            return (
                <label><input type="radio" name="responses" value="{r.value}" />{r.text}</label>
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

var Question = React.createClass({
    getInitialState: function() {
        return (
            { selectOption: null }
        );
    },
    updateSelectedQuestion: function(event) {
        var e = document.getElementById("root-question");
        var v = e.options[e.selectedIndex].value;
        this.props.selectQuestion(v);
    },
    render: function() {
        var options = this.props.questions
                .filter(this.props.filterFunction)
                .map(function(q) {
            return (
                <option value={q.pk}>{q.fields.text}</option>
            );
        });
        return (
            <div>
                <label for="root-question">{this.props.label}</label>
                <select name="root-question" id="root-question" onChange={this.updateSelectedQuestion} value={this.state.selectedOption}>
                {options}
                </select>
        </div>
        );
    }
});

var AddSkipRule = React.createClass({
    dummyFunction: function(a) { return true; },
    selectQuestion: function(question) {
        var selectedQuestion = this.state.questions.filter(function(q) {
            return q.pk == question;
        })[0];
        this.setState({questions:this.state.questions, selectedQuestion: selectedQuestion});
    },
    getInitialState: function() {
        return {
            questions: [],
            selectedQuestion: {pk: null, responses: []}};
    },
    filterQuestions: function(q) { return q.fields.answer_type == "MultiChoice"; },
    render: function() {
        var selectedQuestion = this.state.selectedQuestion;
        var qs = this.state.questions;//This.questions.filter(function(q) { return q != selectedQuestion; });
        return (
            <div>
                <Question questions={this.state.questions} selectQuestion={this.selectQuestion} filterFunction={this.filterQuestions} label="Select Root Question"/>
                <Responses responses={this.state.selectedQuestion.responses} />
                <Question questions={qs} selectQuestion={this.dummyFunction} filterFunction={this.dummyFunction} label="Select Question to Skip"/>
            </div>
        );
    }
});

var component = React.renderComponent(<AddSkipRule />, document.getElementById('id_create-skip-rule'));

var output= {};
skipRules.updateSubsection = function(subsectionId) {
    skipRules.subsection = subsectionId;
    $.get( "/questionnaire/subsection/" + subsectionId + "/questions/", function( data ) {
        var questions = jQuery.parseJSON( data.questions );
        output = questions.filter(function(q) { return q.fields.answer_type == "MultiChoice"; });
        component.setState({questions: questions});
    }, dataType="json");
    // var questions = [ {id: 10, responses: [{value:"yes", text:"yes"}, {value:"no", text:"no"}]},
    //                     {id: 20, responses: [{value:"yes", text:"yes"}, {value:"no", text:"no"}]},
    //                     {id: 30, responses: [{value:"yes", text:"yes"}, {value:"no", text:"no"}]}];  //make get request
    // component.setState({questions: questions});
};
