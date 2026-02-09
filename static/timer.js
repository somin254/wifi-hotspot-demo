function updateTimer() {
    fetch("/time-left")
        .then(response => response.json())
        .then(data => {
            const timer = document.getElementById("timer");

            if (!timer) return;

            if (data.seconds <= 0) {
                timer.innerText = "Session expired";
                return;
            }

            timer.innerText = data.seconds + " seconds remaining";
        });
}

updateTimer();
setInterval(updateTimer, 1000);

