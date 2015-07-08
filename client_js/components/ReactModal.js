var React = require('react');

var Modal = React.createClass({
    toggle: function () {
        $("#" + this.props.modalId + "Modal").modal('toggle');
    },
    componentWillMount: function() {
        var modal = this;
        dispatcher.register(function(payload) {
            if (payload.name === "MODAL_TOGGLE" && payload.data === modal.props.modalId) {
                modal.toggle();
            }
        })
    },
   render: function() {
       var modal_name = this.props.modalId + "Modal";
       var modal_label_name = modal_name + "Label";
       return (
           <div className="modal fade" id={modal_name} tabIndex="-1" role="dialog"
                 aria-labelledby={modal_label_name}>
                <div className="modal-dialog" role="document">
                    <div className="modal-content">
                        <div className="modal-header">
                            <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span
                                aria-hidden="true">&times;</span></button>
                            <h4 className="modal-title" id={modal_label_name}>{this.props.title}</h4>
                        </div>
                        <div className="modal-body">
                            {this.props.children}
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
                            <button type="button" className="btn btn-primary" onClick={this.props.btnAction}>{this.props.btnText}</button>
                        </div>
                    </div>
                </div>
            </div>
       );
   }
});

module.exports = Modal;