let isProcessing = false;
function onScanSuccess(decodedText, decodeResult) {
    if (isProcessing) return;

    isProcessing = true;

    const notification = document.getElementById("notification");

    try {
        let data = JSON.parse(decodedText);
        if (data.id && data.name && data.surname && data.email && data.phone) {

            fetch('/verify_qr', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    qr_data: decodedText
                })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        notification.textContent = "QR-код успішно використано!";
                        notification.className = "success show";
                        setTimeout(() => {
                            notification.className = "success";
                        }, 5000);
                    } else {
                        if (data.error === "Ticket already used.") {
                            notification.textContent = "Помилка: QR-код уже використано!";
                            notification.className = "error show";
                            setTimeout(() => {
                                notification.className = "error";
                            }, 5000);
                        } else {
                            notification.textContent = "Помилка: Відбулася помилка при зчитувані.";
                            notification.className = "error show";
                            setTimeout(() => {
                                notification.className = "error";
                            }, 5000);
                        }
                    }
                })
                .catch(err => {
                    console.log(err);
                    notification.textContent = "Помилка: Система не відповідає!";
                    notification.className = "error show";
                    setTimeout(() => {
                        notification.className = "error";
                    }, 5000);
                })
                .finally(() => {
                    setTimeout(() => {
                        isProcessing = false;
                    }, 6000);
                });
        } else {
            notification.textContent = "Помилка: QR-код містить некоректні дані!";
            notification.className = "error show";
            setTimeout(() => {
                notification.className = "error";
            }, 5000);
            isProcessing = false;
        }
    } catch (e) {
        notification.textContent = "Помилка: QR-код не розпізнано!";
        notification.className = "error show";
        setTimeout(() => {
            notification.className = "error";
        }, 5000);
        isProcessing = false;
    }
}


new Html5QrcodeScanner("my-qr-reader", {fps: 5, qrbox: 300}).render(onScanSuccess);