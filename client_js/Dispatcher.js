var Dispatcher = function() {
    this._callbacks = [];
};

Dispatcher.prototype.register = function(callback) {
    this._callbacks.push(callback);
    console.log("Registered: " + callback);
};

Dispatcher.prototype.dispatch = function (payload) {
    this._callbacks.forEach(function(callback) {
       callback(payload);
    });
    console.log("Dispatched: " + payload.name);
};

module.exports = Dispatcher;
