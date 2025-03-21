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




