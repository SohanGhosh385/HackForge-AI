document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('idea-form');
    const submitBtn = document.getElementById('submit-btn');
    const loader = document.getElementById('loader');
    const resultsSection = document.getElementById('results');
    const errorBox = document.getElementById('error-box');
    const errorMessage = document.getElementById('error-message');
    const ideasGrid = document.getElementById('ideas-grid');
    const rankingReason = document.getElementById('ranking-reason');

    const API_URL = 'http://127.0.0.1:8000/generate-ideas';

    // Categories mapping to match different type rules
    const ideaTypeLabels = [
        "AI-Centric Solution",
        "Web/App Platform",
        "Automation & System Tool"
    ];

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. Reset States
        errorBox.classList.add('hidden');
        resultsSection.classList.add('hidden');
        loader.classList.remove('hidden');
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = 'Forging Ideas...';

        // 2. Extract input values
        const domainVal = document.getElementById('domain').value;
        const skillLevelVal = document.getElementById('skill-level').value;
        const timeAvailableVal = parseInt(document.getElementById('time-available').value, 10);

        const payload = {
            domain: domainVal,
            skill_level: skillLevelVal,
            time_available: timeAvailableVal
        };

        try {
            // 3. API Call
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                // Read validation error details if available
                const errorData = await response.json().catch(() => ({}));
                const detailedError = errorData.detail && typeof errorData.detail === 'object'
                    ? errorData.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join(', ')
                    : errorData.detail || `Server returned status ${response.status}`;
                throw new Error(detailedError);
            }

            const data = await response.json();

            // Validate structured output structure
            if (!data.ideas || !Array.isArray(data.ideas) || data.ideas.length === 0) {
                throw new Error("Received malformed response data format from server.");
            }

            // 4. Render Results
            renderResults(data);

        } catch (err) {
            console.error('Error generating ideas:', err);
            // Display error box
            errorMessage.textContent = err.message || 'Unable to communicate with the FastAPI backend. Make sure the server is running on http://127.0.0.1:8000';
            errorBox.classList.remove('hidden');
            // Scroll to error box
            errorBox.scrollIntoView({ behavior: 'smooth' });
        } finally {
            // 5. Reset Loader State
            loader.classList.add('hidden');
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').textContent = 'Forge Hackathon Ideas';
        }
    });

    function renderResults(data) {
        // Clear previous grid cards
        ideasGrid.innerHTML = '';

        const bestIndex = data.best_idea_index !== undefined ? data.best_idea_index : 0;
        
        // Render Mentor Pick Section
        if (data.ranking_reason) {
            rankingReason.textContent = data.ranking_reason;
            document.querySelector('.mentor-pick-container').classList.remove('hidden');
        } else {
            document.querySelector('.mentor-pick-container').classList.add('hidden');
        }

        // Generate Cards
        data.ideas.forEach((idea, index) => {
            const isBest = index === bestIndex;
            const cardType = ideaTypeLabels[index] || "Hackathon Project";

            // Create list elements for tech stack
            const techPills = idea.tech_stack.map(tech => `<span class="tech-tag">${escapeHtml(tech)}</span>`).join('');

            // Create list items for roadmap milestones
            const roadmapItems = idea.roadmap.map((step, stepIdx) => `
                <li data-step="${stepIdx + 1}">${escapeHtml(step)}</li>
            `).join('');

            // Card HTML template
            const cardHTML = `
                <div class="idea-card ${isBest ? 'best-card' : ''}" style="animation-delay: ${index * 100}ms">
                    ${isBest ? '<div class="card-pick-badge">Best Pick</div>' : ''}
                    <div class="idea-type-label">${escapeHtml(cardType)}</div>
                    <h2>${escapeHtml(idea.title)}</h2>
                    <p class="desc">${escapeHtml(idea.description)}</p>
                    
                    <div class="tech-list">
                        ${techPills}
                    </div>

                    <div class="roadmap-section">
                        <h4>Demo Roadmap</h4>
                        <ol class="roadmap-steps">
                            ${roadmapItems}
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

        // Toggle results section display
        resultsSection.classList.remove('hidden');

        // Trigger dynamic transition width sliders after browser rendering
        setTimeout(() => {
            document.querySelectorAll('.meter-bar-inner').forEach(bar => {
                const score = parseInt(bar.getAttribute('data-score'), 10) || 0;
                bar.style.width = `${Math.min(100, Math.max(0, score * 10))}%`;
            });
        }, 100);

        // Smooth scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Secure helper to escape raw HTML text injections
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
