$(document).ready(function() {
    $('#classify-form').submit(function(e) {
        e.preventDefault()
        clientConnect($(this));
        $('#submit-button').attr('disabled', 'disabled')
    });
});

function clientConnect(formElement) {
    var clientID = uuidv4();
    var data = getFormData(formElement);
    var socket = io.connect('http://' + document.domain + ':' + location.port +
        '/classify?clientID=' + clientID,  {'forceNew': true});

    socket.on('connect', function(){
        console.log("connected");

        // temp values
        data.follower_limit = 10
        data.media_per_follower_limit = 20
        data.comments_per_media_limit = 250

        socket.emit('compute', clientID, data.algorithm, data.username, data.follower_limit,
            data.media_per_follower_limit, function(){
            console.log("Requested computation using " + data.algorithm +
                " algorithm as " + clientID);
        });

        resetProgress();
    })

    socket.on(clientID, function(msg) {
        console.log("[" + clientID + "] " + "Progress: " + msg.progress)

        if(msg.progress < 100){
            $('.progress-bar')
                .css('width', msg.progress + '%')
                .attr('aria-valuenow', msg.progress);
        }else{
            $('#progress-bar').hide();
            $('.progress-bar')
                .css('width', '0%')
                .attr('aria-valuenow', 0);
            $('#submit-button').removeAttr('disabled');
            $('#result').collapse('show');
            socket.disconnect();
        }
    });
}

function resetProgress() {
    $('#progress-bar').show();
    $('.progress-bar')
        .css('width', '0%')
        .attr('aria-valuenow', 0);
    $('#result').collapse('hide');
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
