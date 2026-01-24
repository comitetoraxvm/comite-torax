// Celebración motivacional para cuando se guarda un paciente exitosamente
(function() {
    'use strict';

    // Protección contra errores
    if (typeof document === 'undefined' || typeof window === 'undefined') {
        return;
    }

    // Configuración
    const CONFETTI_COUNT = 150;
    const CONFETTI_COLORS = ['#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#03a9f4', '#00bcd4', '#009688', '#4caf50', '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107', '#ff9800', '#ff5722'];
    
    // Crear confetti
    function createConfetti() {
        const container = document.createElement('div');
        container.className = 'confetti-container';
        document.body.appendChild(container);

        for (let i = 0; i < CONFETTI_COUNT; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.backgroundColor = CONFETTI_COLORS[Math.floor(Math.random() * CONFETTI_COLORS.length)];
                confetti.style.animationDelay = Math.random() * 0.3 + 's';
                confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
                
                // Tamaño aleatorio
                const size = Math.random() * 10 + 5;
                confetti.style.width = size + 'px';
                confetti.style.height = size + 'px';
                
                container.appendChild(confetti);
            }, i * 10);
        }

        // Limpiar después de la animación
        setTimeout(() => {
            container.remove();
        }, 4000);
    }

    // Reproducir sonido de campana
    function playBellSound() {
        try {
            // Múltiples opciones de sonido de celebración (fallback si uno no carga)
            const sounds = [
                'https://actions.google.com/sounds/v1/alarms/bugle_tune.ogg',
                'https://actions.google.com/sounds/v1/cartoon/siren_whistle.ogg'
            ];
            
            if (sounds[0]) {
                const audio = new Audio(sounds[0]);
                if (audio) {
                    audio.volume = 0.4;
                    const playPromise = audio.play();
                    if (playPromise !== undefined) {
                        playPromise.catch(err => {
                            console.log('No se pudo reproducir el sonido:', err);
                        });
                    }
                }
            }
        } catch (e) {
            console.log('Audio no disponible');
        }
    }

    // Mostrar modal de celebración
    function showCelebrationModal(isNewPatient) {
        const overlay = document.createElement('div');
        overlay.className = 'celebration-overlay';
        
        const messages = isNewPatient ? {
            title: '¡CAMPEÓN! 🥊',
            subtitle: 'Nuevo paciente agregado exitosamente',
            motivation: '¡Un paciente más bajo tu cuidado, crack! 💪'
        } : {
            title: '¡GENIAL! ⭐',
            subtitle: 'Datos actualizados correctamente',
            motivation: '¡Seguimiento impecable! 🎯'
        };
        
        const modal = document.createElement('div');
        modal.className = 'celebration-modal';
        modal.innerHTML = `
            <h1>${messages.title}</h1>
            <p>${messages.subtitle}</p>
            <p style="font-size: 1rem; opacity: 0.9;">${messages.motivation}</p>
            <button class="btn" onclick="this.parentElement.parentElement.remove(); document.querySelector('.celebration-overlay').remove();">
                ¡Dale! 🚀
            </button>
        `;

        document.body.appendChild(overlay);
        document.body.appendChild(modal);

        // Auto-cerrar después de 5 segundos
        setTimeout(() => {
            if (modal.parentElement) {
                modal.remove();
                overlay.remove();
            }
        }, 5000);
    }

    // Función principal de celebración
    function celebrate(isNewPatient) {
        createConfetti();
        playBellSound();
        setTimeout(() => showCelebrationModal(isNewPatient), 300);
    }

    // Exponer globalmente
    window.celebratePatientSave = celebrate;

    // Auto-trigger si hay mensaje de éxito en la página
    document.addEventListener('DOMContentLoaded', function() {
        try {
            const alerts = document.querySelectorAll('.alert-success');
            if (alerts && alerts.length > 0) {
                alerts.forEach(function(alert) {
                    if (!alert) return;
                    const text = (alert.textContent || alert.innerText || '').toString();
                    const isNewPatient = text.includes('Paciente agregado correctamente');
                    const isUpdate = text.includes('Datos del paciente actualizados');
                    
                    if (isNewPatient || isUpdate) {
                        // Pequeño delay para que se vea el mensaje
                        setTimeout(() => celebrate(isNewPatient), 100);
                    }
                });
            }
        } catch (err) {
            console.log('Error en celebración:', err);
        }
    });
})();
