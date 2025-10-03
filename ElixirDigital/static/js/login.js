// login.js - Funcionalidades específicas para a página de login

document.addEventListener('DOMContentLoaded', function() {
    initializeLoginForm();
});

// Login Form Handling
function initializeLoginForm() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // Validação básica
            if (!username || !password) {
                showLoginError('Por favor, preencha todos os campos.');
                return;
            }
            
            try {
                const response = await fetch('/admin/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                });
                
                const result = await response.json();
                
                if (response.ok && result.success) {
                    showLoginSuccess('Login realizado com sucesso! Redirecionando...');
                    setTimeout(() => {
                        window.location.href = '/admin';
                    }, 1500);
                } else {
                    showLoginError(result.message || 'Erro ao fazer login. Verifique suas credenciais.');
                }
            } catch (error) {
                console.error('Erro:', error);
                showLoginError('Erro de conexão. Tente novamente.');
            }
        });
    }
}

// Mostrar mensagem de erro
function showLoginError(message) {
    // Remove mensagens anteriores
    const existingError = document.querySelector('.login-error');
    if (existingError) {
        existingError.remove();
    }
    
    const existingSuccess = document.querySelector('.login-success');
    if (existingSuccess) {
        existingSuccess.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'login-error';
    errorDiv.innerHTML = `
        <div class="error-content">
            <i class="fas fa-exclamation-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.insertBefore(errorDiv, loginForm.firstChild);
    }
}

// Mostrar mensagem de sucesso
function showLoginSuccess(message) {
    // Remove mensagens anteriores
    const existingError = document.querySelector('.login-error');
    if (existingError) {
        existingError.remove();
    }
    
    const existingSuccess = document.querySelector('.login-success');
    if (existingSuccess) {
        existingSuccess.remove();
    }
    
    const successDiv = document.createElement('div');
    successDiv.className = 'login-success';
    successDiv.innerHTML = `
        <div class="success-content">
            <i class="fas fa-check-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.insertBefore(successDiv, loginForm.firstChild);
    }
}