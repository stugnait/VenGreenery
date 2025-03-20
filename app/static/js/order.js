document.getElementById('input-form').addEventListener('submit', event => {
    const emailValue = document.getElementById('user-email').value;
    const phoneValue = document.getElementById('user-phone').value;
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const phonePattern = /^\+?[1-9]\d{1,2}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$/;

    if (emailPattern.test(emailValue) && phonePattern.test(phoneValue)) {
        document.getElementById('invalid-input').style.display = 'none';
    } else {
        let hint = document.getElementById('invalid-input');
        hint.textContent = "Неправильно введена пошта";
        hint.style.display = 'block';
        event.preventDefault();
    }
    event.preventDefault();
})

function domReady(fn) {
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



