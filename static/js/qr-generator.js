document.addEventListener('DOMContentLoaded', function() {
    // Update range slider values in real-time
    const boxSizeSlider = document.getElementById('box_size');
    const boxSizeValue = document.getElementById('box_size_value');
    const borderSlider = document.getElementById('border');
    const borderValue = document.getElementById('border_value');

    // Update box size value display
    if (boxSizeSlider && boxSizeValue) {
        boxSizeSlider.addEventListener('input', function() {
            boxSizeValue.textContent = this.value;
        });
    }

    // Update border value display
    if (borderSlider && borderValue) {
        borderSlider.addEventListener('input', function() {
            borderValue.textContent = this.value;
        });
    }

    // Handle transparent background checkbox
    const transparentBgCheckbox = document.getElementById('transparent_bg');
    const backColorPicker = document.getElementById('back_color');

    if (transparentBgCheckbox && backColorPicker) {
        function toggleBackgroundColor() {
            if (transparentBgCheckbox.checked) {
                backColorPicker.disabled = true;
                backColorPicker.style.opacity = '0.5';
                backColorPicker.parentElement.querySelector('label').style.opacity = '0.5';
            } else {
                backColorPicker.disabled = false;
                backColorPicker.style.opacity = '1';
                backColorPicker.parentElement.querySelector('label').style.opacity = '1';
            }
        }

        // Initial state
        toggleBackgroundColor();

        // Listen for changes
        transparentBgCheckbox.addEventListener('change', toggleBackgroundColor);
    }
});