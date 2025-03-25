$(document).ready(function(){
  $("#phone").mask("+38 (999) 999 99 99");
});

document.getElementById('input-form').addEventListener('submit', event => {
    event.preventDefault();

    const emailValue = document.getElementById('email').value;
    const phoneValue = document.getElementById('phone').value;
    const ticketType = document.querySelector('input[name="ticket_type"]:checked');
    const userSurnameValue = document.getElementById('surname').value;
    const userNameValue = document.getElementById('name').value;

    if (!validateEmail(emailValue)) {
        alert("Неправильно введена пошта");
    }
    else if (!validatePhone(phoneValue)) {
        alert("Неправильно введений номер телефону")
    }
    else if (!ticketType) {
        alert("Лише один квиток")
    }
    else if (!validateFullName(userNameValue, userSurnameValue)) {
        alert("Заповніть поле імені та прізвища")
    }
    else {
        fetch("/order", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: userNameValue,
                surname: userSurnameValue,
                email: emailValue,
                phone: phoneValue,
                ticket_type: ticketType.value,
            })
        })
        .then(res => res.json())
        .then(data => {
            window.location.href = data;
        })
        .catch(err => console.log(err));
    }
})

function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}
function validatePhone(phone) {
    const phonePattern = /^\+?\d{1,3}[\s\-]?\(?\d{2,3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$/;
    return phonePattern.test(phone);
}

function validateFullName(name, surname) {
    return name.trim().length > 0 && surname.trim().length > 0;
}

