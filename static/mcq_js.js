// window.onbeforeunload = function () {return "Do you want to leave this page?";};
// document.getElementById("mcq_paper").onsubmit = function () {window.onbeforeunload = null;};
function swap_class (radio) {
    var labels = document.getElementsByName("label"+radio.name);
    var atag = document.getElementsByName("btnq"+radio.name)[0];
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
function flag_it (anchor) {
    var atag = document.getElementsByName("btnq"+anchor.name)[0];
    if (atag.childNodes.length == 1) {
        atag.innerHTML = atag.innerHTML+"<span class='pop'>!</span>";
        anchor.innerHTML = "flagged!";
    } else {
        atag.innerHTML = atag.childNodes[0].data;
        anchor.innerHTML = "flag";
    };
};