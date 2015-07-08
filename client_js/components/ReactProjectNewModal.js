var React = require('react');

var Modal = require('./ReactModal');

var ProjectNewModal = React.createClass({
    post: function (event) {
        var name = $("#projectNew-name").val();
        var url = $("#projectNew-url").val();

        $.post("/projects/", {name: name, url: url});
        dispatcher.dispatch({name: 'MODAL_TOGGLE', data: 'projectNew'});
        dispatcher.dispatch({name: "PROJECTS_UPDATE_START"});
    },
    render: function () {
        return (
            <Modal modalId="projectNew" title="New Project" btnAction={this.post} btnText="Create">
                <table>
                    <tr>
                        <td>Name:&nbsp;&nbsp;</td>
                        <td><input id="projectNew-name" />&nbsp;&nbsp;</td>
                    </tr>
                    <tr>
                        <td>Url:&nbsp;&nbsp;</td>
                        <td><input id="projectNew-url" />&nbsp;&nbsp;</td>
                    </tr>
                </table>
            </Modal>
        )
    }
});

module.exports = ProjectNewModal;
