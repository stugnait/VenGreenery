function domReady(fn) {
    document.getElementById('my-qr-reader').style.display = 'none';
    document.getElementById('hide-scanner-button').style.display = 'none';
    if (
        document.readyState === "complete" ||
        document.readyState === "interactive"
    ) {
        setTimeout(fn, 1000);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

domReady(function () {

    function onScanSuccess(decodeText, decodeResult) {
        alert("You Qr is : " + decodeText + decodeResult);
        console.log(decodeText);
        fetch('/verify_qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                qr_data: decodeText
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                console.log("Success!!!");
            }
            else {
                console.log("Error!!!" + data);
            }
        })  
        .catch(err => console.log(err));
    }

    let htmlscanner = new Html5QrcodeScanner(
        "my-qr-reader",
        { fps: 1, qrbos: 250 }
    );
    htmlscanner.render(onScanSuccess);
});

function showScanner() {
    document.getElementById('my-qr-reader').style.display = 'block';
    document.getElementById('show-scanner-button').style.display = 'none';
    document.getElementById('hide-scanner-button').style.display = 'block';
}
function hideScanner() {
    document.getElementById('my-qr-reader').style.display = 'none';
    document.getElementById('hide-scanner-button').style.display = 'none';
    document.getElementById('show-scanner-button').style.display = 'block';
}