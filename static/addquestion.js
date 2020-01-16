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