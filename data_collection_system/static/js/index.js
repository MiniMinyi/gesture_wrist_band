// var gesture_img_list = [
//     'ezgif.com-gif-maker-13.gif',
//     'ezgif.com-gif-maker-12.gif',
//     'ezgif.com-gif-maker-10.gif',
//     'ezgif.com-gif-maker-11.gif',
//     'ezgif.com-gif-maker-3.gif',
//     'ezgif.com-gif-maker-2.gif',
//     'ezgif.com-gif-maker-6.gif',
//     'ezgif.com-gif-maker.gif',
//     'ezgif.com-gif-maker-7.gif',
//     'ezgif.com-gif-maker-5.gif',
//     'ezgif.com-gif-maker-4.gif',
//     'ezgif.com-gif-maker-9.gif',
//     'ezgif.com-gif-maker-8.gif',
//     'ezgif.com-gif-maker-15.gif',
//     'ezgif.com-gif-maker-14.gif',
//     'ezgif.com-gif-maker-16.gif',
//     'ezgif.com-gif-maker-17.gif',
//     'ezgif.com-gif-maker-20.gif',
//     'ezgif.com-gif-maker-21.gif',
//     'ezgif.com-gif-maker-22.gif',
//     'ezgif.com-gif-maker-19.gif',
//     'ezgif.com-gif-maker-18.gif',
//     'shaking hand.gif',
//     '1.png',
//     '2.png',
//     '3.png',
//     '4.png',
//     '5.png',
//     '6.png'];



var gesture_img_list = [
    'ezgif.com-gif-maker-11.gif',
    'ezgif.com-gif-maker-21.gif',
    '5.png',
    'cross.jpg',
    'flap_surface.jpeg',
    'shaking hand.gif',
];


var gesture_description_list = [
    'One finger click',
    'Open hand',
    'Raise your thumb',
    'Draw a cross with your index finger and middle finger',
    'flap a surface',
    'Shake your hand',
];


var gesture_times_list = [];
var current_gesture_index = -1;
var experiment_start_flag = false;
var gesture_record_flag = false;
var gesture_max_index = gesture_description_list.length - 1;
var experiment_log_list = [];
var current_log = null;
var user_name = "";
var timer = null;
var max_times_per_gesture = 20;
var gesture_times = 0;
var experiment_start_type = 0;
var gesture_sum = max_times_per_gesture * gesture_description_list.length;
var clock_for_capturing = null;
var capturing_url_1 = "http://192.168.5.178/html/cam_pic.php";
var capturing_url_2 = "http://192.168.5.73/html/cam_pic.php";
// var capturing_url_1 = "http://10.0.0.73/html/cam_pic.php";
// var capturing_url_2 = "http://10.0.0.224/html/cam_pic.php";
var IMU_url = "http://192.168.5.178:8888/get_IMU_data";
var video_panel_1 = document.getElementById("video-panel-1");
var video_panel_2 = document.getElementById("video-panel-2");
var gesture_times_per_gesture = 0;


console.log("max gesture index:", gesture_max_index);

$(document).ready(function () {
    $("#start-recording-btn").hide();
    $("#finish-recording-btn").hide();
    $("#restart-recording-btn").hide();
    $("#gesture-img").hide();
    $("#gesture-description").hide();
    $("#progress-panel").hide();

});

function start_experiment() {
    swal({
            title: "Are you ready to start the experiment?",
            text: "Please follow our instructions to finish this experiment.",
            type: "info",
            showCancelButton: true,
            confirmButtonColor: "#4f9add",
            confirmButtonText: "Confirm",
            cancelButtonText: "Cancel",
            closeOnConfirm: true
        },
        function () {
            if (experiment_start_flag) {
                return;
            }
            experiment_start_type = 0;
            max_times_per_gesture = 20;
            gesture_sum = max_times_per_gesture * gesture_description_list.length;
            init_gesture_times_list();
            console.log("max_times_per_gesture", max_times_per_gesture);
            user_name = $("#user-name-input").val();
            $("#user-name-input").val("");
            console.log("user name:", user_name);
            experiment_log_list = [];
            experiment_start_flag = true;
            $("#start-recording-btn").show();
            $("#start-experiment-btn").hide();
            $("#practice-experiment-btn").hide();
            $("#gesture-img").show();
            $("#start-img").hide();
            $("#gesture-description").show();
            $("#start-description").hide();
            $("#progress-panel").show();
            clock_for_capturing = setInterval(capture_data, 100);
            update_gesture();
        });

}

function practice_experiment() {
    swal({
            title: "Are you ready to start the warm-up?",
            text: "Please follow our instructions to finish this warm-up.",
            type: "info",
            showCancelButton: true,
            confirmButtonColor: "#4f9add",
            confirmButtonText: "Confirm",
            cancelButtonText: "Cancel",
            closeOnConfirm: true
        },
        function () {
            if (experiment_start_flag) {
                return;
            }
            experiment_start_type = 1;
            max_times_per_gesture = 1;
            gesture_sum = max_times_per_gesture * gesture_description_list.length;
            console.log("max_times_per_gesture", max_times_per_gesture);
            init_gesture_times_list();
            user_name = $("#user-name-input").val();
            $("#user-name-input").val("");
            console.log("user name:", user_name);
            experiment_log_list = [];
            experiment_start_flag = true;
            $("#start-recording-btn").show();
            $("#start-experiment-btn").hide();
            $("#practice-experiment-btn").hide();
            $("#gesture-img").show();
            $("#start-img").hide();
            $("#gesture-description").show();
            $("#start-description").hide();
            $("#progress-panel").show();
            clock_for_capturing = setInterval(capture_data, 100);

            update_gesture();
        });

}

function stop_experiment(flag) {
    if (flag === 0) {
        swal({
                title: "Are you sure to stop the experiment?",
                text: "The experiment data would be clear.",
                type: "info",
                showCancelButton: true,
                confirmButtonColor: "#4f9add",
                confirmButtonText: "Confirm",
                cancelButtonText: "Cancel",
                closeOnConfirm: true
            },
            function () {
                confirm_stop_experiment();

            });
    } else {
        swal({
            title: "You have finished the experiment.",
            text: "Thank you for your contributions",
            type: "info",
            confirmButtonColor: "#4f9add",
            confirmButtonText: "Yes",
            closeOnConfirm: true
        });
        confirm_stop_experiment();
    }
}

function confirm_stop_experiment() {
    if (!experiment_start_flag) {
        return;
    }
    experiment_start_flag = false;
    gesture_record_flag = false;
    clearInterval(clock_for_capturing);
    $("#start-recording-btn").hide();
    $("#finish-recording-btn").hide();
    $("#restart-recording-btn").hide();
    $("#start-experiment-btn").show();
    $("#practice-experiment-btn").show();
    $("#gesture-img").hide();
    $("#start-img").show();
    $("#gesture-description").hide();
    $("#start-description").show();
    $("#progress-panel").hide();
    if (experiment_start_type === 0)
        download_logs();
    experiment_log_list = [];
}

function init_gesture_times_list() {
    gesture_times_list = [];
    current_log = null;
    for (var i = 0; i <= gesture_max_index; i++)
        gesture_times_list.push(0);
    gesture_times = 0;
    gesture_times_per_gesture = 10000;
}

function download_logs() {
    var text = "gesture_index, start_time, finish_time\n";
    for (var i = 0; i < experiment_log_list.length; i++) {
        var log = experiment_log_list[i];
        console.log(log);
        text += log["gesture_index"] + ", " + log["start_time"] + ", " + log["finish_time"] + "\n";
    }
    saveAs(
        new Blob(
            [text]
            , {type: "text/plain;charset=" + 'utf-8'}
        )
        , user_name + "_log.csv"
    );

}


function get_next_gesture() {
    if (gesture_times >= gesture_sum) {
        return -1;
    }
    var width = gesture_times * 100 / gesture_sum;
    $("#progress-bar").attr("style", "width: " + width + "%");
    gesture_times += 1;
    if (gesture_times_per_gesture >= max_times_per_gesture) {
        var gesture_index = Math.floor(Math.random() * (gesture_max_index + 1));
        while (gesture_times_list[gesture_index] >= max_times_per_gesture) {
            gesture_index = Math.floor(Math.random() * (gesture_max_index + 1));
        }
        gesture_times_list[gesture_index] += 1;
        gesture_times_per_gesture = 1;
        $("body").css("background", "#ddffba");
        return gesture_index;
    } else {
        gesture_times_list[current_gesture_index] += 1;
        gesture_times_per_gesture += 1;
        return current_gesture_index;
    }
}


function capture_data() {
    // console.log("capturing");
    var now = get_timestamp();
    video_panel_1.src = capturing_url_1 + "?time=" + now + "&pDelay=40000";
    video_panel_2.src = capturing_url_2 + "?time=" + now + "&pDelay=40000";

    $.get(
        IMU_url + "/" + now,
        function (data) {
            // console.log(data);
        }
    )
    // $.get(
    //     capturing_url_2 + "?time=" + get_timestamp() + "&pDelay=40000",
    //     function (data) {
    //         // console.log(data);
    //     }
    // )
}

function start_recording() {
    if (!experiment_start_flag || gesture_record_flag)
        return -1;
    console.log("start recording");
    $("#start-recording-btn").hide();
    $("#finish-recording-btn").show();
    $("#restart-recording-btn").show();
    gesture_record_flag = true;
    current_log["start_time"] = get_timestamp();
    $("body").css("background", "#ffa5a5");
}


function finish_recording() {
    if (!experiment_start_flag || !gesture_record_flag)
        return -1;
    console.log("finish recording");
    console.log("-----------------");
    $("#start-recording-btn").show();
    $("#finish-recording-btn").hide();
    $("#restart-recording-btn").hide();
    gesture_record_flag = false;
    // clearInterval(clock_for_capturing);
    current_log["finish_time"] = get_timestamp();
    $("body").css("background", "#f3f3f4");
    update_gesture();
}

function restart_recording() {
    if (!experiment_start_flag || !gesture_record_flag)
        return -1;
    console.log("restart recording");
    gesture_record_flag = false;
    // clearInterval(clock_for_capturing);
    $("#start-recording-btn").show();
    $("#finish-recording-btn").hide();
    $("#restart-recording-btn").hide();
    $("body").css("background", "#f3f3f4");


}


function get_timestamp() {
    // console.log(Date.now());
    return Date.now();
}


function update_gesture() {
    if (current_log !== null)
        experiment_log_list.push(current_log);
    current_log = {};
    current_gesture_index = get_next_gesture();
    if (current_gesture_index === -1) {
        stop_experiment(1);
        return;
    }
    $("#collapse-btn-1").click();
    setTimeout(next_update_gesture, 400);
}

function next_update_gesture() {
    $("#collapse-btn-1").click();
    console.log("gesture index", current_gesture_index);
    $("#gesture-img").attr("src", "img/" + gesture_img_list[current_gesture_index]);
    $("#gesture-description").html(gesture_description_list[current_gesture_index] + "</br>");
    current_log["gesture_index"] = current_gesture_index;

}

$(document).keypress(function (e) {
    if (!experiment_start_flag)
        return;
    // console.log(e.which);
    var key = e.which;
    if (key === 32) {
        if (gesture_record_flag) {
            finish_recording();
        } else {
            start_recording();
        }
    } else if (key === 113) {
        stop_experiment(0);
    } else if (key === 114) {
        restart_recording();
    }
});