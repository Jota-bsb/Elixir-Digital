// admin.js - Funcionalidades dinâmicas para a página de administração

document.addEventListener('DOMContentLoaded', function() {
    const refreshBtn = document.getElementById('refresh-btn');
    
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            location.reload();
        });
    }

    // Configurar event listeners para status
    setupStatusEventListeners();
    
    // Configurar event listeners para os botões de ação
    setupActionButtons();
});

// Configurar event listeners para os botões de ação
function setupActionButtons() {
    // Botões "Ver Detalhes"
    const viewDetailsBtns = document.querySelectorAll('.view-details-btn');
    viewDetailsBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const requestId = this.getAttribute('data-request-id');
            viewRequestDetails(requestId);
        });
    });
    
    // Botões "Contatar Cliente"
    const contactClientBtns = document.querySelectorAll('.contact-client-btn');
    contactClientBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const requestId = this.getAttribute('data-request-id');
            const email = this.getAttribute('data-email');
            contactClient(requestId, email);
        });
    });
}

// Configurar event listeners para status
function setupStatusEventListeners() {
    const statusOptions = document.querySelectorAll('.status-option');
    
    statusOptions.forEach(option => {
        option.addEventListener('click', function() {
            const requestId = this.getAttribute('data-request-id');
            const newStatus = this.getAttribute('data-status');
            
            updateRequestStatus(requestId, newStatus);
        });
    });
}

// Atualizar status da solicitação via API
async function updateRequestStatus(requestId, newStatus) {
    try {
        const response = await fetch(`/api/requests/${requestId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showNotification(`Status atualizado com sucesso!`, 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification('Erro ao atualizar status', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showNotification('Erro de conexão', 'error');
    }
}

// Funções globais
function viewRequestDetails(requestId) {
    alert(`Detalhes da solicitação #${requestId}`);
    // Aqui você pode implementar um modal ou redirecionar para uma página de detalhes
}

function contactClient(requestId, email) {
    alert(`Contatar cliente #${requestId}\nEmail: ${email}`);
    // Aqui você pode implementar a abertura do cliente de email
    // Exemplo: window.location.href = `mailto:${email}?subject=Solicitação #${requestId}`;
}

// Mostrar notificação
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
    
    notification.querySelector('.notification-close').addEventListener('click', () => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    });
}