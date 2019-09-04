var time = document.getElementById("id_duration").value;
time = time.split(":");
document.getElementById("hours").innerHTML = Number(time[0]);
document.getElementById("minutes").innerHTML = Number(time[1]);
document.getElementById("duration").value = Number(time[0]) * 60 + Number(time[1]);
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
    document.getElementById("id_duration").setAttribute('value', hours + ":" + minutes + ":00");
};