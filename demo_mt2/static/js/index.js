var clock_for_capturing = null;
var capturing_url_1 = "http://10.19.218.9/html/cam_pic.php";
var capturing_url_2 = "http://10.18.169.208/html/cam_pic.php";
var video_panel_1 = document.getElementById("video-panel-1");
var video_panel_2 = document.getElementById("video-panel-2");
var start_flag = false;

var gesture_description_list = [
    'Two fingers click',
    'One finger click',
    'Two fingers double click',
    'One finger double click',
    'Zoom out',
    'Open hand',
    'Close hand',
    'Zoom in',
    'Shaking hand',
];

$(document).ready(function () {
});


function start_stop() {
    start_flag = !start_flag;
    if (start_flag) {
        $("#start-stop-btn").html("Stop");
        $("#start-stop-btn").removeClass("btn-success");
        $("#start-stop-btn").addClass("btn-warning");
        clock_for_capturing = setInterval(capture_data, 100);

    } else {
        $("#start-stop-btn").html("Start");
        $("#start-stop-btn").removeClass("btn-warning");
        $("#start-stop-btn").addClass("btn-success");
        clearInterval(clock_for_capturing);
        $(".value-column").html("-");
        $("#label-result").html();

    }

}

function hexToBase64(str) {
    return btoa(String.fromCharCode.apply(null, str.replace(/\r|\n/g, "").replace(/([\da-fA-F]{2}) ?/g, "0x$1 ").replace(/ +$/, "").split(" ")));
}

function get_timestamp() {
    // console.log(Date.now());
    return Date.now();
}

var image_data = null;


function capture_data() {
    // console.log("capturing");
    var now = get_timestamp();
    video_panel_1.src = "/get_image_1/time=" + now;
    video_panel_2.src = "/get_image_2/time=" + now;
    $.get("/predict", function (data) {
        var status = data.return_code;
        // console.log(data);
        if (status === -2) {
            $("#label-result").html("Initializing...")
        } else if (status === 0) {
            var rets = data.ret;
            var max_value = 0;
            var best_gesture = null;
            for (var i = 0; i < rets.length; i++) {
                var value = rets[i];
                if (value > max_value) {
                    max_value = value;
                    best_gesture = i;
                }
                // console.log(value);
                // console.log("#" + i + "v");
                $("#" + i + "v").html(value.toString())
            }
            $("#label-result").html(gesture_description_list[best_gesture]);
        } else {
            $("#label-result").html("Server Error")
        }
    })

    // clearInterval(clock_for_capturing);
}


