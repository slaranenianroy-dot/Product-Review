/**
 * Three.js 3D Background Scene
 * 
 * Creates a cinematic backdrop with:
 *  - Floating product box geometries with glow edges
 *  - Starfield particle system
 *  - Ambient + point lighting with cyan/purple tones
 *  - Slow orbital camera drift for 60fps immersion
 */
import * as THREE from 'three';

// ── State ──────────────────────────────────────────────────────
let scene, camera, renderer;
let particles, boxes = [];
let clock;
let mouseX = 0, mouseY = 0;

// ── Initialise ─────────────────────────────────────────────────
export function initScene(canvas) {
  clock = new THREE.Clock();

  // Scene
  scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x050510, 0.035);

  // Camera
  camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.set(0, 0, 30);

  // Renderer
  renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x050510, 1);

  // ── Lights ─────────────────────────────────────────────────
  const ambientLight = new THREE.AmbientLight(0x1a1a3e, 0.6);
  scene.add(ambientLight);

  const cyanPoint = new THREE.PointLight(0x00d4ff, 1.5, 80);
  cyanPoint.position.set(-15, 10, 20);
  scene.add(cyanPoint);

  const purplePoint = new THREE.PointLight(0x7c3aed, 1.2, 80);
  purplePoint.position.set(15, -8, 15);
  scene.add(purplePoint);

  const warmPoint = new THREE.PointLight(0xff6b35, 0.4, 60);
  warmPoint.position.set(0, 15, 10);
  scene.add(warmPoint);

  // ── Particle Starfield ─────────────────────────────────────
  createParticles();

  // ── Floating Product Boxes ─────────────────────────────────
  createBoxes();

  // ── Events ─────────────────────────────────────────────────
  window.addEventListener('resize', onResize);
  window.addEventListener('mousemove', onMouseMove);

  // ── Start ──────────────────────────────────────────────────
  animate();
}


// ── Particle System ────────────────────────────────────────────
function createParticles() {
  const count = 2000;
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(count * 3);
  const sizes = new Float32Array(count);

  for (let i = 0; i < count; i++) {
    positions[i * 3]     = (Math.random() - 0.5) * 120;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 120;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 120;
    sizes[i] = Math.random() * 2 + 0.3;
  }

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

  const material = new THREE.PointsMaterial({
    color: 0x4488cc,
    size: 0.12,
    transparent: true,
    opacity: 0.6,
    sizeAttenuation: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });

  particles = new THREE.Points(geometry, material);
  scene.add(particles);
}


// ── Floating Boxes ─────────────────────────────────────────────
function createBoxes() {
  const boxGeometry = new THREE.BoxGeometry(1, 1.4, 0.15);

  for (let i = 0; i < 18; i++) {
    // Face material: dark translucent
    const faceMaterial = new THREE.MeshPhysicalMaterial({
      color: 0x0f0f2e,
      metalness: 0.3,
      roughness: 0.5,
      transparent: true,
      opacity: 0.35,
      side: THREE.DoubleSide,
    });

    // Edge lines for glow effect
    const edgesGeo = new THREE.EdgesGeometry(boxGeometry);
    const edgeMaterial = new THREE.LineBasicMaterial({
      color: i % 3 === 0 ? 0x00d4ff : (i % 3 === 1 ? 0x7c3aed : 0x22c55e),
      transparent: true,
      opacity: 0.35,
    });

    const mesh = new THREE.Mesh(boxGeometry, faceMaterial);
    const edges = new THREE.LineSegments(edgesGeo, edgeMaterial);
    mesh.add(edges);

    // Random position
    mesh.position.set(
      (Math.random() - 0.5) * 50,
      (Math.random() - 0.5) * 40,
      (Math.random() - 0.5) * 30 - 10
    );

    // Random rotation
    mesh.rotation.set(
      Math.random() * Math.PI,
      Math.random() * Math.PI,
      Math.random() * Math.PI
    );

    // Store animation data
    mesh.userData = {
      rotSpeed: {
        x: (Math.random() - 0.5) * 0.005,
        y: (Math.random() - 0.5) * 0.005,
        z: (Math.random() - 0.5) * 0.003,
      },
      floatOffset: Math.random() * Math.PI * 2,
      floatSpeed: 0.3 + Math.random() * 0.4,
      floatAmplitude: 0.3 + Math.random() * 0.5,
      baseY: mesh.position.y,
    };

    const scale = 0.8 + Math.random() * 1.8;
    mesh.scale.set(scale, scale, scale);

    scene.add(mesh);
    boxes.push(mesh);
  }
}


// ── Animation Loop ─────────────────────────────────────────────
function animate() {
  requestAnimationFrame(animate);

  const elapsed = clock.getElapsedTime();

  // Rotate particles slowly
  particles.rotation.y = elapsed * 0.02;
  particles.rotation.x = elapsed * 0.008;

  // Animate boxes
  boxes.forEach((box) => {
    const d = box.userData;
    box.rotation.x += d.rotSpeed.x;
    box.rotation.y += d.rotSpeed.y;
    box.rotation.z += d.rotSpeed.z;
    box.position.y = d.baseY + Math.sin(elapsed * d.floatSpeed + d.floatOffset) * d.floatAmplitude;
  });

  // Subtle camera follow mouse
  const targetX = mouseX * 0.002;
  const targetY = -mouseY * 0.002;
  camera.position.x += (targetX - camera.position.x) * 0.02;
  camera.position.y += (targetY - camera.position.y) * 0.02;
  camera.lookAt(0, 0, 0);

  renderer.render(scene, camera);
}


// ── Events ─────────────────────────────────────────────────────
function onResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

function onMouseMove(e) {
  mouseX = e.clientX - window.innerWidth / 2;
  mouseY = e.clientY - window.innerHeight / 2;
}
