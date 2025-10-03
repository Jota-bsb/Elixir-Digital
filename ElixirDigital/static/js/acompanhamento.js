// acompanhamento.js - Sistema de acompanhamento de solicitações

class AcompanhamentoSystem {
    constructor() {
        this.trackingForm = document.getElementById('trackingForm');
        this.errorMessage = document.getElementById('errorMessage');
        this.statusSection = document.getElementById('statusSection');
        this.trackingSection = document.querySelector('.tracking-section');
        this.requestsList = document.getElementById('requestsList');
        this.backButton = document.getElementById('backButton');
        
        this.init();
    }

    init() {
        if (this.trackingForm) {
            this.trackingForm.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        if (this.backButton) {
            this.backButton.addEventListener('click', () => this.showForm());
        }

        // Esconder a seção de resultados inicialmente
        this.hideResults();
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value.trim();
        
        if (!email) {
            this.showError('Por favor, digite um email válido.');
            return;
        }
        
        await this.buscarSolicitacoes(email);
    }

    async buscarSolicitacoes(email) {
        try {
            this.mostrarLoading(true);
            
            const response = await fetch('/api/acompanhamento', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email })
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                this.renderRequests(result.requests);
                this.showResults();
                this.hideError();
            } else {
                this.showError(result.message || 'Erro ao buscar solicitações.');
            }
            
        } catch (error) {
            console.error('Erro:', error);
            this.showError('Erro de conexão com o servidor.');
        } finally {
            this.mostrarLoading(false);
        }
    }

    renderRequests(requests) {
        if (!requests || requests.length === 0) {
            this.requestsList.innerHTML = `
                <div class="no-requests">
                    <h3>Nenhuma solicitação encontrada</h3>
                    <p>Não há solicitações para este email.</p>
                </div>
            `;
            return;
        }

        this.requestsList.innerHTML = requests.map(request => `
            <div class="request-card">
                <div class="request-header">
                    <div>
                        <div class="request-company">${this.escapeHtml(request.company)}</div>
                        <div class="request-date">Recebido em: ${this.escapeHtml(request.formatted_date)}</div>
                    </div>
                    <div class="request-id">#${this.escapeHtml(request.id)}</div>
                </div>

                <div class="request-details">
                    <div class="request-field">
                        <span class="field-label">Email:</span>
                        <span class="field-value">${this.escapeHtml(request.email)}</span>
                    </div>
                    <div class="request-field">
                        <span class="field-label">Telefone:</span>
                        <span class="field-value">${this.escapeHtml(request.phone)}</span>
                    </div>
                    <div class="request-field">
                        <span class="field-label">Descrição:</span>
                        <div class="field-value">${this.escapeHtml(request.description || 'Sem descrição')}</div>
                    </div>
                    <div class="request-field">
                        <span class="field-label">Tecnologias:</span>
                        <div class="field-value">${this.escapeHtml(request.technologies)}</div>
                    </div>
                    
                    <!-- Status atual do pedido -->
                    <div class="request-field">
                        <span class="field-label">Status Atual:</span>
                        <div class="current-status">
                            <span class="status-badge ${this.escapeHtml(request.status_class)}">
                                ${this.escapeHtml(request.status_display)}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    mostrarLoading(mostrar) {
        const submitButton = this.trackingForm.querySelector('.submit-button');
        
        if (mostrar) {
            submitButton.textContent = 'Buscando...';
            submitButton.disabled = true;
        } else {
            submitButton.textContent = 'Verificar Status';
            submitButton.disabled = false;
        }
    }

    showForm() {
        if (this.trackingForm) {
            this.trackingForm.reset();
        }
        this.hideResults();
        this.hideError();
    }

    showResults() {
        if (this.trackingSection) {
            this.trackingSection.style.display = 'none';
        }
        if (this.statusSection) {
            this.statusSection.style.display = 'block';
        }
    }

    hideResults() {
        if (this.statusSection) {
            this.statusSection.style.display = 'none';
        }
        if (this.trackingSection) {
            this.trackingSection.style.display = 'block';
        }
    }

    showError(message) {
        if (this.errorMessage) {
            const errorText = document.getElementById('errorText');
            if (errorText) {
                errorText.textContent = message;
            }
            this.errorMessage.style.display = 'block';
        }
    }

    hideError() {
        if (this.errorMessage) {
            this.errorMessage.style.display = 'none';
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Inicializar o sistema quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    new AcompanhamentoSystem();
});