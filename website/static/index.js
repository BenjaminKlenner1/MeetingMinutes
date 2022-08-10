function deleteMinute(minuteId) {
    console.log("test")
    fetch('/delete-minute', {
        method: 'POST',
        body: JSON.stringify({minuteId: minuteId})
    }).then((_res) => {
        window.location.href = "/"
    }); 
}