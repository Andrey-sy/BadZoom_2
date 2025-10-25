// Валидация формы на стороне клиента
function validateForm() {
    const email = document.getElementById('email');
    const firstName = document.getElementById('first_name');
    const lastName = document.getElementById('last_name');
    const password = document.getElementById('password');
    const passwordConfirm = document.getElementById('password_confirm');
    const position = document.getElementById('position');
    const errorDiv = document.getElementById('errorMessage');

    // Скрываем предыдущие ошибки
    errorDiv.style.display = 'none';
    errorDiv.textContent = '';

    // Валидация email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.value)) {
        showError('Пожалуйста, введите корректный email адрес');
        email.focus();
        return false;
    }

    // Валидация имени
    if (firstName.value.trim().length < 2) {
        showError('Имя должно содержать минимум 2 символа');
        firstName.focus();
        return false;
    }

    // Валидация фамилии
    if (lastName.value.trim().length < 2) {
        showError('Фамилия должна содержать минимум 2 символа');
        lastName.focus();
        return false;
    }

    // Валидация должности
    if (position.value.trim().length < 2) {
        showError('Должность должна содержать минимум 2 символа');
        position.focus();
        return false;
    }

    // Валидация пароля
    if (password.value.length < 6) {
        showError('Пароль должен содержать минимум 6 символов');
        password.focus();
        return false;
    }

    // Проверка совпадения паролей
    if (password.value !== passwordConfirm.value) {
        showError('Пароли не совпадают');
        passwordConfirm.focus();
        return false;
    }

    // Показываем loading state
    const submitBtn = document.querySelector('.submit-btn');
    submitBtn.textContent = 'Регистрация...';
    submitBtn.disabled = true;

    return true;
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';

    // Прокрутка к ошибке
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Автоскрытие ошибки через 5 секунд
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Real-time валидация паролей
document.addEventListener('DOMContentLoaded', function() {
    const password = document.getElementById('password');
    const passwordConfirm = document.getElementById('password_confirm');

    if (password && passwordConfirm) {
        function validatePasswords() {
            if (password.value && passwordConfirm.value) {
                if (password.value !== passwordConfirm.value) {
                    passwordConfirm.style.borderColor = 'var(--error-color)';
                } else {
                    passwordConfirm.style.borderColor = 'var(--success-color)';
                }
            }
        }

        password.addEventListener('input', validatePasswords);
        passwordConfirm.addEventListener('input', validatePasswords);
    }
});