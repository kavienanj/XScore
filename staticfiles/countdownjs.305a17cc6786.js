var Url = document.getElementById("time").getAttribute("content");
var endTime = document.getElementById("end_time_hidden").innerHTML;
var countDownTime = new Date(endTime).getTime();
var type = document.getElementsByClassName("card-header")[0];
var clock = setInterval(function() {
        var now = new Date().getTime();
        var distance = countDownTime - now;
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        document.getElementById("time_hours").innerHTML = hours;
        document.getElementById("time_minutes").innerHTML = minutes;
        document.getElementById("time_seconds").innerHTML = seconds;
        if (distance <= 1800000) {
            if (distance <= 300000) {
                document.getElementById("time_span").className = "btn btn-danger";
            } else {
                document.getElementById("time_span").className = "btn btn-warning";
            };
        };
        if (distance <= 0) {
            clearInterval(clock);
            document.getElementById("time").innerHTML = "<button class='btn btn-outline-dark btn-lg' disabled><span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span> Finishing Exam...</button>";
            window.onbeforeunload == null;
            if (type.innerHTML == "MCQ Questions") {
                document.getElementById("mcq_paper").submit();
            } else {
                setTimeout(function(){
                    window.location.replace(window.location);
                }, 6000);
            };
            return;
        };
    }, 1000);
