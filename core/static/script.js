// Función para mostrar/ocultar rutas con animación mejorada
function toggleRutas() {
    const contenedor = document.getElementById('rutasContainer');
    const button = document.querySelector('[onclick="toggleRutas()"]');
    
    if (contenedor.style.display === 'none' || contenedor.style.display === '') {
        // Mostrar rutas
        contenedor.style.display = 'block';
        contenedor.classList.add('fade-in');
        
        // Actualizar texto del botón
        if (button) {
            button.innerHTML = '<i class="fas fa-eye-slash me-1"></i> Ocultar rutas';
            button.classList.remove('btn-outline-primary');
            button.classList.add('btn-outline-secondary');
        }
        
        // Scroll suave hacia las rutas
        setTimeout(() => {
            contenedor.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 100);
        
    } else {
        // Ocultar rutas
        contenedor.classList.remove('fade-in');
        contenedor.classList.add('fade-out');
        
        // Actualizar texto del botón
        if (button) {
            button.innerHTML = '<i class="fas fa-route me-1"></i> Ver rutas';
            button.classList.remove('btn-outline-secondary');
            button.classList.add('btn-outline-primary');
        }
        
        setTimeout(() => {
            contenedor.style.display = 'none';
            contenedor.classList.remove('fade-out');
        }, 300);
    }
}

// Animaciones CSS dinámicas
document.addEventListener('DOMContentLoaded', function() {
    // Agregar clases de animación
    const style = document.createElement('style');
    style.textContent = `
        .fade-in {
            animation: fadeInUp 0.5s ease-out forwards;
        }
        
        .fade-out {
            animation: fadeOutDown 0.3s ease-in forwards;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeOutDown {
            from {
                opacity: 1;
                transform: translateY(0);
            }
            to {
                opacity: 0;
                transform: translateY(-20px);
            }
        }
        
        /* Animación para hover en tarjetas */
        .card {
            transition: all 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        /* Animación para botones */
        .btn {
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.2);
            transition: left 0.5s ease;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        /* Animación para elementos de lista */
        .list-group-item,
        .reservation-item {
            transition: all 0.3s ease;
        }
        
        .list-group-item:hover,
        .reservation-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* Animación de entrada para formularios */
        .form-control:focus {
            transform: scale(1.02);
            transition: transform 0.2s ease;
        }
        
        /* Loading animation para botones */
        .btn-loading {
            position: relative;
            color: transparent !important;
        }
        
        .btn-loading::after {
            content: '';
            position: absolute;
            width: 16px;
            height: 16px;
            top: 50%;
            left: 50%;
            margin-left: -8px;
            margin-top: -8px;
            border: 2px solid #ffffff;
            border-radius: 50%;
            border-top-color: transparent;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
        
        /* Mejoras para navbar fijo */
        .navbar.fixed-top {
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        /* Animación para badges */
        .badge {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
            100% {
                transform: scale(1);
            }
        }
    `;
    document.head.appendChild(style);
    
    // Agregar efectos de scroll
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (navbar && navbar.classList.contains('fixed-top')) {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(255, 255, 255, 0.98)';
                navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
            } else {
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
                navbar.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
            }
        }
    });
    
    // Agregar loading state a los formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('btn-loading');
                submitBtn.disabled = true;
                
                // Remover loading state después de 5 segundos como backup
                setTimeout(() => {
                    submitBtn.classList.remove('btn-loading');
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
    
    // Validación en tiempo real para formularios
    const inputs = document.querySelectorAll('.form-control, .form-select');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateField(this);
            }
        });
    });
    
    // Auto-focus en el primer campo de formularios
    const firstInput = document.querySelector('.form-control');
    if (firstInput && !firstInput.value) {
        firstInput.focus();
    }
    
    // Confirmar antes de enviar formularios importantes
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || '¿Estás seguro?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
});

// Función de validación de campos
function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let message = '';
    
    // Validaciones específicas por tipo
    if (field.type === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (value && !emailRegex.test(value)) {
            isValid = false;
            message = 'Por favor ingresa un email válido';
        }
    }
    
    if (field.type === 'tel') {
        const phoneRegex = /^[\+]?[0-9\s\-\(\)]+$/;
        if (value && !phoneRegex.test(value)) {
            isValid = false;
            message = 'Por favor ingresa un teléfono válido';
        }
    }
    
    if (field.required && !value) {
        isValid = false;
        message = 'Este campo es obligatorio';
    }
    
    // Aplicar estilos de validación
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
    
    // Mostrar mensaje de error
    let feedback = field.parentNode.querySelector('.invalid-feedback');
    if (!feedback && !isValid) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        field.parentNode.appendChild(feedback);
    }
    
    if (feedback) {
        feedback.textContent = message;
        feedback.style.display = isValid ? 'none' : 'block';
    }
}

// Función para mostrar notificaciones toast
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remover el toast después de que se oculte
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Crear contenedor de toasts si no existe
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Función para formatear fechas
function formatDate(date) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        weekday: 'long'
    };
    return new Date(date).toLocaleDateString('es-ES', options);
}

// Función para formatear hora
function formatTime(time) {
    return new Date(`1970-01-01T${time}`).toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
    });
}