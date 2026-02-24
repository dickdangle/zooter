<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ex‑Machina Brain‑Interface Visualizer (Three.js)</title>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        #info {
            position: absolute;
            top: 20px;
            left: 20px;
            color: white;
            background: rgba(0,0,0,0.6);
            padding: 10px 20px;
            border-radius: 30px;
            pointer-events: none;
            z-index: 10;
            backdrop-filter: blur(5px);
            border: 1px solid #00ffff33;
        }
        #time-slider-container {
            position: absolute;
            bottom: 40px;
            left: 20%;
            width: 60%;
            background: rgba(0,0,0,0.7);
            padding: 15px 25px;
            border-radius: 50px;
            backdrop-filter: blur(8px);
            border: 1px solid #aa88ff;
            box-shadow: 0 0 30px rgba(170,136,255,0.3);
            color: white;
            display: flex;
            align-items: center;
            gap: 20px;
            z-index: 20;
        }
        #time-slider {
            flex: 1;
            height: 6px;
            -webkit-appearance: none;
            background: linear-gradient(90deg, #ff3366, #ffaa00, #33ccff);
            border-radius: 3px;
            outline: none;
        }
        #time-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 22px;
            height: 22px;
            background: white;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 0 20px #ffffffaa;
            border: 2px solid #aa88ff;
        }
        #time-label {
            font-family: monospace;
            font-size: 1.2rem;
            min-width: 70px;
            text-align: center;
            color: #ccddff;
            text-shadow: 0 0 10px #88aaff;
        }
        .legend {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(10,10,20,0.8);
            padding: 15px;
            border-radius: 16px;
            color: #eee;
            border-left: 4px solid #aa88ff;
            backdrop-filter: blur(4px);
            font-size: 0.9rem;
            z-index: 15;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin: 8px 0;
        }
        .color-dot {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            margin-right: 10px;
            box-shadow: 0 0 10px currentColor;
        }
    </style>
</head>
<body>
    <div id="info">🧠 EX‑MACHINA BRAIN‑INTERFACE LOG VISUALIZER • L0 (high entropy) ⟷ L9 (core)</div>
    <div class="legend">
        <div style="margin-bottom:12px; font-weight:bold; text-align:center; color:#ccddff;">◈ LAYERS ◈</div>
        <div class="legend-item"><span class="color-dot" style="background:#ff3366; box-shadow:0 0 15px #ff3366;"></span> L0–L2 : volatile, high entropy</div>
        <div class="legend-item"><span class="color-dot" style="background:#ffaa00;"></span> L3–L5 : transitional</div>
        <div class="legend-item"><span class="color-dot" style="background:#33ccff;"></span> L6–L8 : stable</div>
        <div class="legend-item"><span class="color-dot" style="background:#aa88ff; box-shadow:0 0 15px #aa88ff;"></span> L9 core : permanent</div>
        <div class="legend-item"><span style="margin-right:10px;">⚡</span> Ghosts : past states</div>
        <div class="legend-item"><span style="margin-right:10px;">🌀</span> Arcs : transformations</div>
    </div>
    <div id="time-slider-container">
        <span style="color:#99aaff;">⏮</span>
        <input type="range" id="time-slider" min="0" max="100" value="100" step="1">
        <span id="time-label">t: 1.00</span>
        <span style="color:#99aaff;">⏭</span>
    </div>

    <!-- Import Three.js and add-ons -->
    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.128.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.128.0/examples/jsm/"
            }
        }
    </script>

    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
        import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

        // --- Setup scene, camera, renderers ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a20); // deep space
        
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(25, 15, 30);
        camera.lookAt(0, 0, 0);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.shadowMap.enabled = false; // not needed
        renderer.toneMapping = THREE.ReinhardToneMapping;
        renderer.toneMappingExposure = 1.2;
        document.body.appendChild(renderer.domElement);

        // CSS2 renderer for labels
        const labelRenderer = new CSS2DRenderer();
        labelRenderer.setSize(window.innerWidth, window.innerHeight);
        labelRenderer.domElement.style.position = 'absolute';
        labelRenderer.domElement.style.top = '0px';
        labelRenderer.domElement.style.left = '0px';
        labelRenderer.domElement.style.pointerEvents = 'none'; // allow clicks to pass through
        document.body.appendChild(labelRenderer.domElement);

        // Controls
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.autoRotate = true;
        controls.autoRotateSpeed = 0.8;
        controls.enableZoom = true;
        controls.maxPolarAngle = Math.PI / 2; // restrict below to see layers

        // --- Lighting ---
        const ambientLight = new THREE.AmbientLight(0x404060);
        scene.add(ambientLight);
        
        const dirLight = new THREE.DirectionalLight(0xffffff, 1);
        dirLight.position.set(10, 20, 5);
        scene.add(dirLight);
        
        const pointLight = new THREE.PointLight(0xaa88ff, 1, 50);
        pointLight.position.set(0, 0, 0);
        scene.add(pointLight);

        // Add a subtle starfield background
        const starsGeometry = new THREE.BufferGeometry();
        const starsCount = 2000;
        const starPositions = new Float32Array(starsCount * 3);
        for (let i = 0; i < starsCount; i++) {
            const r = 80 + Math.random() * 40;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            starPositions[i*3] = r * Math.sin(phi) * Math.cos(theta);
            starPositions[i*3+1] = r * Math.sin(phi) * Math.sin(theta);
            starPositions[i*3+2] = r * Math.cos(phi);
        }
        starsGeometry.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
        const starsMaterial = new THREE.PointsMaterial({ color: 0x88aaff, size: 0.2, transparent: true, opacity: 0.6 });
        const stars = new THREE.Points(starsGeometry, starsMaterial);
        scene.add(stars);

        // --- Core (L9) glowing sphere ---
        const coreGeo = new THREE.SphereGeometry(1.8, 64, 64);
        const coreMat = new THREE.MeshStandardMaterial({ 
            color: 0xaa88ff, 
            emissive: 0x442288,
            roughness: 0.2,
            metalness: 0.8
        });
        const core = new THREE.Mesh(coreGeo, coreMat);
        scene.add(core);

        // Add a point light inside core to make it glow
        const coreLight = new THREE.PointLight(0xaa88ff, 2, 20);
        coreLight.position.set(0, 0, 0);
        scene.add(coreLight);

        // --- Layer shells L0 - L8 (transparent spheres) ---
        const layerColors = [0xff3366, 0xff5533, 0xff7733, 0xffaa00, 0xffcc00, 0x99cc33, 0x33cc99, 0x33ccff, 0x6688ff];
        const layerRadii = [10, 9, 8, 7, 6, 5, 4, 3, 2.2]; // L0 outermost, L8 just outside core
        const layers = [];
        for (let i = 0; i < 9; i++) {
            const radius = layerRadii[i];
            const geometry = new THREE.SphereGeometry(radius, 48, 32);
            const material = new THREE.MeshPhongMaterial({
                color: layerColors[i],
                transparent: true,
                opacity: 0.08,
                wireframe: true,
                emissive: 0x000000,
                side: THREE.DoubleSide
            });
            const sphere = new THREE.Mesh(geometry, material);
            scene.add(sphere);
            layers.push(sphere);
            
            // Add faint edge rings for definition
            const ringGeo = new THREE.TorusGeometry(radius, 0.03, 16, 100);
            const ringMat = new THREE.MeshStandardMaterial({ color: layerColors[i], emissive: layerColors[i], transparent: true, opacity: 0.15 });
            const ring = new THREE.Mesh(ringGeo, ringMat);
            ring.rotation.x = Math.PI / 2;
            scene.add(ring);
            
            // Add CSS2D label
            const div = document.createElement('div');
            div.textContent = `L${i}`;
            div.style.color = '#ffffff';
            div.style.fontSize = '18px';
            div.style.fontWeight = 'bold';
            div.style.textShadow = `0 0 15px ${new THREE.Color(layerColors[i]).getStyle()}`;
            div.style.background = 'rgba(20,20,40,0.6)';
            div.style.padding = '2px 10px';
            div.style.borderRadius = '20px';
            div.style.border = `1px solid ${new THREE.Color(layerColors[i]).getStyle()}`;
            div.style.backdropFilter = 'blur(2px)';
            
            const label = new CSS2DObject(div);
            label.position.set(radius * 0.7, radius * 0.7, 0); // place in first quadrant
            scene.add(label);
        }

        // --- Particles (SQDs) ---
        const PARTICLE_COUNT = 400;
        // Each particle: level (0-9), position, velocity, history array of positions
        const particles = [];
        
        // Geometry for current particle representation (small spheres)
        // We'll use instanced mesh for efficiency? But we need per-particle color based on level.
        // Simpler: create individual meshes (for clarity and ghosting). With 400 it's okay.
        // But we also need ghost trails, so we'll create separate ghost meshes.
        
        // Helper to get color from level
        function getColorFromLevel(level) {
            if (level < 3) return new THREE.Color(0xff3366);
            if (level < 6) return new THREE.Color(0xffaa00);
            if (level < 9) return new THREE.Color(0x33ccff);
            return new THREE.Color(0xaa88ff);
        }

        // Create particles
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            // Assign level biased towards outer layers? Let's random but with some distribution
            const level = Math.floor(Math.random() * 10); // 0-9
            const radiusBase = layerRadii[Math.min(level, 8)]; // L9 uses core radius 2, but we'll treat separately
            let radius;
            if (level === 9) {
                radius = 1.0 + Math.random() * 0.8; // inside core sphere
            } else {
                // Place within the shell of that layer: between previous layer radius and current?
                const outerR = layerRadii[level];
                const innerR = level === 0 ? 0 : layerRadii[level-1];
                radius = innerR + Math.random() * (outerR - innerR) * 0.9; // avoid edges
            }
            
            // Random direction
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            const pos = new THREE.Vector3(
                radius * Math.sin(phi) * Math.cos(theta),
                radius * Math.sin(phi) * Math.sin(theta),
                radius * Math.cos(phi)
            );
            
            // Create mesh
            const size = level === 9 ? 0.25 : 0.18;
            const geometry = new THREE.SphereGeometry(size, 16, 16);
            const material = new THREE.MeshStandardMaterial({
                color: getColorFromLevel(level),
                emissive: level === 9 ? 0x442288 : 0x000000,
                emissiveIntensity: level === 9 ? 0.8 : 0.2
            });
            const sphere = new THREE.Mesh(geometry, material);
            sphere.position.copy(pos);
            scene.add(sphere);
            
            // Store particle data
            particles.push({
                mesh: sphere,
                level: level,
                pos: pos.clone(),
                vel: new THREE.Vector3(
                    (Math.random() - 0.5) * 0.02,
                    (Math.random() - 0.5) * 0.02,
                    (Math.random() - 0.5) * 0.02
                ),
                history: [] // will store recent positions for ghosting
            });
        }

        // Create ghost particles (translucent copies) – we'll reuse the same geometry and update positions from history
        const GHOST_STEPS = 15; // number of past states to show
        const ghosts = [];
        for (let i = 0; i < GHOST_STEPS; i++) {
            for (let p = 0; p < particles.length; p++) {
                const particle = particles[p];
                const ghostGeo = new THREE.SphereGeometry(0.12, 8, 8);
                const ghostMat = new THREE.MeshStandardMaterial({
                    color: getColorFromLevel(particle.level),
                    transparent: true,
                    opacity: 0.15 * (1 - i / GHOST_STEPS), // fade older ghosts
                    emissive: 0x000000
                });
                const ghost = new THREE.Mesh(ghostGeo, ghostMat);
                scene.add(ghost);
                ghosts.push({
                    mesh: ghost,
                    particleIndex: p,
                    step: i
                });
            }
        }

        // --- Transformation arcs (random connections) ---
        const arcMaterial = new THREE.LineBasicMaterial({ color: 0x88aaff, transparent: true, opacity: 0.15 });
        const arcCount = 80;
        for (let i = 0; i < arcCount; i++) {
            const p1 = particles[Math.floor(Math.random() * particles.length)];
            const p2 = particles[Math.floor(Math.random() * particles.length)];
            if (p1 === p2) continue;
            
            // Create a simple quadratic bezier curve
            const start = p1.mesh.position.clone();
            const end = p2.mesh.position.clone();
            const mid = new THREE.Vector3().addVectors(start, end).multiplyScalar(0.5);
            // add some perpendicular offset
            const dir = new THREE.Vector3().subVectors(end, start).normalize();
            const perp = new THREE.Vector3(-dir.y, dir.x, dir.z).normalize();
            mid.addScaledVector(perp, (Math.random() - 0.5) * 3);
            
            const curve = new THREE.QuadraticBezierCurve3(start, mid, end);
            const points = curve.getPoints(30);
            const geometry = new THREE.BufferGeometry().setFromPoints(points);
            const line = new THREE.Line(geometry, arcMaterial);
            scene.add(line);
        }

        // --- History update and ghosting logic ---
        // We'll run a simple physics loop: particles attract to core, and also to others of similar level (clustering), plus random noise.
        // Also store history every frame.
        
        const clock = new THREE.Clock();
        
        // Time slider element
        const slider = document.getElementById('time-slider');
        const timeLabel = document.getElementById('time-label');
        let timeFactor = 1.0; // 1 = present, 0 = far past (we'll use it to blend ghost positions)
        
        slider.addEventListener('input', (e) => {
            timeFactor = e.target.value / 100;
            timeLabel.textContent = `t: ${timeFactor.toFixed(2)}`;
        });

        // Store position history for each particle (ring buffer)
        const MAX_HISTORY = 30;
        particles.forEach(p => p.history = []);

        // Helper to update ghost positions based on timeFactor
        function updateGhosts() {
            // timeFactor 1 -> show most recent history (index 0)
            // timeFactor 0 -> show oldest history (index MAX_HISTORY-1)
            // For simplicity, we map ghosts to steps: ghost step i (0 = newest) shows history index based on timeFactor
            // We'll just use the stored history per particle.
            
            ghosts.forEach(ghost => {
                const particle = particles[ghost.particleIndex];
                const history = particle.history;
                if (history.length === 0) return;
                
                // Map ghost.step (0=most recent) to history index
                // We want to show a slice of history centered around timeFactor.
                // Let's compute target history index: timeFactor maps to a continuous index.
                const maxIndex = history.length - 1;
                // ghost.step ranges 0..GHOST_STEPS-1, we want to offset relative to timeFactor.
                // e.g., if timeFactor = 1, ghost 0 gets index 0, ghost 1 gets index 1, ...
                // if timeFactor = 0, ghost 0 gets index maxIndex, ghost 1 gets maxIndex-1, ...
                const spread = GHOST_STEPS;
                const baseIndex = Math.round((1 - timeFactor) * maxIndex); // 0 at timeFactor=1, maxIndex at timeFactor=0
                // Now for ghost step i, we want index = baseIndex + i (but wrap around)
                let idx = baseIndex + ghost.step;
                if (idx > maxIndex) idx = maxIndex; // clamp
                // But we also want ghosts to be distributed around that point.
                // Simpler: use timeFactor directly to interpolate between history entries? We'll just show discrete.
                // For now, we'll just show history entry at index based on ghost.step and timeFactor.
                // Let's do: history index = floor( (1 - timeFactor) * maxIndex + ghost.step * (timeFactor/maxIndex) )? Too complex.
                // Let's just use timeFactor to blend between two history frames? Not necessary for demo.
                // I'll keep it simple: ghosts display a fixed set of past frames (last N), and timeFactor adjusts opacity? Or we shift which frames.
                // To match slider, we'll shift the whole ghost set: ghost with step i shows history entry at index (maxIndex - i) when timeFactor=1, and index i when timeFactor=0.
                // So linear mapping:
                const t = timeFactor;
                const idxNew = Math.floor( t * (maxIndex - ghost.step) + (1 - t) * ghost.step );
                // clamp
                const safeIdx = Math.min(maxIndex, Math.max(0, idxNew));
                if (history[safeIdx]) {
                    ghost.mesh.position.copy(history[safeIdx]);
                }
            });
        }

        // Animation loop
        function animate() {
            const delta = clock.getDelta();
            const time = performance.now() * 0.001; // seconds

            // Auto-rotate stars slowly
            stars.rotation.y += 0.0001;

            // Update particle positions (simple gravity and clustering)
            particles.forEach(p => {
                // Attraction to core (0,0,0)
                const toCore = new THREE.Vector3(0,0,0).sub(p.mesh.position).normalize().multiplyScalar(0.005);
                p.vel.add(toCore);
                
                // Repulsion from other particles (simple separation)
                particles.forEach(other => {
                    if (other === p) return;
                    const dist = p.mesh.position.distanceTo(other.mesh.position);
                    if (dist < 2.0) {
                        const away = new THREE.Vector3().subVectors(p.mesh.position, other.mesh.position).normalize().multiplyScalar(0.001 * (2.0 - dist));
                        p.vel.add(away);
                    }
                });

                // Attraction to particles of same level (clustering)
                particles.forEach(other => {
                    if (other === p || other.level !== p.level) return;
                    const dist = p.mesh.position.distanceTo(other.mesh.position);
                    if (dist > 0.5 && dist < 4.0) {
                        const towards = new THREE.Vector3().subVectors(other.mesh.position, p.mesh.position).normalize().multiplyScalar(0.002 * (4.0 - dist));
                        p.vel.add(towards);
                    }
                });

                // Random walk
                p.vel.x += (Math.random() - 0.5) * 0.003;
                p.vel.y += (Math.random() - 0.5) * 0.003;
                p.vel.z += (Math.random() - 0.5) * 0.003;

                // Damping
                p.vel.multiplyScalar(0.98);

                // Update position
                p.mesh.position.add(p.vel);

                // Keep within rough shell bounds? Not strictly necessary
            });

            // Store history (current positions) for each particle
            particles.forEach(p => {
                p.history.push(p.mesh.position.clone());
                if (p.history.length > MAX_HISTORY) p.history.shift();
            });

            // Update ghost positions based on slider
            updateGhosts();

            // Update controls
            controls.update();

            // Render
            renderer.render(scene, camera);
            labelRenderer.render(scene, camera);

            requestAnimationFrame(animate);
        }

        animate();

        // Resize handler
        window.addEventListener('resize', onWindowResize, false);
        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
            labelRenderer.setSize(window.innerWidth, window.innerHeight);
        }

        // Some interactive flair: click to toggle auto-rotate
        renderer.domElement.addEventListener('click', () => {
            controls.autoRotate = !controls.autoRotate;
        });

        console.log('Ex-Machina Visualizer started');
    </script>
</body>
</html>