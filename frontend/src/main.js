/**
 * Application bootstrap — wires up Three.js scene and UI overlay.
 */
import './style.css';
import { initScene } from './scene.js';
import { initUI } from './ui.js';

// ── Boot ───────────────────────────────────────────────────────
const canvas = document.getElementById('three-canvas');
initScene(canvas);
initUI();
