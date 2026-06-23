document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const form = document.getElementById('idea-form');
    const submitBtn = document.getElementById('submit-btn');
    const loader = document.getElementById('loader');
    const resultsSection = document.getElementById('results');
    const errorBox = document.getElementById('error-box');
    const errorMessage = document.getElementById('error-message');
    const ideasGrid = document.getElementById('ideas-grid');
    const rankingReason = document.getElementById('ranking-reason');
    
    // Navbar Hamburger menu
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link, .nav-cta');
    
    // Modal Elements
    const detailsModal = document.getElementById('details-modal');
    const modalClose = document.getElementById('modal-close');
    const modalTitle = document.getElementById('modal-idea-title');
    const modalDesc = document.getElementById('modal-idea-desc');
    const modalType = document.getElementById('modal-idea-type');
    const modalTechList = document.getElementById('modal-tech-list');
    const modalRoadmapList = document.getElementById('modal-roadmap-list');
    const modalComplexityVal = document.getElementById('modal-complexity-val');
    const modalComplexityBar = document.getElementById('modal-complexity-bar');
    const modalImpactVal = document.getElementById('modal-impact-val');
    const modalImpactBar = document.getElementById('modal-impact-bar');

    const API_URL = 'http://127.0.0.1:8000/generate-ideas';

    // Global state to store last generated ideas for modal lookup
    let generatedIdeasCache = [];
    let activeIdeaIndex = -1;

    // Categories mapping to match different type rules
    const ideaTypeLabels = [
        "AI-Centric Solution",
        "Web/App Platform",
        "Automation & System Tool"
    ];

    // Navbar toggle trigger
    const navbarEl = document.querySelector('.navbar');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
            if (navbarEl) {
                navbarEl.classList.toggle('mobile-active');
            }
        });
    }

    // Close mobile navbar menu on navigation link clicks
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                if (navbarEl) {
                    navbarEl.classList.remove('mobile-active');
                }
            }
        });
    });

    // Auto-suggest dropdown logic and quick select pills
    const domainInput = document.getElementById('domain');
    const suggestionsBox = document.getElementById('suggestions-box');
    const quickPills = document.querySelectorAll('.quick-pill');
    
    // Toggle suggestions box visibility and dropdown arrow active state
    const dropdownArrow = document.querySelector('.dropdown-arrow-btn');
    
    if (domainInput && suggestionsBox) {
        const toggleDropdown = (show) => {
            if (show) {
                suggestionsBox.classList.remove('hidden');
                if (dropdownArrow) dropdownArrow.classList.add('active');
            } else {
                suggestionsBox.classList.add('hidden');
                if (dropdownArrow) dropdownArrow.classList.remove('active');
            }
        };

        domainInput.addEventListener('focus', () => {
            toggleDropdown(true);
        });
        
        // Hide with delay so clicks inside the dropdown register first
        domainInput.addEventListener('blur', () => {
            setTimeout(() => {
                toggleDropdown(false);
            }, 200);
        });

        // Click suggestion item to populate input (using mousedown to resolve focus blur race conditions)
        suggestionsBox.addEventListener('mousedown', (e) => {
            const item = e.target.closest('.suggestion-item');
            if (item) {
                domainInput.value = item.textContent.trim();
                toggleDropdown(false);
                e.preventDefault(); // Keep focus inside the input so user can edit if needed
            }
        });

        // Toggle dropdown on arrow button click
        if (dropdownArrow) {
            dropdownArrow.addEventListener('mousedown', (e) => {
                e.preventDefault(); // Prevents browser focus blur cycle
                const isHidden = suggestionsBox.classList.contains('hidden');
                if (isHidden) {
                    domainInput.focus();
                    toggleDropdown(true);
                } else {
                    toggleDropdown(false);
                    domainInput.blur();
                }
            });
        }
    }

    // Click quick pill to populate input
    quickPills.forEach(pill => {
        pill.addEventListener('click', () => {
            if (domainInput) {
                domainInput.value = pill.getAttribute('data-value');
            }
        });
    });

    // Form submission API flow
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. Reset state
        errorBox.classList.add('hidden');
        resultsSection.classList.add('hidden');
        loader.classList.remove('hidden');
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = 'Forging Ideas...';

        // Scroll to loader smoothly
        loader.scrollIntoView({ behavior: 'smooth' });

        // 2. Read values
        const domainVal = document.getElementById('domain').value;
        const skillLevelVal = document.querySelector('input[name="skill-level"]:checked').value;
        const timeAvailableVal = parseInt(document.querySelector('input[name="time-available"]:checked').value, 10);

        const payload = {
            domain: domainVal,
            skill_level: skillLevelVal,
            time_available: timeAvailableVal
        };

        try {
            // 3. Post to API
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const detailedError = errorData.detail && typeof errorData.detail === 'object'
                    ? errorData.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join(', ')
                    : errorData.detail || `Server returned code ${response.status}`;
                throw new Error(detailedError);
            }

            const data = await response.json();

            if (!data.ideas || !Array.isArray(data.ideas) || data.ideas.length === 0) {
                throw new Error("Received empty or invalid data format from the generator API.");
            }

            // 4. Update local cache & Render results
            generatedIdeasCache = data.ideas;
            renderResults(data);

        } catch (err) {
            console.error('Error generating ideas:', err);
            errorMessage.textContent = err.message || 'Unable to connect to the FastAPI backend. Check that your uvicorn server is running on http://127.0.0.1:8000';
            errorBox.classList.remove('hidden');
            errorBox.scrollIntoView({ behavior: 'smooth' });
        } finally {
            // 5. Reset states
            loader.classList.add('hidden');
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').textContent = 'Forge Ideas';
        }
    });

    // Helper to categorize technology tags for custom color gradients
    function getTechCategory(tech) {
        const t = tech.toLowerCase();
        if (t.includes('python') || t.includes('numpy') || t.includes('pandas') || t.includes('pytorch') || 
            t.includes('tensorflow') || t.includes('llm') || t.includes('openai') || t.includes('gemini') || 
            t.includes('scikit') || t.includes('langchain') || t.includes('llama') || t.includes('bert') || 
            t.includes('ai') || t.includes('ml') || t.includes('claude') || t.includes('hugging')) {
            return 'ai';
        }
        if (t.includes('react') || t.includes('next.js') || t.includes('vue') || t.includes('svelte') || 
            t.includes('html') || t.includes('css') || t.includes('javascript') || t.includes('typescript') || 
            t.includes('frontend') || t.includes('tailwind') || t.includes('bootstrap') || t.includes('express') ||
            t.includes('fastapi') || t.includes('django') || t.includes('flask') || t.includes('node')) {
            return 'web';
        }
        if (t.includes('postgres') || t.includes('mongodb') || t.includes('mysql') || t.includes('redis') || 
            t.includes('sqlite') || t.includes('sql') || t.includes('prisma') || t.includes('database') || 
            t.includes('db') || t.includes('supabase') || t.includes('firebase')) {
            return 'db';
        }
        return 'sys'; // systems, devops, scripts, default
    }

    // Helper to return clean vector icons based on technology name
    function getTechIconSvg(tech) {
        const lower = tech.toLowerCase();
        
        // 1. AI & LLMs (Sparkles / Star)
        if (lower.includes('gemini') || lower.includes('openai') || lower.includes('anthropic') || 
            lower.includes('llm') || lower.includes('langchain') || lower.includes('hugging') || 
            lower.includes('ai') || lower.includes('ml') || lower.includes('llama') || lower.includes('claude')) {
            return `
                <svg class="pill-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"></path>
                </svg>
            `;
        }
        
        // 2. FastAPI, backend frameworks (Lightning bolt for speed/performance)
        if (lower.includes('fastapi') || lower.includes('python') || lower.includes('flask') || 
            lower.includes('django') || lower.includes('express') || lower.includes('node')) {
            return `
                <svg class="pill-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                </svg>
            `;
        }
        
        // 3. Frontend frameworks & Libraries (Monitor/Screen for UI/Web layout)
        if (lower.includes('react') || lower.includes('next') || lower.includes('vue') || 
            lower.includes('svelte') || lower.includes('tailwind') || lower.includes('bootstrap') || 
            lower.includes('html') || lower.includes('css') || lower.includes('javascript') || lower.includes('typescript')) {
            return `
                <svg class="pill-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                    <line x1="8" y1="21" x2="16" y2="21"></line>
                    <line x1="12" y1="17" x2="12" y2="21"></line>
                </svg>
            `;
        }
        
        // 4. Data frameworks (Pandas, NumPy, Scikit - analytics grid/bars)
        if (lower.includes('pandas') || lower.includes('numpy') || lower.includes('scikit') || 
            lower.includes('tensor') || lower.includes('torch') || lower.includes('data') || lower.includes('plot')) {
            return `
                <svg class="pill-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="20" x2="18" y2="10"></line>
                    <line x1="12" y1="20" x2="12" y2="4"></line>
                    <line x1="6" y1="20" x2="6" y2="14"></line>
                </svg>
            `;
        }
        
        // 5. Databases & Storage (Cylinder)
        if (lower.includes('postgres') || lower.includes('mongo') || lower.includes('sql') || 
            lower.includes('pinecone') || lower.includes('chroma') || lower.includes('db') || 
            lower.includes('redis') || lower.includes('supabase') || lower.includes('firebase')) {
            return `
                <svg class="pill-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
                    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
                    <path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"></path>
                </svg>
            `;
        }
        
        // 6. Default Fallback (Code brackets </>)
        return `
            <svg class="pill-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="16 18 22 12 16 6"></polyline>
                <polyline points="8 6 2 12 8 18"></polyline>
            </svg>
        `;
    }

    // Populate and render results section
    function renderResults(data) {
        let cardsHTML = '';
        const bestIndex = data.best_idea_index !== undefined ? data.best_idea_index : 0;
        
        // Render Mentor Pick explanation
        if (data.ranking_reason) {
            rankingReason.textContent = data.ranking_reason;
            document.querySelector('.mentor-pick-container').classList.remove('hidden');
        } else {
            document.querySelector('.mentor-pick-container').classList.add('hidden');
        }

        // Generate card layout dynamically
        data.ideas.forEach((idea, index) => {
            const isBest = index === bestIndex;
            const cardType = ideaTypeLabels[index] || "Project Idea";

            const techPills = idea.tech_stack.map(tech => `
                <span class="tech-tag tech-${getTechCategory(tech)}">
                    ${getTechIconSvg(tech)}
                    <span>${escapeHtml(tech)}</span>
                </span>
            `).join('');

            cardsHTML += `
                <div class="idea-card ${isBest ? 'best-card' : ''}" data-index="${index}" style="animation-delay: ${index * 100}ms">
                    ${isBest ? `
                        <div class="card-pick-badge">
                            <svg class="badge-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path>
                                <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path>
                                <path d="M4 22h16"></path>
                                <path d="M10 14.66V17c0 .55-.45 1-1 1H4v2h16v-2h-5c-.55 0-1-.45-1-1v-2.34"></path>
                                <path d="M12 2a5 5 0 0 0-5 5v3c0 2.2 1.8 4 4 4h2c2.2 0 4-1.8 4-4V7a5 5 0 0 0-5-5z"></path>
                            </svg>
                            <span>Mentor Pick</span>
                        </div>
                    ` : ''}
                    <div class="idea-type-label">${escapeHtml(cardType)}</div>
                    <h3>${escapeHtml(idea.title)}</h3>
                    <p class="desc">${escapeHtml(idea.description)}</p>
                    
                    <div class="tech-list">
                        ${techPills}
                    </div>

                    <div class="card-action-hint">
                        <span>Explore roadmap & metrics</span>
                        <svg class="arrow-right-svg" viewBox="0 0 24 24">
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <polyline points="12 5 19 12 12 19"></polyline>
                        </svg>
                    </div>
                </div>
            `;
        });
        
        ideasGrid.innerHTML = cardsHTML;

        // Toggle results visibility
        resultsSection.classList.remove('hidden');

        // Scroll down
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        // Re-attach card click triggers and cursor spotlight listeners
        const cards = document.querySelectorAll('.idea-card');
        cards.forEach(card => {
            card.addEventListener('click', (e) => {
                // Ensure clicks on individual interactive elements don't double fire
                if (e.target.closest('.tech-tag')) return;
                const index = parseInt(card.getAttribute('data-index'), 10);
                openDetailsModal(index);
            });

            // Tracking mouse position for cursor-following radial spotlight glow
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });
        });
    }

    // Modal popup control logic
    function openDetailsModal(index) {
        const idea = generatedIdeasCache[index];
        if (!idea) return;

        const cardType = ideaTypeLabels[index] || "Project Idea";
        activeIdeaIndex = index; // Store globally for copy command reference

        // Set static texts
        modalTitle.textContent = idea.title;
        modalDesc.textContent = idea.description;
        modalType.textContent = cardType;
        
        modalTechList.innerHTML = idea.tech_stack.map(tech => `
            <span class="tech-tag tech-${getTechCategory(tech)}">
                ${getTechIconSvg(tech)}
                <span>${escapeHtml(tech)}</span>
            </span>
        `).join('');

        // Full roadmap list mapping with interactive checklist inputs
        modalRoadmapList.innerHTML = idea.roadmap.map((step, idx) => `
            <li class="roadmap-item">
                <label class="checkbox-wrapper">
                    <input type="checkbox" class="roadmap-checkbox" data-index="${idx}">
                    <span class="custom-checkbox" data-step="${idx + 1}"></span>
                </label>
                <span class="roadmap-text">${escapeHtml(step)}</span>
            </li>
        `).join('');

        // Reset progress bar to 0% initially
        updateRoadmapProgress(0, idea.roadmap.length);

        // Bind checklist checkbox change handlers
        const checkboxes = modalRoadmapList.querySelectorAll('.roadmap-checkbox');
        checkboxes.forEach(cb => {
            cb.addEventListener('change', () => {
                const checkedCount = modalRoadmapList.querySelectorAll('.roadmap-checkbox:checked').length;
                updateRoadmapProgress(checkedCount, idea.roadmap.length);
            });
        });

        // Score numbers
        modalComplexityVal.textContent = `${idea.complexity_score}/10`;
        modalImpactVal.textContent = `${idea.impact_score}/10`;

        // Initialize score bar width animations to 0% first
        modalComplexityBar.style.width = '0%';
        modalImpactBar.style.width = '0%';

        // Display Modal Overlay
        detailsModal.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Lock body scroll

        // Slide width animations in
        setTimeout(() => {
            modalComplexityBar.style.width = `${idea.complexity_score * 10}%`;
            modalImpactBar.style.width = `${idea.impact_score * 10}%`;
        }, 50);
    }

    // Update dynamic progress tracker bar and state percentage
    function updateRoadmapProgress(checkedCount, total) {
        const percent = total > 0 ? Math.round((checkedCount / total) * 100) : 0;
        const progressPercent = document.getElementById('modal-progress-percent');
        const progressBar = document.getElementById('modal-progress-bar');
        
        if (progressPercent) {
            progressPercent.textContent = `${percent}% Completed (${checkedCount}/${total})`;
        }
        if (progressBar) {
            progressBar.style.width = `${percent}%`;
        }
    }

    function closeDetailsModal() {
        detailsModal.classList.add('hidden');
        document.body.style.overflow = ''; // Unlock body scroll
    }

    // Modal close triggers
    if (modalClose) {
        modalClose.addEventListener('click', closeDetailsModal);
    }

    if (detailsModal) {
        detailsModal.addEventListener('click', (e) => {
            // Close only if clicking outside the card itself
            if (e.target === detailsModal) {
                closeDetailsModal();
            }
        });
    }

    // Close modal on Escape key press
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !detailsModal.classList.contains('hidden')) {
            closeDetailsModal();
        }
    });

    // Copy markdown button click listener
    const modalCopyBtn = document.getElementById('modal-copy-btn');
    if (modalCopyBtn) {
        modalCopyBtn.addEventListener('click', () => {
            if (activeIdeaIndex === -1 || !generatedIdeasCache[activeIdeaIndex]) return;
            const idea = generatedIdeasCache[activeIdeaIndex];
            const cardType = ideaTypeLabels[activeIdeaIndex] || "Project Idea";

            // Format markdown text
            let markdown = `# ${idea.title}\n\n`;
            markdown += `**Category**: ${cardType}\n`;
            markdown += `**Description**: ${idea.description}\n\n`;
            markdown += `## 🛠️ Technology Stack\n`;
            idea.tech_stack.forEach(tech => {
                markdown += `- ${tech}\n`;
            });
            markdown += `\n`;
            markdown += `## 📊 Judge Scores\n`;
            markdown += `- Complexity Score: ${idea.complexity_score}/10\n`;
            markdown += `- Demo Impact Score: ${idea.impact_score}/10\n\n`;
            markdown += `## 📋 Implementation Roadmap\n`;
            
            // Collect checked statuses from active checkboxes in modal
            const cbElements = modalRoadmapList.querySelectorAll('.roadmap-checkbox');
            idea.roadmap.forEach((step, idx) => {
                const isChecked = cbElements[idx] && cbElements[idx].checked;
                markdown += `- [${isChecked ? 'x' : ' '}] ${step}\n`;
            });

            // Copy to clipboard
            navigator.clipboard.writeText(markdown).then(() => {
                // Show success status on button
                modalCopyBtn.classList.add('copied');
                const btnTextEl = modalCopyBtn.querySelector('.copy-btn-text');
                if (btnTextEl) {
                    btnTextEl.textContent = 'Copied!';
                }

                // Show toast notification
                showToast('Project details copied as Markdown!', 'success');

                // Reset button text after 2 seconds
                setTimeout(() => {
                    modalCopyBtn.classList.remove('copied');
                    if (btnTextEl) {
                        btnTextEl.textContent = 'Copy Markdown';
                    }
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                showToast('Copy failed. Please try again.', 'error');
            });
        });
    }

    // Toast Notification utility
    function showToast(message, type = 'success') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let iconHTML = '';
        if (type === 'success') {
            iconHTML = `
                <svg class="toast-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
            `;
        } else {
            iconHTML = `
                <svg class="toast-icon-svg toast-error-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
            `;
        }

        toast.innerHTML = `${iconHTML}<span>${message}</span>`;
        container.appendChild(toast);

        // Trigger animation
        setTimeout(() => {
            toast.classList.add('show');
        }, 10);

        // Dismiss after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 400);
        }, 3000);
    }

    // Helper function to escape text parameters
    function escapeHtml(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Floating Back to Top Button Logic
    const backToTopBtn = document.getElementById('back-to-top');
    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });

        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});
