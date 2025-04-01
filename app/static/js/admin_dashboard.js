let isProcessing = false;
const scanner = new Html5QrcodeScanner("my-qr-reader", {fps: 5, qrbox: 300});

function onScanSuccess(decodedText) {
    if (isProcessing) return;
    isProcessing = true;

    const notification = document.getElementById("notification");

    try {
        let data = JSON.parse(decodedText);
        if (data.id && data.name && data.surname && data.email && data.phone) {
            fetch('/verify_qr', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({qr_data: decodedText})
            })
                .then(res => res.json())
                .then(response => {
                    if (response.success) {
                        showTicketInfo(response.ticket);
                    } else {
                        if (response.error === "Ticket already used.") {
                            showTicketInfo(response.ticket);
                            notification.textContent = "Помилка: Квиток уже використано!";
                            notification.className = "error show";
                            setTimeout(() => notification.className = "error", 5000);
                            isProcessing = false;
                        }
                        notification.textContent = "Помилка: Неправильні дані QR коду!";
                        notification.className = "error show";
                        setTimeout(() => notification.className = "error", 5000);
                        isProcessing = false;

                    }
                })
                .catch(() => {
                    notification.textContent = "Помилка: Відбулася помилка при зчитувані.";
                    notification.className = "error show";
                    setTimeout(() => notification.className = "error", 5000);
                    isProcessing = false;
                });
        } else {
            showError("Помилка: QR-код містить некоректні дані!");
        }
    } catch (e) {
        showError("Помилка: QR-код не розпізнано!");
    }
}

function showTicketInfo(ticket) {
    console.log("Відображення модального вікна", ticket);
    scanner.clear();

    const modal = document.createElement("div");
    modal.id = "ticket-modal";
    modal.innerHTML = `
        <div class="modal-content">
            <h2>Дані квитка</h2>
            <p><b>ID:</b> ${ticket.id}</p>
            <p><b>Тип:</b> ${ticket.type === "child" ? "Дитячий" : "Дорослий"}</p>
            <p><b>Використано:</b> ${ticket.used ? "Так" : "Ні"}</p>
            <p><b>Дата створення:</b> ${ticket.create_date}</p>
            <p><b>Дата використання:</b> ${ticket.use_date || "Ще не використано"}</p>
            <p><b>Покупець:</b></p>
            <div class="credentials-wrapper">
                <div class="credentials">
                    <p>${ticket.name} ${ticket.surname}</p>
                    <p>${ticket.phone}</p>
                    <p>${ticket.email}</p>
                </div>
            </div>            
            <div class="modal-button-block">
                <button id="activate-ticket" ${ticket.used ? "disabled" : ""}>Активувати</button>
                <button id="close-modal">Закрити</button>
            </div>
            
        </div>
    `;
    modal.className = "modal";
    document.body.appendChild(modal);

    document.getElementById("close-modal").addEventListener("click", () => {
        modal.remove();
        isProcessing = false;
        scanner.render(onScanSuccess);
    });

    document.getElementById("activate-ticket").addEventListener("click", () => {
        activateTicket(ticket.id, modal);
    });
}


function activateTicket(ticketId, modal) {
    fetch('/activate_ticket', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ticket_id: ticketId})
    })
        .then(res => res.json())
        .then(response => {
            if (response.success) {
                console.log(response);
                modal.querySelector("p:nth-child(4)").innerHTML = "<strong>Використано:</strong> Так";
                modal.querySelector("p:nth-child(6)").innerHTML = `<strong>Дата використання:</strong> ${response.use_date}`;
                const activateButton = document.getElementById("activate-ticket");
                activateButton.disabled = true
            }
        });
}

function showError(message) {
    const notification = document.getElementById("notification");
    notification.textContent = message;
    notification.className = "error show";
    setTimeout(() => notification.className = "error", 5000);
    isProcessing = false;
}

scanner.render(onScanSuccess);
