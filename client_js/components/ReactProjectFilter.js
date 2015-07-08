var React = require('react');

module.exports = React.createClass({
    render: function() {
        return (
            <div style={{"display": "inline"}}>
                <label>Filter project name:</label>&nbsp;&nbsp;<input type="text" id="project-filter-name" className="form-control"/> <button className="btn">Filter</button>
            </div>
        )
    }
})