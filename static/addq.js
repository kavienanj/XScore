show_value(document.getElementsByName("durationx")[0].value);
function show_value (x) {
    var hours = Math.floor( x / 60 );
    var minutes = Math.floor( x % 60 );
    document.getElementById("hours").innerHTML = hours;
    document.getElementById("minutes").innerHTML = minutes;
    if (hours.toString().length == 1) {
        hours = "0" + hours.toString();
    };
    if (minutes.toString().length == 1) {
        minutes = "0" + minutes.toString();
    };
};
