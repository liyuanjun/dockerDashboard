/**
 * Created by king-aric-ubuntu14.04 on 16-7-29.
 */


/**
 * variable_win.print(variable_win.uri())
 */
var variable_win = {  //windows global variable
    url: window.location.href,
    port: window.location.port,
    hostname: window.location.hostname,
    host: window.location.host,
    protocol:window.location.protocol,
    _index: function () {
        return variable_win.url.indexOf('?') == -1 ?
            variable_win.url.length :
            variable_win.url.indexOf('?')
    },
    uri: function () {
        return variable_win.url.substring(0, this._index())
    },
    param: function () {
        var result = {}
        var params = window.location.search
        if (!params)return result
        var array = (params.substring(1, params.length)).split('&')
        for (var i = 0; i < array.length; i++) {
            if (array[i].split('=').length != 2 ? false : true) {
                result[array[i].split('=')[0]] = array[i].split('=')[1]
            }
        }
        return result
    },
    print: function (e) {
        console.log(e)
    }

}

/**
 var js=json_utils.object.init();
 js.put('id',1)
 console.log(js.data)
 */
 var json_utils = {
    object: {
        data: undefined,
        init: function () {
            json_utils.object.data = {}
            return this;
        },
        put: function (key, value) {
            json_utils.object.data[key] = value;
        },
        remove: function (key) {
            delete json_utils.object.data[key]
        },
        get:function (key) {
            return json_utils.object.data[key]
        }
    }


}