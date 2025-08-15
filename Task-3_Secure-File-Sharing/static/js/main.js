// File upload handling
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                fileName.textContent = file.name;
                fileSize.textContent = formatFileSize(file.size);
                fileInfo.style.display = 'block';
            } else {
                fileInfo.style.display = 'none';
            }
        });
    }
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Add loading state to buttons
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn') && !e.target.classList.contains('btn-sm')) {
        const originalText = e.target.innerHTML;
        e.target.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        e.target.disabled = true;
        
        // Re-enable after a delay (for demo purposes)
        setTimeout(function() {
            e.target.innerHTML = originalText;
            e.target.disabled = false;
        }, 2000);
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add animation to file cards
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.file-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
});

// Modal functionality
function showDecryptInfo(filename) {
    fetch(`/decrypt-info/${filename}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            const modal = document.getElementById('decryptModal');
            const infoDiv = document.getElementById('decryptInfo');
            
            infoDiv.innerHTML = `
                <div class="info-grid">
                    <div class="info-item">
                        <h4>File Name</h4>
                        <p>${data.filename}</p>
                    </div>
                    <div class="info-item">
                        <h4>Upload Time</h4>
                        <p>${data.upload_time}</p>
                    </div>
                    <div class="info-item">
                        <h4>Original Size</h4>
                        <p>${formatFileSize(data.original_size)}</p>
                    </div>
                    <div class="info-item">
                        <h4>Encrypted Size</h4>
                        <p>${formatFileSize(data.encrypted_size)}</p>
                    </div>
                    <div class="info-item">
                        <h4>Encryption Algorithm</h4>
                        <p>${data.encryption_algorithm}</p>
                    </div>
                    <div class="info-item">
                        <h4>Key Length</h4>
                        <p>${data.key_length} bits</p>
                    </div>
                    <div class="info-item">
                        <h4>IV Length</h4>
                        <p>${data.iv_length} bits</p>
                    </div>
                    <div class="info-item">
                        <h4>Hash Algorithm</h4>
                        <p>${data.hash_algorithm}</p>
                    </div>
                </div>
                <div class="info-item" style="grid-column: 1 / -1;">
                    <h4>File Hash (SHA-256)</h4>
                    <p style="word-break: break-all; font-family: monospace;">${data.hash}</p>
                </div>
            `;
            
            modal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching decryption information');
        });
}

function verifyIntegrity(filename) {
    fetch(`/verify-integrity/${filename}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }
            
            const modal = document.getElementById('integrityModal');
            const infoDiv = document.getElementById('integrityInfo');
            
            const integrityClass = data.integrity_valid ? 'integrity-valid' : 'integrity-invalid';
            const integrityIcon = data.integrity_valid ? 'check-circle' : 'exclamation-triangle';
            const integrityMessage = data.integrity_valid ? 'File integrity verified successfully!' : 'File integrity check failed!';
            
            infoDiv.innerHTML = `
                <div class="info-grid">
                    <div class="info-item">
                        <h4>File Name</h4>
                        <p>${data.filename}</p>
                    </div>
                    <div class="info-item">
                        <h4>File Size</h4>
                        <p>${formatFileSize(data.file_size)}</p>
                    </div>
                    <div class="info-item">
                        <h4>Encrypted Size</h4>
                        <p>${formatFileSize(data.encrypted_size)}</p>
                    </div>
                </div>
                <div class="integrity-result ${integrityClass}">
                    <i class="fas fa-${integrityIcon}"></i>
                    <h4>${integrityMessage}</h4>
                    <p>Calculated Hash: <code>${data.calculated_hash}</code></p>
                    <p>Stored Hash: <code>${data.stored_hash}</code></p>
                </div>
            `;
            
            modal.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error verifying file integrity');
        });
}

// Close modal when clicking on X or outside
document.addEventListener('DOMContentLoaded', function() {
    const modals = document.querySelectorAll('.modal');
    const closeButtons = document.querySelectorAll('.close');
    
    closeButtons.forEach(button => {
        button.onclick = function() {
            modals.forEach(modal => modal.style.display = 'none');
        }
    });
    
    window.onclick = function(event) {
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
});
