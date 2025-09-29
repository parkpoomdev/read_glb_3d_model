import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf4f4f4);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 1.5, 3);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.useLegacyLights = false;
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.1, 0);
controls.enableDamping = true;
// Set initial camera azimuth and distance using spherical coordinates
{
    const desiredAzimuthDeg = 25;
    const desiredDistance = 5.35;
    const offset = camera.position.clone().sub(controls.target);
    const spherical = new THREE.Spherical().setFromVector3(offset);
    spherical.radius = desiredDistance;
    spherical.theta = THREE.MathUtils.degToRad(desiredAzimuthDeg);
    const newOffset = new THREE.Vector3().setFromSpherical(spherical);
    camera.position.copy(controls.target).add(newOffset);
}
controls.update();

// Lighting
const ambientLight = new THREE.AmbientLight(0xfff0e5, 0.6);
scene.add(ambientLight);

const sunLight = new THREE.DirectionalLight(0xfff6cf, 1.1);
sunLight.position.set(-6, 9, 6);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.radius = 4;
sunLight.shadow.bias = -0.0002;
scene.add(sunLight);

const keyLight = new THREE.DirectionalLight(0xffffff, 0.8);
keyLight.position.set(5, 7, 4);
keyLight.castShadow = true;
keyLight.shadow.bias = -0.0005;
scene.add(keyLight);

const rimLight = new THREE.DirectionalLight(0xfff5f0, 0.5);
rimLight.position.set(-4, 4, -3);
scene.add(rimLight);

// Ground
const groundGeometry = new THREE.CircleGeometry(5, 48);
const groundMaterial = new THREE.MeshStandardMaterial({ color: 0xfaf5f0, roughness: 0.95, metalness: 0 });
const ground = new THREE.Mesh(groundGeometry, groundMaterial);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Model loading
const loader = new GLTFLoader();
const modelUrl = new URL('./human_model_sit_possition_003.glb', import.meta.url);
const NEUTRAL_GREY = 0x808080;

function makeNeutralMaterial(sourceMaterial) {
    const material = new THREE.MeshStandardMaterial({
        color: NEUTRAL_GREY,
        roughness: 0.65,
        metalness: 0.05,
        skinning: sourceMaterial?.skinning === true
    });

    material.needsUpdate = true;
    return material;
}

loader.load(
    modelUrl.href,
    (gltf) => {
        const model = gltf.scene || gltf.scenes[0];
        if (!model) {
            console.error('GLB did not contain a scene');
            return;
        }

        model.scale.setScalar(1);

        model.traverse((child) => {
            if (!child.isMesh) {
                return;
            }

            child.castShadow = true;
            child.receiveShadow = true;

            const materials = Array.isArray(child.material) ? child.material : [child.material];
            const updatedMaterials = materials.map((mat) => makeNeutralMaterial(mat));
            child.material = Array.isArray(child.material) ? updatedMaterials : updatedMaterials[0];
        });

        scene.add(model);
    },
    undefined,
    (error) => {
        console.error('Failed to load GLB model:', error);
    }
);

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

animate();

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
