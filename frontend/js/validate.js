/**
 * BookMyShoot — Shared Validation Library
 * Reusable, consistent validation across all forms
 * v1.0 — 2026-03-04
 */
const BMSValidate = (() => {
  'use strict';

  /* ═══════════════ REGEX PATTERNS ═══════════════ */
  const PATTERNS = {
    email: /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/,
    nameOnly: /^[A-Za-z\s\-'.]+$/,
    phone: /^[\d]{10}$/,
    phoneLoose: /^[\d\s\-\+\(\)]{7,15}$/,
    alphanumeric: /^[A-Za-z0-9\s]+$/,
    numericOnly: /^\d+(\.\d+)?$/,
    timeFormat: /^([01]?\d|2[0-3]):([0-5]\d)$/,
    strongPassword: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/,
    dateISO: /^\d{4}-\d{2}-\d{2}$/,
  };

  /* ═══════════════ SIZE LIMITS ═══════════════ */
  const LIMITS = {
    name: { min: 2, max: 50 },
    email: { max: 100 },
    phone: { min: 10, max: 10 },
    password: { min: 8, max: 128 },
    message: { min: 10, max: 2000 },
    subject: { max: 200 },
    bio: { max: 1000 },
    notes: { max: 500 },
    location: { max: 200 },
  };

  /* ═══════════════ FIELD VALIDATORS ═══════════════ */

  function validateName(value, fieldLabel = 'Name') {
    const v = (value || '').trim();
    if (!v) return `${fieldLabel} is required`;
    if (v.length < LIMITS.name.min) return `${fieldLabel} must be at least ${LIMITS.name.min} characters`;
    if (v.length > LIMITS.name.max) return `${fieldLabel} must be under ${LIMITS.name.max} characters`;
    if (!PATTERNS.nameOnly.test(v)) return `${fieldLabel} can only contain letters, spaces, hyphens, and apostrophes`;
    return null;
  }

  function validateEmail(value) {
    const v = (value || '').trim();
    if (!v) return 'Email is required';
    if (v.length > LIMITS.email.max) return `Email must be under ${LIMITS.email.max} characters`;
    if (!PATTERNS.email.test(v)) return 'Please enter a valid email address';
    return null;
  }

  function validatePhone(value, required = true) {
    const v = (value || '').trim();
    if (!v) return required ? 'Phone number is required' : null;
    const digits = v.replace(/\D/g, '');
    if (digits.length !== 10) return 'Phone number must be exactly 10 digits';
    if (!/^\d+$/.test(digits)) return 'Phone number must contain only numbers';
    return null;
  }

  function validatePassword(value, fieldLabel = 'Password') {
    const v = value || '';
    if (!v) return `${fieldLabel} is required`;
    if (v.length < LIMITS.password.min) return `${fieldLabel} must be at least ${LIMITS.password.min} characters`;
    if (v.length > LIMITS.password.max) return `${fieldLabel} is too long`;
    if (!/[a-z]/.test(v)) return `${fieldLabel} must include a lowercase letter`;
    if (!/[A-Z]/.test(v)) return `${fieldLabel} must include an uppercase letter`;
    if (!/\d/.test(v)) return `${fieldLabel} must include a number`;
    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(v)) return `${fieldLabel} must include a special character`;
    return null;
  }

  function validatePasswordMatch(password, confirmPassword) {
    if (!confirmPassword) return 'Please confirm your password';
    if (password !== confirmPassword) return 'Passwords do not match';
    return null;
  }

  function validateRequired(value, fieldLabel = 'This field') {
    const v = (typeof value === 'string') ? value.trim() : value;
    if (v === null || v === undefined || v === '') return `${fieldLabel} is required`;
    return null;
  }

  function validateDate(value, { allowPast = false, fieldLabel = 'Date' } = {}) {
    const v = (value || '').trim();
    if (!v) return `${fieldLabel} is required`;
    if (!PATTERNS.dateISO.test(v)) return `${fieldLabel} must be a valid date (YYYY-MM-DD)`;
    const d = new Date(v + 'T00:00:00');
    if (isNaN(d.getTime())) return `${fieldLabel} is not a valid date`;
    if (!allowPast) {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      if (d < today) return `${fieldLabel} cannot be in the past`;
    }
    return null;
  }

  function validateTime(value, { fieldLabel = 'Time', eventDate = null } = {}) {
    const v = (value || '').trim();
    if (!v) return `${fieldLabel} is required`;
    if (!PATTERNS.timeFormat.test(v)) return `${fieldLabel} must be in HH:MM format`;
    // If date is today, time must be in the future
    if (eventDate) {
      const today = new Date();
      const todayStr = today.toISOString().split('T')[0];
      if (eventDate === todayStr) {
        const [h, m] = v.split(':').map(Number);
        const now = new Date();
        if (h < now.getHours() || (h === now.getHours() && m <= now.getMinutes())) {
          return `${fieldLabel} must be in the future for today's date`;
        }
      }
    }
    return null;
  }

  function validateNumeric(value, { min, max, fieldLabel = 'Value', required = true } = {}) {
    const v = (value === undefined || value === null) ? '' : String(value).trim();
    if (!v) return required ? `${fieldLabel} is required` : null;
    if (!PATTERNS.numericOnly.test(v)) return `${fieldLabel} must be a number`;
    const n = parseFloat(v);
    if (min !== undefined && n < min) return `${fieldLabel} must be at least ${min}`;
    if (max !== undefined && n > max) return `${fieldLabel} must be at most ${max}`;
    return null;
  }

  function validateTextLength(value, { min = 0, max = 500, fieldLabel = 'Text', required = false } = {}) {
    const v = (value || '').trim();
    if (!v) return required ? `${fieldLabel} is required` : null;
    if (min && v.length < min) return `${fieldLabel} must be at least ${min} characters`;
    if (v.length > max) return `${fieldLabel} must be under ${max} characters`;
    return null;
  }

  /* ═══════════════ SANITIZATION ═══════════════ */

  function sanitize(value) {
    if (typeof value !== 'string') return value;
    return value
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;');
  }

  function cleanInput(value) {
    if (typeof value !== 'string') return value;
    return value.trim().replace(/\s+/g, ' ');
  }

  /* ═══════════════ DOM HELPERS ═══════════════ */

  /**
   * Show/hide error message and highlight field
   * @param {HTMLElement} field - The input element
   * @param {string|null} error - Error message or null if valid
   */
  function showFieldError(field, error) {
    if (!field) return;
    // Find or create error container
    let errEl = field.parentElement.querySelector('.bms-field-error');
    if (!errEl) {
      errEl = document.createElement('div');
      errEl.className = 'bms-field-error';
      errEl.style.cssText = 'color:#dc3545;font-size:0.78rem;margin-top:4px;font-weight:500;display:flex;align-items:center;gap:4px;';
      field.parentElement.appendChild(errEl);
    }
    if (error) {
      errEl.innerHTML = `<i class="bi bi-exclamation-circle" style="font-size:0.8rem;"></i> ${sanitize(error)}`;
      errEl.style.display = 'flex';
      field.style.borderColor = '#dc3545';
      field.style.boxShadow = '0 0 0 2px rgba(220,53,69,0.15)';
      field.classList.add('bms-invalid');
      field.classList.remove('bms-valid');
    } else {
      errEl.style.display = 'none';
      errEl.innerHTML = '';
      field.style.borderColor = '#28a745';
      field.style.boxShadow = '0 0 0 2px rgba(40,167,69,0.1)';
      field.classList.remove('bms-invalid');
      field.classList.add('bms-valid');
    }
  }

  /** Clear all validation state from a field */
  function clearFieldState(field) {
    if (!field) return;
    const errEl = field.parentElement.querySelector('.bms-field-error');
    if (errEl) { errEl.style.display = 'none'; errEl.innerHTML = ''; }
    field.style.borderColor = '';
    field.style.boxShadow = '';
    field.classList.remove('bms-invalid', 'bms-valid');
  }

  /** Clear all validation from a form */
  function clearForm(formEl) {
    if (!formEl) return;
    formEl.querySelectorAll('.bms-field-error').forEach(e => { e.style.display = 'none'; });
    formEl.querySelectorAll('.bms-invalid, .bms-valid').forEach(e => {
      e.classList.remove('bms-invalid', 'bms-valid');
      e.style.borderColor = '';
      e.style.boxShadow = '';
    });
  }

  /**
   * Validate all fields in a rules map and show errors
   * @param {Object} rules - { fieldId: { validate: fn, label: string } }
   * @returns {boolean} true if all valid
   */
  function validateForm(rules) {
    let allValid = true;
    for (const [fieldId, rule] of Object.entries(rules)) {
      const field = document.getElementById(fieldId);
      if (!field) continue;
      const error = rule.validate(field.value);
      showFieldError(field, error);
      if (error) allValid = false;
    }
    return allValid;
  }

  /**
   * Attach real-time validation listeners to fields
   * @param {Object} rules - { fieldId: { validate: fn } }
   */
  function attachLiveValidation(rules) {
    for (const [fieldId, rule] of Object.entries(rules)) {
      const field = document.getElementById(fieldId);
      if (!field) continue;
      const handler = () => {
        const error = rule.validate(field.value);
        showFieldError(field, error);
      };
      field.addEventListener('input', handler);
      field.addEventListener('blur', handler);
    }
  }

  /* ═══════════════ SUBMIT PROTECTION ═══════════════ */

  const _submitting = new Set();

  /** Prevent double submission: returns true if allowed, false if already in progress */
  function guardSubmit(formId) {
    if (_submitting.has(formId)) return false;
    _submitting.add(formId);
    return true;
  }

  function releaseSubmit(formId) {
    _submitting.delete(formId);
  }

  /** Set button loading state */
  function setButtonLoading(btn, loading, originalText) {
    if (!btn) return;
    if (loading) {
      btn._originalText = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" style="width:14px;height:14px;border-width:2px;margin-right:6px;display:inline-block;vertical-align:middle;animation:bms-spin .6s linear infinite;border:2px solid currentColor;border-right-color:transparent;border-radius:50%;"></span> Processing...`;
    } else {
      btn.disabled = false;
      btn.innerHTML = btn._originalText || originalText || 'Submit';
    }
  }

  /* ═══════════════ DATE/TIME UTILITIES ═══════════════ */

  /** Get today's date as YYYY-MM-DD (local timezone) */
  function todayISO() {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  }

  /** Check if two date strings represent the same day */
  function isSameDay(d1, d2) {
    return d1 === d2;
  }

  /** Get available time slots filtering out past times if date is today */
  function getAvailableTimeSlots(selectedDate, bookedSlots = []) {
    const allSlots = [];
    for (let h = 9; h <= 18; h++) {
      allSlots.push(`${String(h).padStart(2, '0')}:00`);
    }
    const now = new Date();
    const todayStr = todayISO();
    return allSlots.map(slot => {
      const booked = bookedSlots.includes(slot);
      let pastTime = false;
      if (selectedDate === todayStr) {
        const [sh] = slot.split(':').map(Number);
        pastTime = sh <= now.getHours();
      }
      return { time: slot, available: !booked && !pastTime, booked, pastTime };
    });
  }

  /** Format 24h time to 12h display */
  function formatTime12h(time24) {
    const [h, m] = time24.split(':').map(Number);
    const period = h >= 12 ? 'PM' : 'AM';
    const h12 = h === 0 ? 12 : h > 12 ? h - 12 : h;
    return `${h12}:${String(m).padStart(2, '0')} ${period}`;
  }

  /* ═══════════════ STYLE INJECTION ═══════════════ */
  function injectStyles() {
    if (document.getElementById('bms-validate-styles')) return;
    const style = document.createElement('style');
    style.id = 'bms-validate-styles';
    style.textContent = `
      @keyframes bms-spin { to { transform: rotate(360deg); } }
      .bms-invalid { border-color: #dc3545 !important; }
      .bms-valid { border-color: #28a745 !important; }
      .bms-field-error { transition: all 0.2s ease; }
      .bms-field-error i { flex-shrink: 0; }
    `;
    document.head.appendChild(style);
  }
  // Auto-inject
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', injectStyles);
    } else {
      injectStyles();
    }
  }

  /* ═══════════════ PUBLIC API ═══════════════ */
  return {
    // Validators
    validateName,
    validateEmail,
    validatePhone,
    validatePassword,
    validatePasswordMatch,
    validateRequired,
    validateDate,
    validateTime,
    validateNumeric,
    validateTextLength,
    // Sanitization
    sanitize,
    cleanInput,
    // DOM helpers
    showFieldError,
    clearFieldState,
    clearForm,
    validateForm,
    attachLiveValidation,
    // Submit protection
    guardSubmit,
    releaseSubmit,
    setButtonLoading,
    // Date/Time
    todayISO,
    isSameDay,
    getAvailableTimeSlots,
    formatTime12h,
    // Constants
    PATTERNS,
    LIMITS,
  };
})();
