import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const fileInput = document.querySelector('input[type="file"]');
const previewContainer = document.getElementById('preview-container');
const hiddenInput = document.getElementById('id_image_data');
const submitBtn = document.getElementById('submit-btn');

if (fileInput) {
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const url = URL.createObjectURL(file);
            generateThumbnail(url);
        }
    });
}

function generateThumbnail(modelUrl) {
    previewContainer.innerHTML = 'Генерация...';

    const width = 300;
    const height = 200;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);

    const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    renderer.setSize(width, height);
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    previewContainer.innerHTML = '';
    previewContainer.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
    dirLight.position.set(5, 10, 7);
    scene.add(dirLight);

    const loader = new GLTFLoader();

    loader.load(modelUrl, (gltf) => {
        const model = gltf.scene;

        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);

        model.position.sub(center);
        scene.add(model);

        const fov = camera.fov * (Math.PI / 180);
        const cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2)) * 1.5;

        camera.position.set(cameraZ * 0.5, cameraZ * 0.5, cameraZ);
        camera.lookAt(0, 0, 0);

        renderer.render(scene, camera);

        const dataURL = renderer.domElement.toDataURL('image/jpeg', 0.8);

        hiddenInput.value = dataURL;
        submitBtn.disabled = false;
        submitBtn.innerText = 'Загрузить в базу';

        console.log('Скриншот создан!');
        URL.revokeObjectURL(modelUrl);
    }, undefined, (err) => {
        console.error(err);
        previewContainer.innerHTML = 'Ошибка генерации превью';
    });
}