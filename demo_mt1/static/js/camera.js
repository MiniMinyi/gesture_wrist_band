

function set_face_canvas_position() {
    let position = $("#video-panel").position();
    $("#face-canvas").css({top: position.top, left: position.left, position: 'absolute'});
}

/* This function checks and sets up the camera */
function startVideo() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
            .getUserMedia(config)
            .then(handleUserMediaSuccessStartVideo);
    }
    $("#video-btn").html("Stop Exercise");
    $("#camera-canvas").height(558);
    setTimeout(show_video, 1000);

}

function show_video() {
    $("#video-canvas").removeClass('hidden');
    set_face_canvas_position();
}

function stopVideo() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
            .getUserMedia(config)
            .then(handleUserMediaSuccessStopVideo);
    }
    $("#video-btn").html("Start Exercise");
    $("#video-canvas").addClass('hidden');
    $("#camera-canvas").height(51);
}

/* This function initiates the camera video */
function handleUserMediaSuccessStartVideo(stream) {
    let video = document.getElementById("myVideo");
    // video.src = window.URL.createObjectURL(stream);
    video.srcObject = stream;
    video.play();

    /* We will capture an image twice every second */
    cameraInterval = window.setInterval(captureImageFromVideo, 500);
}

function handleUserMediaSuccessStopVideo(stream) {
    let video = document.getElementById("myVideo");
    video.pause();
    // video.src = "";
    if (cameraInterval) {
        window.clearInterval(cameraInterval);
        cameraInterval = null;
    }
    document.getElementById("video-panel").getContext("2d").clearRect(0, 0, video.width, video.height);
}


/* This function captures the video */
function captureImageFromVideo() {
    let canvas = document.getElementById("video-panel");
    let context = canvas.getContext("2d");
    let video = document.getElementById("myVideo");

    canvas.setAttribute("width", video.width);
    canvas.setAttribute("height", video.height);
    context.drawImage(video, 0, 0, video.width, video.height);

    let dataObj = context.getImageData(0, 0, canvas.width, canvas.height);

    // Now data is a long, flat array containing the RGB values of each pixel
    frame_data = dataObj.data;
    $.post("/frame_operation", {data: window.btoa(frame_data)}).done(function (faces) {
        draw_faces(faces);
    });
    context.putImageData(dataObj, 0, 0);
}

function draw_faces(faces) {
    face_ctx.clearRect(0, 0, face_canvas.width, face_canvas.height);

    for (let i = 0; i < faces.length; i++) {
        const face = faces[i];
        const face_rectangle = face.face_rectangle;
        const is_owner = face.is_owner;
        if (is_owner) {
            face_ctx.strokeStyle = owner_color;
            owner_flag = true;
            check_if_started();
        } else {
            face_ctx.strokeStyle = strange_color;
        }
        face_ctx.lineWidth = 5;
        face_ctx.beginPath();
        face_ctx.rect(face_rectangle[3], face_rectangle[0], face_rectangle[1] - face_rectangle[3], face_rectangle[2] - face_rectangle[0]);
        face_ctx.stroke();
        face_ctx.lineWidth = 1;
        face_ctx.strokeText(face.emotion, face_rectangle[3], face_rectangle[0]);
    }
}

function add_owner() {
    $.post("/add_owner", {}).done(function (data) {
        console.log(data)
    });
}

function forget_owner() {
    $.post("/forget_owner", {}).done(function (data) {
        console.log(data)
    });
}