setTimeout (function() {
    console.log("HI")
    let messages = document.getElementById("msg");
    let alert = new bootstrap.Alert(messages);
    alert.close();
    }, 7000);