var Url = document.getElementById("time").getAttribute("content");
$.ajax({url: Url,
        type: "GET",
        dataType: 'json',
        success: function (data) {
            var countDownTime = new Date(data.over).getTime();
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
                    document.getElementById("time").innerHTML = "EXPIRED";
                    window.onbeforeunload = null;
                    window.location.replace(window.location);
                    return;
                };
            }, 1000);
        }
})
