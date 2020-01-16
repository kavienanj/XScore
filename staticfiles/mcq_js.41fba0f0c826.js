function swap_class (radio) {
    var labels = document.getElementsByName("label"+radio.name);
    var atag = document.getElementsByName("btnq"+radio.name)[0];
    console.log(atag);
    var radio;
    for(var i = 0; i < labels.length; i++){
        radio = labels[i].childNodes[1];
        if (radio.checked) {
            atag.className = "btn btn-sm btn-success"
            labels[i].className =  "d-flex align-items-center border-secondary list-group-item-success";
        } else {
            labels[i].className = "d-flex align-items-center border-secondary";
        };
    };
};
