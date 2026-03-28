const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirm_password');
const form = document.querySelector('form');
const passwordError = document.getElementById('password-error');

passwordError.classList.add('display-none');

confirmPassword.addEventListener('focusout', (e) => {
    if (password.value !== confirmPassword.value) {
        passwordError.classList.remove('display-none');
        confirmPassword.classList.add('password-mal');
        passwordError.textContent = 'Las contraseñas no coinciden';
    } else {
        passwordError.classList.remove('password-mal');
        passwordError.textContent = '';
    }
});

confirmPassword.addEventListener('keyup', (e) => {
    if (password.value === confirmPassword.value) {
        confirmPassword.classList.remove('password-mal');
        passwordError.textContent = '';
        passwordError.classList.add('display-none');
    }
});