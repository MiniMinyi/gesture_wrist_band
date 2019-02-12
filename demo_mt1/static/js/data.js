let state = 0;


let cameraInterval = null;
let config = {video: {width: 640/*320-640-1280*/}};
let frame_data = null;
const owner_color = "#00FF00";
const strange_color = "#FF0000";
const face_canvas = document.getElementById("face-canvas");
const face_ctx = face_canvas.getContext("2d");
face_ctx.font = "30px Verdana";
let owner_flag = false;


let recognition = null;
const grammar_state_2 = "#JSGF V1.0; grammar emar; public <YN> = yes | no;";
const grammar_state_3 = "#JSGF V1.0; grammar emar; public <YN> = abdominals | abductors | forearm | neck;";
const grammar_state_4 = "#JSGF V1.0; grammar emar; public <YN> = restart | change | stop;";
const exercise_types = {
    'abdominals': [0, 'abdominals', `<iframe id="tutorial-frame" width="700" height="400" 
                            src="https://www.youtube.com/embed/HJV2MNzRieI?&autoplay=1&start=23&controls=0&end=46&showinfo=0&rel=0"
                            frameborder="0"
                            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen></iframe>`, 23000],
    'abductors': [1, 'abductors', `<iframe id="tutorial-frame" width="700" height="400"
                            src="https://www.youtube.com/embed/GmD77fBsLHw?&autoplay=1&start=174&controls=0&end=240&showinfo=0&rel=0"
                            frameborder="0"
                            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen></iframe>`, 66000],
    'forearm': [2, 'forearm', `<iframe id="tutorial-frame" width="700" height="400"
                            src="https://www.youtube.com/embed/nqvZ7z3vS30?&autoplay=1&start=27&controls=0&end=117&showinfo=0&rel=0"
                            frameborder="0"
                            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen></iframe>`, 90000],
    'neck': [3, 'neck', `<iframe id="tutorial-frame" width="700" height="400"
                            src="https://www.youtube.com/embed/YPiqpLtQbvc?&autoplay=1&start=16&controls=0&end=58&showinfo=0&rel=0"
                            frameborder="0"
                            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen></iframe>`, 42000],
};
const orders = {'restart': 0, 'change': 1, 'stop': 2};



