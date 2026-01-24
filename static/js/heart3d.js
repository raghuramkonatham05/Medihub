// ✅ PURE BROWSER MODULE (NO "three" STRING ANYWHERE)

import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.158.0/build/three.module.js";
import { OrbitControls } from "https://cdn.jsdelivr.net/npm/three@0.158.0/examples/jsm/controls/OrbitControls.js";
import { FBXLoader } from "https://cdn.jsdelivr.net/npm/three@0.158.0/examples/jsm/loaders/FBXLoader.js";

const container = document.getElementById("heart3d");

if (!container) {
  console.warn("heart3d container not found");
} else {

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xf8fafc);

  const camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  );
  camera.position.set(0, 1.6, 4);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  container.appendChild(renderer.domElement);

  // Lights
  scene.add(new THREE.AmbientLight(0xffffff, 0.7));
  const dirLight = new THREE.DirectionalLight(0xffffff, 1);
  dirLight.position.set(5, 10, 7);
  scene.add(dirLight);

  // Controls
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enableZoom = false;

  // Textures
  const tex = new THREE.TextureLoader();
  const baseColor = tex.load("/static/models/heart/BaseColor.png");
  const normalMap = tex.load("/static/models/heart/Normal.png");
  const roughnessMap = tex.load("/static/models/heart/Roughness.png");
  const metalnessMap = tex.load("/static/models/heart/Metalness.png");

  // Model
  const loader = new FBXLoader();
  loader.load("/static/models/heart/Heart.fbx", (model) => {
    model.scale.set(0.01, 0.01, 0.01);

    model.traverse((child) => {
      if (child.isMesh) {
        child.material = new THREE.MeshStandardMaterial({
          map: baseColor,
          normalMap,
          roughnessMap,
          metalnessMap,
          roughness: 0.7,
          metalness: 0.2
        });
      }
    });

    scene.add(model);

    function animate() {
      requestAnimationFrame(animate);
      model.rotation.y += 0.003;
      controls.update();
      renderer.render(scene, camera);
    }

    animate();
  });

  window.addEventListener("resize", () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });
}
