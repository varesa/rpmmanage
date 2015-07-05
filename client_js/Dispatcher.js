var Dispatcher = function() {
    this._callbacks = [];
};

Dispatcher.prototype.register = function(callback) {
    this._callbacks.push(callback);
};

Dispatcher.prototype.dispatch = function (payload) {
    this._callbacks.forEach(function(callback) {
       callback(payload);
    });
};

module.exports = Dispatcher;
