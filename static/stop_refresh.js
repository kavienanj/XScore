var signal = document.getElementsByName("status")[0].innerHTML;
if (signal == "Started") {
    window.onbeforeunload = function() {
        return "Do you want to leave this page?";
    };
} else {
    window.onbeforeunload = null
};