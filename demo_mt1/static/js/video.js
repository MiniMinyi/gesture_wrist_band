let iframe_html = "";
let play_time = 0;

function start_tutorial(signal) {
    iframe_html = exercise_types[signal][2];
    $("#tutorial-panel").html(iframe_html);
    $("#camera-canvas").width(1460);
    play_time = exercise_types[signal][3];
    setTimeout(show_tutorial, 1000);
}

function show_tutorial() {
    $("#tutorial-panel").show();
    set_face_canvas_position();
    setTimeout(finish_tutorial, play_time);
}

function finish_tutorial() {
    if (state === 4) {
        state_change(0);
    }
}

function delete_tutorial() {
    $("#tutorial-panel").html("");
    $("#camera-canvas").width(700);
    $("#tutorial-panel").hide();
    set_face_canvas_position();
}

function restart_tutorial() {
    $("#tutorial-panel").html(iframe_html);
    setTimeout(finish_tutorial, play_time);

}