document.addEventListener('DOMContentLoaded', function() {
    // Copy URL functionality
    const copyButtons = document.querySelectorAll('.copy-url');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const urlInput = this.previousElementSibling;
            urlInput.select();
            document.execCommand('copy');
            
            // Change button text temporarily
            const originalText = this.textContent;
            this.textContent = 'Copied!';
            setTimeout(() => {
                this.textContent = originalText;
            }, 2000);
        });
    });

    // Form validation
    const urlForm = document.querySelector('#url-form');
    if (urlForm) {
        urlForm.addEventListener('submit', function(e) {
            const urlInput = this.querySelector('#url');
            if (!isValidUrl(urlInput.value)) {
                e.preventDefault();
                showError(urlInput, 'Please enter a valid URL');
            }
        });
    }

    // Helper function to validate URL
    function isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;  
        }
    }

    // Helper function to show error
    function showError(input, message) {
        const formGroup = input.closest('.form-group');
        const errorDiv = formGroup.querySelector('.invalid-feedback') || document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        formGroup.appendChild(errorDiv);
        input.classList.add('is-invalid');
    }

    // Dismiss alerts automatically
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // Copy to clipboard functionality
    function copyToClipboard(elementId) {
        var copyText = document.getElementById(elementId);
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        document.execCommand("copy");
        alert("Copied the text: " + copyText.value);
    }

    var copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            copyToClipboard(this.getAttribute('data-copy-target'));
        });
    });
});
