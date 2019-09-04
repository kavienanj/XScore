document.getElementById("mcq_paper").onsubmit = function stop_msg () {
    window.onbeforeunload = null;
};
var signal = document.getElementsByName("status")[0].innerHTML;
if (signal == "Started") {
    window.onbeforeunload = function() {
        return "Do you want to leave this page?";
    };
} else {
    window.onbeforeunload = null
};