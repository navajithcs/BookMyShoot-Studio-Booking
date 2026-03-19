class CustomModal {
  constructor() {
    this.overlay = null;
    this.titleEl = null;
    this.messageEl = null;
    this.confirmBtn = null;
    this.onClose = null;

    this.init();
  }

  init() {
    // Create DOM elements
    this.overlay = document.createElement('div');
    this.overlay.className = 'custom-modal-overlay';

    this.overlay.innerHTML = `
      <div class="custom-modal-content">
        <h2 class="custom-modal-title"></h2>
        <p class="custom-modal-message"></p>
        <button class="custom-modal-btn">OK</button>
      </div>
    `;

    document.body.appendChild(this.overlay);

    // Cache elements
    this.titleEl = this.overlay.querySelector('.custom-modal-title');
    this.messageEl = this.overlay.querySelector('.custom-modal-message');
    this.confirmBtn = this.overlay.querySelector('.custom-modal-btn');

    // Event Listeners
    this.confirmBtn.addEventListener('click', () => this.hide());
    
    // Close on outside click (optional)
    this.overlay.addEventListener('click', (e) => {
      if (e.target === this.overlay) {
        this.hide();
      }
    });
  }

  show(title, message, callback = null) {
    this.titleEl.textContent = title;
    this.messageEl.textContent = message;
    this.onClose = callback;

    this.overlay.classList.add('active');
  }

  hide() {
    this.overlay.classList.remove('active');
    
    if (this.onClose) {
      this.onClose();
      this.onClose = null;
    }
  }
}

// Singleton instance
const modalSystem = new CustomModal();

// Global helper function
window.showModal = function(title, message, callback) {
  modalSystem.show(title, message, callback);
};
