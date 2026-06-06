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

    // Sync domain select dropdown to domain input field
    const domainInput = document.getElementById('domain');
    const domainSelect = document.getElementById('domain-select');
    
    if (domainSelect && domainInput) {
        domainSelect.addEventListener('change', () => {
            domainInput.value = domainSelect.value;
        });
    }

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
        const skillLevelVal = document.getElementById('skill-level').value;
        const timeAvailableVal = parseInt(document.getElementById('time-available').value, 10);

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

    // Populate and render results section
    function renderResults(data) {
        ideasGrid.innerHTML = '';
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

            const techPills = idea.tech_stack.map(tech => `<span class="tech-tag">${escapeHtml(tech)}</span>`).join('');

            // Minimal roadmap representation for the card itself
            const miniRoadmap = idea.roadmap.slice(0, 2).map((step, stepIdx) => `
                <li data-step="${stepIdx + 1}">${escapeHtml(step)}</li>
            `).join('');
            
            const cardHTML = `
                <div class="idea-card ${isBest ? 'best-card' : ''}" data-index="${index}" style="animation-delay: ${index * 100}ms">
                    ${isBest ? '<div class="card-pick-badge">🏆 Mentor Pick</div>' : ''}
                    <div class="idea-type-label">${escapeHtml(cardType)}</div>
                    <h3>${escapeHtml(idea.title)}</h3>
                    <p class="desc">${escapeHtml(idea.description)}</p>
                    
                    <div class="tech-list">
                        ${techPills}
                    </div>

                    <div class="roadmap-section">
                        <h4>Demo Preview</h4>
                        <ol class="roadmap-steps">
                            ${miniRoadmap}
                            ${idea.roadmap.length > 2 ? `<li class="more-steps" style="list-style: none; padding-left: 0; font-size: 0.8rem; color: var(--color-accent); font-weight: 600; margin-top: 5px;">+ Click card to see full roadmap</li>` : ''}
                        </ol>
                    </div>

                    <div class="score-meters">
                        <div class="meter-group">
                            <div class="meter-label-row">
                                <span>Complexity Level</span>
                                <span class="meter-val">${idea.complexity_score}/10</span>
                            </div>
                            <div class="meter-bar-outer">
                                <div class="meter-bar-inner complexity-bar" data-score="${idea.complexity_score}"></div>
                            </div>
                        </div>
                        <div class="meter-group">
                            <div class="meter-label-row">
                                <span>Demo Impact</span>
                                <span class="meter-val">${idea.impact_score}/10</span>
                            </div>
                            <div class="meter-bar-outer">
                                <div class="meter-bar-inner impact-bar" data-score="${idea.impact_score}"></div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            ideasGrid.insertAdjacentHTML('beforeend', cardHTML);
        });

        // Toggle results visibility
        resultsSection.classList.remove('hidden');

        // Apply slide transition for values
        setTimeout(() => {
            document.querySelectorAll('.meter-bar-inner').forEach(bar => {
                const score = parseInt(bar.getAttribute('data-score'), 10) || 0;
                bar.style.width = `${Math.min(100, Math.max(0, score * 10))}%`;
            });
        }, 100);

        // Scroll down
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        // Re-attach card click triggers for detailed modal lookup
        document.querySelectorAll('.idea-card').forEach(card => {
            card.addEventListener('click', (e) => {
                // Avoid trigger if clicking individual tag links or buttons directly (if any)
                const index = parseInt(card.getAttribute('data-index'), 10);
                openDetailsModal(index);
            });
        });
    }

    // Modal popup control logic
    function openDetailsModal(index) {
        const idea = generatedIdeasCache[index];
        if (!idea) return;

        const cardType = ideaTypeLabels[index] || "Project Idea";

        // Set static texts
        modalTitle.textContent = idea.title;
        modalDesc.textContent = idea.description;
        modalType.textContent = cardType;
        
        // Dynamic tech tags
        modalTechList.innerHTML = idea.tech_stack.map(tech => `
            <span class="tech-tag">${escapeHtml(tech)}</span>
        `).join('');

        // Full roadmap list mapping
        modalRoadmapList.innerHTML = idea.roadmap.map((step, idx) => `
            <li data-step="${idx + 1}">${escapeHtml(step)}</li>
        `).join('');

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
});
