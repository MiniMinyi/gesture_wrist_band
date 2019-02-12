// 640 480

let canvas = document.getElementById("robot-face");
canvas.width = $("#robot-canvas").width();
let ctx = canvas.getContext("2d");
let blink_status = false;
let timer = Math.random() * 2000;


const left_eyebow_center_position_r = [canvas.width / 2 - 80, 50];
const right_eyebow_center_position_r = [canvas.width / 2 + 80, 50];
let left_eyebow_position_r = left_eyebow_center_position_r;
let right_eyebow_position_r = right_eyebow_center_position_r;


let draw = function () {
    ctx.strokeStyle = "#FFFFFF";
    ctx.lineWidth = 5;
    if (!blink_status) {
        ctx.beginPath();
        ctx.arc(left_eyebow_center_position_r[0], left_eyebow_center_position_r[1], 44, 0, 2 * Math.PI);
        ctx.stroke();

        ctx.beginPath();
        ctx.fillStyle = "#FFFFFF";
        ctx.arc(left_eyebow_position_r[0], left_eyebow_position_r[1], 20, 0, 2 * Math.PI);
        ctx.fill();


        ctx.beginPath();
        ctx.arc(right_eyebow_center_position_r[0], right_eyebow_center_position_r[1], 44, 0, 2 * Math.PI);
        ctx.stroke();

        ctx.beginPath();
        ctx.fillStyle = "#FFFFFF";
        ctx.arc(right_eyebow_position_r[0], right_eyebow_position_r[1], 20, 0, 2 * Math.PI);
        ctx.fill();
    } else {
        ctx.beginPath();
        ctx.moveTo(left_eyebow_center_position_r[0] - 44, left_eyebow_center_position_r[1]);
        ctx.lineTo(left_eyebow_center_position_r[0] + 44, left_eyebow_center_position_r[1]);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(right_eyebow_center_position_r[0] - 44, right_eyebow_center_position_r[1]);
        ctx.lineTo(right_eyebow_center_position_r[0] + 44, right_eyebow_center_position_r[1]);
        ctx.stroke();
    }

    ctx.beginPath();
    ctx.arc(canvas.width / 2, 125, 22, 0, 2 * Math.PI);
    ctx.stroke();
};

const redraw = function () {
    ctx.clearRect(0, 0, canvas.clientWidth, canvas.clientHeight);
    draw();
};

const reset_blink_timer = function () {
    timer = Math.random() * 2000;
    setTimeout(blink, timer);
};

const blink = function () {
    blink_status = !blink_status;
    redraw();
    reset_blink_timer();
    // console.log(blink_status);

};

reset_blink_timer();
let msg = null;


