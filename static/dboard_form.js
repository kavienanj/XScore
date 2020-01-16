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
function swap_class (radio) {
    var labels = document.getElementsByName("labels");
    var radio;
    for(var i = 0; i < labels.length; i++){
        radio = labels[i].childNodes[1];
        if (radio.checked) {
            labels[i].className =  "d-flex align-items-center border-secondary list-group-item-success";
        } else {
            labels[i].className = "d-flex align-items-center border-secondary";
        };
    };
};
