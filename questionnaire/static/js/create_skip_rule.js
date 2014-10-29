/** @jsx React.DOM */
var skipRules = skipRules || {};
skipRules.subsection = "";
skipRules.isMultichoiceQuestion = function(q) { return q.fields.answer_type == "MultiChoice"; }

var Responses = React.createClass({
    render: function() {
        var divStyle = {
            paddingLeft: '10px',
            paddingRight: '10px'
        };

        var options = this.props.responses.map(function(r) {
            return (
                <label className="pull-right" style={divStyle}><input type="radio" name="responses" value={r.pk} />{r.fields.text}</label>
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
                <select className="pull-right" name="skip-question" id="root-question">
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
        this.props.selectQuestion(question);
    },
    render: function() {
        var options = this.props.questions
                .filter(skipRules.isMultichoiceQuestion)
                .map(function(q) {
            return (
                <option value={q.pk}>{q.fields.text}</option>
            );
        });
        var responses = this.props.selectedQuestion.options; 
        return (
            <div>
                <label for="root-question">{this.props.label}</label>
                <select className="pull-right" name="root-question" id="root-question" onChange={this.updateSelectedQuestion} value={this.state.selectedQuestion.pk}>
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
            subsectionId: -1,
            selectedQuestion: {},
            questions: []};
    },

    render: function() {
        var selectedQuestion = this.state.selectedQuestion;
        var qs = this.state.questions.filter(function(q) { return q != selectedQuestion; });
        if (this.state.questions.filter(function(q) { return q.fields.answer_type == "MultiChoice"; }).length > 0) {
            $("#save-skip-rule-button").show();
            return (
                <div>
                    <input name="subsection-id" type="hidden" value={this.state.subsectionId} />
                    <Question questions={this.state.questions} selectQuestion={this.selectQuestion} label="Select Root Question" selectedQuestion={this.state.selectedQuestion}/>
                    <AllQuestions questions={qs} label="Select Question to Skip"/>
                </div>
            );
        } else {
            $("#save-skip-rule-button").hide();     
            return (<div>There are no Multiple Choice questions to create skip rules for</div>);
        }
    }
});

var component = React.renderComponent(<AddSkipRule />, document.getElementById('id_create-skip-rule'));

skipRules.updateSubsection = function(subsectionId) {
    skipRules.subsection = subsectionId;
    $.get( "/questionnaire/subsection/" + subsectionId + "/questions/", function( data ) {
        var questions = data.questions;
        component.setState({subsectionId: subsectionId})
        component.setState({questions: questions});
        component.setState({selectedQuestion: questions.filter(function(q) { return q.fields.answer_type == "MultiChoice"; })[0]});
    }, dataType="json");
};
