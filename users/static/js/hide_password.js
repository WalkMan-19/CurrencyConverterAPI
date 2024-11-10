document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('togglePassword').addEventListener('click', function () {
        const passwordInput = document.getElementById('password');
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Показать' : 'Скрыть';
    });

    document.getElementById('togglePasswordRepeat').addEventListener('click', function () {
        const PasswordRepeatInput = document.getElementById('password_repeat');
        const type = PasswordRepeatInput.getAttribute('type') === 'password' ? 'text' : 'password';
        PasswordRepeatInput.setAttribute('type', type);
        this.textContent = type === 'password' ? 'Показать' : 'Скрыть';
    });
});
