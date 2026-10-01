/**
 * Form validation and submission handler for user registration.
 * 
 * This module handles client-side form validation feedback and submission
 * to the backend. All critical validation is performed server-side.
 * Frontend validation is for UX/feedback purposes only.
 */

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registrationForm');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const submitBtn = document.getElementById('submitBtn');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');
    const errorDetail = document.getElementById('errorDetail');

    // Validation patterns
    const patterns = {
        username: /^[a-zA-Z][a-zA-Z0-9_]*$/,
        email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    };

    /**
     * Validate username format.
     * @returns {Object} Validation result with isValid and message.
     */
    function validateUsername() {
        const username = usernameInput.value.trim();
        const feedback = document.getElementById('usernameFeedback');

        if (!username) {
            showFeedback(feedback, 'Username is required');
            return { isValid: false };
        }

        if (username.length < 4) {
            showFeedback(feedback, 'Username must be at least 4 characters');
            return { isValid: false };
        }

        if (username.length > 20) {
            showFeedback(feedback, 'Username must not exceed 20 characters');
            return { isValid: false };
        }

        if (!patterns.username.test(username)) {
            showFeedback(
                feedback,
                'Username must start with a letter and contain only letters, numbers, and underscores'
            );
            return { isValid: false };
        }

        hideFeedback(feedback);
        return { isValid: true };
    }

    /**
     * Validate email format.
     * @returns {Object} Validation result with isValid and message.
     */
    function validateEmail() {
        const email = emailInput.value.trim();
        const feedback = document.getElementById('emailFeedback');

        if (!email) {
            showFeedback(feedback, 'Email address is required');
            return { isValid: false };
        }

        if (!patterns.email.test(email)) {
            showFeedback(feedback, 'Please enter a valid email address');
            return { isValid: false };
        }

        if (email.length > 120) {
            showFeedback(feedback, 'Email address is too long');
            return { isValid: false };
        }

        hideFeedback(feedback);
        return { isValid: true };
    }

    /**
     * Validate password strength.
     * @returns {Object} Validation result with isValid and message.
     */
    function validatePassword() {
        const password = passwordInput.value;
        const feedback = document.getElementById('passwordFeedback');

        if (!password) {
            showFeedback(feedback, 'Password is required');
            return { isValid: false };
        }

        if (password.length < 8) {
            showFeedback(feedback, 'Password must be at least 8 characters');
            return { isValid: false };
        }

        if (!/\d/.test(password)) {
            showFeedback(feedback, 'Password must contain at least one number');
            return { isValid: false };
        }

        hideFeedback(feedback);
        updatePasswordRequirements();
        return { isValid: true };
    }

    /**
     * Validate password confirmation match.
     * @returns {Object} Validation result with isValid and message.
     */
    function validateConfirmPassword() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const feedback = document.getElementById('confirmPasswordFeedback');
        const indicator = document.getElementById('confirmPasswordIndicator');

        if (!confirmPassword) {
            showFeedback(feedback, 'Password confirmation is required');
            indicator.classList.add('hidden');
            confirmPasswordInput.setAttribute('aria-invalid', 'true');
            return { isValid: false };
        }

        if (password !== confirmPassword) {
            showFeedback(feedback, 'Passwords do not match');
            indicator.classList.add('hidden');
            confirmPasswordInput.setAttribute('aria-invalid', 'true');
            return { isValid: false };
        }

        hideFeedback(feedback);
        indicator.classList.remove('hidden');
        confirmPasswordInput.setAttribute('aria-invalid', 'false');
        return { isValid: true };
    }

    /**
     * Update visual password requirement indicators.
     */
    function updatePasswordRequirements() {
        const password = passwordInput.value;
        const lengthReq = document.getElementById('requirementLength');
        const numberReq = document.getElementById('requirementNumber');

        if (password.length >= 8) {
            lengthReq.classList.add('bg-green-500', 'border-green-500');
            lengthReq.classList.remove('border-gray-300');
            lengthReq.innerHTML =
                '<svg class="w-2 h-2 text-white" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>';
        } else {
            lengthReq.classList.remove('bg-green-500', 'border-green-500');
            lengthReq.classList.add('border-gray-300');
            lengthReq.innerHTML = '';
        }

        if (/\d/.test(password)) {
            numberReq.classList.add('bg-green-500', 'border-green-500');
            numberReq.classList.remove('border-gray-300');
            numberReq.innerHTML =
                '<svg class="w-2 h-2 text-white" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>';
        } else {
            numberReq.classList.remove('bg-green-500', 'border-green-500');
            numberReq.classList.add('border-gray-300');
            numberReq.innerHTML = '';
        }
    }

    /**
     * Display validation feedback message.
     */
    function showFeedback(element, message) {
        element.textContent = message;
        element.classList.remove('hidden');
    }

    /**
     * Hide validation feedback message.
     */
    function hideFeedback(element) {
        element.classList.add('hidden');
        element.textContent = '';
    }

    /**
     * Validate all form fields.
     * @returns {boolean} True if all fields are valid.
     */
    function validateForm() {
        const usernameValid = validateUsername().isValid;
        const emailValid = validateEmail().isValid;
        const passwordValid = validatePassword().isValid;
        const confirmPasswordValid = validateConfirmPassword().isValid;

        return usernameValid && emailValid && passwordValid && confirmPasswordValid;
    }

    /**
     * Display error message from backend.
     */
    function displayError(message, details = '') {
        errorMessage.classList.remove('hidden');
        document.getElementById('errorTitle').textContent = message;
        if (details) {
            errorDetail.textContent = details;
        }
        successMessage.classList.add('hidden');
        scrollToTop();
    }

    /**
     * Display success message.
     */
    function displaySuccess() {
        successMessage.classList.remove('hidden');
        errorMessage.classList.add('hidden');
        scrollToTop();
    }

    /**
     * Scroll to top of form to show messages.
     */
    function scrollToTop() {
        document.querySelector('.bg-white.rounded-lg.shadow-xl').scrollIntoView({
            behavior: 'smooth',
            block: 'start',
        });
    }

    /**
     * Set form loading state.
     */
    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        submitBtn.setAttribute('aria-busy', isLoading);
        document.getElementById('loadingIndicator').classList.toggle('hidden', !isLoading);
    }

    /**
     * Handle form submission.
     */
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Reset messages
        errorMessage.classList.add('hidden');
        successMessage.classList.add('hidden');

        // Client-side validation
        if (!validateForm()) {
            displayError('Please fix the errors above');
            return;
        }

        // Prepare form data
        const formData = new FormData(form);
        const data = {
            username: formData.get('username').trim(),
            email: formData.get('email').trim(),
            password: formData.get('password'),
            confirm_password: formData.get('confirm_password'),
        };

        setLoading(true);

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok && response.status === 201) {
                displaySuccess();
                form.reset();
                document.getElementById('requirementLength').classList.remove('bg-green-500', 'border-green-500');
                document.getElementById('requirementNumber').classList.remove('bg-green-500', 'border-green-500');
                document.getElementById('confirmPasswordIndicator').classList.add('hidden');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            } else {
                const errorMsg = result.error || 'Registration failed. Please try again.';
                let details = '';

                // Handle different error response formats
                if (result.details) {
                    if (typeof result.details === 'object') {
                        // If details is an object, format it nicely
                        details = Object.values(result.details).join(' ');
                    } else {
                        // If it's a string, use it as-is
                        details = result.details;
                    }
                }

                displayError(errorMsg, details);
            }
        } catch (error) {
            console.error('Registration error:', error);
            displayError('Network error. Please check your connection and try again.');
        } finally {
            setLoading(false);
        }
    });

    // Real-time validation listeners
    usernameInput.addEventListener('blur', validateUsername);
    usernameInput.addEventListener('input', validateUsername);

    emailInput.addEventListener('blur', validateEmail);
    emailInput.addEventListener('input', validateEmail);

    passwordInput.addEventListener('input', function () {
        validatePassword();
        validateConfirmPassword();
    });

    confirmPasswordInput.addEventListener('input', validateConfirmPassword);

    // Hide error messages when user starts typing
    [usernameInput, emailInput, passwordInput, confirmPasswordInput].forEach(input => {
        input.addEventListener('focus', function () {
            errorMessage.classList.add('hidden');
        });
    });
});
