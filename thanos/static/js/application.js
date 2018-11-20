$(document).ready(function(){
    $('#classify-form').submit(function(e){
        e.preventDefault()
        clientConnect($(this));
    });
});

function clientConnect(formElement){
    var clientID = uuidv4();
    var data = getFormData(formElement);
    var socket = io.connect('http://' + document.domain + ':' + location.port +
        '/classify?clientID=' + clientID);

    socket.on('connect', function(){
        console.log("connected");

        socket.emit('compute', clientID, data.algorithm, function(){
            console.log("Requested computation using " + data.algorithm +
                " algorithm as " + clientID);
                $('#progress-bar').show();
            });
        })

        socket.on(clientID, function(msg) {
            console.log("[" + clientID + "] " + "Progress: " + msg.progress)
            if(msg.progress < 100){
                $('.progress-bar')
                    .css('width', msg.progress + '%')
                    .attr('aria-valuenow', msg.progress);
            }else{
                $('#progress-bar').hide();
                $('#result').collapse('show');
            }
    });
}

function getFormData(formElement) {
    var data = {}, inputs = formElement.serializeArray();
    $.each(inputs, function(i, o){
        data[o.name] = o.value;
    });

    return data
}

function checkProgress(clientID) {
    function worker() {
        $.get('progress/' + clientID, function(data) {
            if (progress < 100) {
                // progressBar.set_progress(progress)
                console.log("Progress: " + data)
                setTimeout(worker, 1000)
            }
        })
    }
}

function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
}
