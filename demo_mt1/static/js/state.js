function assign_state(value) {
    state = value;
    console.log("change state: ", state);
}

function reset_state() {
    assign_state(0);
    owner_flag = false;
    frame_data = null;
}

function state_change(signal) {
    switch (state) {
        case 0:
            assign_state(1);
            speak("Hello, I'm Nike Bot, your smart exercise assistant.", 'en');
            startVideo();
            break;
        case 1:
            if (signal === 1) {
                assign_state(2);
                speak("My dear master，Do you want to do some exercise?", 'en', true);
            } else {
                speak("Sorry, I only serve my master.", 'en');
            }
            break;
        case 2:
            if (signal === 1) {
                assign_state(3);
                speak("Which parts of your body you want to exercise, abdominals, abductors, forearm, or neck?", 'en', true);
            } else {
                start_or_stop_video();
            }
            break;
        case 3:
            console.log('start tutorial');
            speak("Please follow the instructions in the video.", 'en');
            assign_state(4);
            setTimeout(function () {
                start_tutorial(signal);
            }, 2000);
            break;
        case 4:
            assign_state(5);
            speak("You can say restart, change exercises, stop at any time.", 'en', true);
            break;
        case 5:
            if (signal === 0) {
                assign_state(4);
                restart_tutorial();
            } else if (signal === 1) {
                assign_state(2);
                delete_tutorial();
                state_change(1);
            } else if (signal === 2) {
                start_or_stop_video();
            }
    }
}

function check_if_started() {
    if (state === 1) {
        state_change(1);
    }
}

function start_or_stop_video() {
    if (state === 0) {
        state_change();
    } else {
        reset_state();
        speak("See you!", 'en');
        stopVideo();
        delete_tutorial();
    }
}


reset_state();