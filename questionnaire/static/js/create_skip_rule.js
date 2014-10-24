/** @jsx React.DOM */

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
        var options = this.props.questions.map(function(q) {
            return (
                <option value={q.id}>{q.id}</option>
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
    dummyFunction: function(a) { return; },
    selectQuestion: function(question) {
        var selectedQuestion = this.state.questions.filter(function(q) {
            return q.id == question;
        })[0];
        this.setState({questions:this.state.questions, selectedQuestion: selectedQuestion});
    },
    getInitialState: function() {
        return {questions:[ {id: 10, responses: [{value:"yes", text:"yes"}, {value:"no", text:"no"}]},
                            {id: 20, responses: [{value:"yes", text:"yes"}, {value:"no", text:"no"}]},
                            {id: 30, responses: [{value:"yes", text:"yes"}, {value:"no", text:"no"}]}],
               selectedQuestion: {id: null, responses: []}};
    },
    render: function() {
        var selectedQuestion = this.state.selectedQuestion;
        var qs = this.state.questions.filter(function(q) { return q != selectedQuestion; });
        return (
            <div>
                <Question questions={this.state.questions} selectQuestion={this.selectQuestion} label="Select Root Question"/>
                <Responses responses={this.state.selectedQuestion.responses} />
                <Question questions={qs} selectQuestion={this.dummyFunction} label="Select Question to Skip"/>
            </div>
        );
    }
});

React.renderComponent(<AddSkipRule />, document.getElementById('id_create-skip-rule'));
