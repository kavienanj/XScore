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
function delete_q (object, q) {
 var q_url = object.href;
 var i=1;
 var h=550;
 var btn = document.getElementsByName("n" + q.id.toString())[0];
 var opacity = setInterval(function () {
    i-=0.1;
    h-=50;
    q.style.cssText = q.style.cssText + ";opacity:" + i.toString() + ";height:" + h.toString() + "px;";
    btn.style.cssText = btn.style.cssText + "opacity:" + i.toString() + ";";
    if (i<=0) {
     clearInterval(opacity);
     document.getElementById("addedqnum").innerHTML = (Number(document.getElementById("addedqnum").innerHTML)-1).toString();
     $.ajax({
        url: q_url,
        success: function(result){
            var div = document.getElementById("alerts");
            if (result == "success") {
                div.innerHTML = 'MCQ Question ' + q.id.toString().slice(1) + ' is removed successfully!';
                q.remove();
                btn.remove();
            }
        }
     });
    };
 }, 100);
}