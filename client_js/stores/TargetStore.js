var $ = require('jquery');
var React = require('react');

var Target = require('./Target');

var TargetStore = function() {
    this._targets = [];

    var ts = this;
    dispatcher.register(function(payload) {
        if(payload.name === "TARGETS_UPDATE_START") {
            ts.fetch();
        }
    })
};

TargetStore.prototype.fetch = function() {
    var ps = this;
    $.get("/targets", function(data) {
        console.log(data);
        var json = JSON.parse(data);
        ps._targets = [];
        for(var i = 0; i < json.length; i++) {
            ps._targets.push(new Target(json[i].name));
            console.log(json[i]);
        }
        dispatcher.dispatch({name: 'TARGETS_UPDATE_DONE'});
    });
};

TargetStore.prototype.getAll = function () {
    return this._targets;
};

module.exports = TargetStore;