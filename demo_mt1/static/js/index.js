let video_panel = document.getElementById("video-panel");
let halted = true;


function reload_img() {
    if (!halted) {
        video_panel.src = "http://10.0.0.73/html/cam_pic.php?time=" + new Date().getTime() + "&pDelay=40000";
        setTimeout("reload_img()", 200);
    }
}

function start_capturing() {
    $("#video-canvas").removeClass('hidden');
    reload_img();
}

function stop_capturing() {
    $("#video-canvas").addClass('hidden');
    $("#camera-canvas").height(51);
}


function start_or_stop_capturing() {
    if (halted) {
        $("#camera-canvas").height(500);
        $("#video-btn").html("Stop Capturing");
        halted = false;
        setTimeout("start_capturing()", 1000);
    } else {
        stop_capturing();
        $("#video-btn").html("Start Capturing");
        halted = true;
    }
}
