# 🥊 Celebración Motivacional - Comité Tórax

## Descripción
Sistema de celebración visual y sonora que se activa cuando un médico guarda o actualiza los datos de un paciente exitosamente.

## Componentes

### 1. **celebration.css**
Estilos para el efecto de confetti y el modal de celebración:
- Animación de confetti cayendo (150 partículas de colores)
- Modal con gradiente púrpura y mensaje motivacional
- Overlay oscuro de fondo
- Animaciones suaves (pop, pulse, fade)

### 2. **celebration.js**
Lógica de la celebración:
- **Confetti**: Crea 150 partículas de colores aleatorios que caen con animaciones variadas
- **Sonido**: Reproduce un sonido de celebración (bugle_tune de Google Actions)
- **Modal**: Muestra mensaje "¡CAMPEÓN! 🥊 Paciente guardado exitosamente"
- **Auto-trigger**: Detecta automáticamente mensajes de éxito en alerts de Bootstrap

### 3. **Integración en base.html**
Los archivos CSS y JS se cargan globalmente en todas las páginas para detectar celebraciones.

## Triggers
La celebración se activa cuando aparece un alert de éxito con alguno de estos textos:
- ✅ "Paciente agregado correctamente"
- ✅ "Datos del paciente actualizados"

## Configuración

### Personalización del confetti
```javascript
const CONFETTI_COUNT = 150;  // Cantidad de partículas
const CONFETTI_COLORS = [...]; // Colores disponibles
```

### Personalización del sonido
```javascript
const sounds = [
    'URL_DEL_SONIDO_1',
    'URL_DEL_SONIDO_2'  // Fallback si el primero falla
];
audio.volume = 0.4;  // Volumen (0.0 - 1.0)
```

### Personalización del modal
Editar contenido en `showCelebrationModal()`:
```html
<h1>¡CAMPEÓN! 🥊</h1>
<p>Paciente guardado exitosamente</p>
<p>¡Seguí así, crack! 💪</p>
```

## Funcionamiento

1. Usuario guarda/actualiza paciente
2. Backend muestra flash message de éxito
3. JavaScript detecta el mensaje en el DOM
4. Se ejecuta `celebrate()`:
   - Crea confetti (300ms)
   - Reproduce sonido
   - Muestra modal (300ms después del confetti)
5. Modal se auto-cierra a los 5 segundos
6. Confetti desaparece a los 4 segundos

## Uso manual
Para activar la celebración desde código JavaScript:
```javascript
window.celebratePatientSave();
```

## Notas técnicas
- ✅ No bloquea la interfaz (pointer-events: none en confetti)
- ✅ Auto-limpieza de elementos DOM después de la animación
- ✅ Manejo de errores si el audio no carga
- ✅ Responsive (funciona en móvil)
- ✅ Compatible con todos los navegadores modernos
- ✅ Z-index alto (99999) para estar sobre todo contenido

## Créditos
- Sonidos: Google Actions Sounds (dominio público)
- Implementación: Comité Multidisciplinario de Tórax
- Inspiración: Gamificación para motivar al equipo médico 🚀
