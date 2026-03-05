/**
 * UI Controller — Fetches data from the live API and renders results.
 * All text is 100% grounded in API response data (zero hallucination).
 */

const API_BASE = 'http://localhost:8002';
const API_KEY = 'password';

// ── DOM Refs ──────────────────────────────────────────────────
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const loadingEl = document.getElementById('loading-section');
const resultsEl = document.getElementById('results-panel');
const productIdEl = document.getElementById('result-product-id');
const reviewCountEl = document.getElementById('result-review-count');
const confidenceEl = document.getElementById('confidence-badge');
const aspectsRowEl = document.getElementById('aspects-row');
const prosListEl = document.getElementById('pros-list');
const consListEl = document.getElementById('cons-list');
const summaryTextEl = document.getElementById('summary-text');
const summaryCardEl = document.getElementById('summary-card');


// ── Init ──────────────────────────────────────────────────────
export function initUI() {
    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') handleSearch();
    });
}


// ── Search Handler ────────────────────────────────────────────
async function handleSearch() {
    const productId = searchInput.value.trim();
    if (!productId) {
        searchInput.focus();
        return;
    }

    // Show loading
    resultsEl.style.display = 'none';
    loadingEl.style.display = 'block';

    try {
        const res = await fetch(`${API_BASE}/api/v1/insights/${productId}`, {
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Accept': 'application/json',
            },
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.message || `Error ${res.status}`);
        }

        const data = await res.json();
        renderResults(data);
    } catch (err) {
        loadingEl.style.display = 'none';
        alert(`⚠️ ${err.message}`);
    }
}


// ── Render ────────────────────────────────────────────────────
function renderResults(data) {
    loadingEl.style.display = 'none';
    resultsEl.style.display = 'block';

    // Header
    productIdEl.textContent = data.product_id;
    reviewCountEl.textContent = data.review_count.toLocaleString();

    // Confidence
    const confPercent = Math.round(data.confidence * 100);
    confidenceEl.textContent = `${confPercent}% Confidence`;
    confidenceEl.style.color = confPercent >= 80
        ? 'var(--accent-green)'
        : confPercent >= 50
            ? '#f59e0b'
            : 'var(--accent-red)';
    confidenceEl.style.borderColor = confidenceEl.style.color;
    confidenceEl.style.background = confPercent >= 80
        ? 'rgba(34,197,94,0.12)'
        : confPercent >= 50
            ? 'rgba(245,158,11,0.12)'
            : 'rgba(239,68,68,0.12)';

    // Aspects
    aspectsRowEl.innerHTML = '';
    (data.top_aspects || []).forEach((a) => {
        const tag = document.createElement('span');
        tag.className = `aspect-tag ${a.sentiment}`;
        tag.textContent = `${a.aspect}  (${a.score > 0 ? '+' : ''}${a.score.toFixed(2)})`;
        aspectsRowEl.appendChild(tag);
    });

    // Pros
    prosListEl.innerHTML = '';
    if (data.pros && data.pros.length) {
        data.pros.forEach((p) => {
            prosListEl.appendChild(createEvidenceCard(p, 'pro'));
        });
    } else {
        prosListEl.innerHTML = '<p class="no-data">No strengths detected</p>';
    }

    // Cons
    consListEl.innerHTML = '';
    if (data.cons && data.cons.length) {
        data.cons.forEach((c) => {
            consListEl.appendChild(createEvidenceCard(c, 'con'));
        });
    } else {
        consListEl.innerHTML = '<p class="no-data">No weaknesses detected</p>';
    }

    // Summary
    if (data.summary) {
        summaryCardEl.style.display = 'block';
        summaryTextEl.textContent = data.summary;
    } else {
        summaryCardEl.style.display = 'none';
    }

    // Smooth scroll to results
    resultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
}


// ── Evidence Card Builder ─────────────────────────────────────
function createEvidenceCard(item, type) {
    const card = document.createElement('div');
    card.className = `evidence-card ${type}`;

    const point = document.createElement('div');
    point.className = 'evidence-point';
    point.textContent = item.point;

    const quote = document.createElement('div');
    quote.className = 'evidence-quote';
    quote.textContent = item.evidence;

    const source = document.createElement('div');
    source.className = 'evidence-source';
    source.textContent = `Review ID: ${item.review_id}`;

    card.appendChild(point);
    card.appendChild(quote);
    card.appendChild(source);
    return card;
}
