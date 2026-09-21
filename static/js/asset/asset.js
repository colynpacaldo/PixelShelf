document.addEventListener("DOMContentLoaded", function () {
    initUploadPreview();
    initSpriteAnimator();
});

/**
 * Live-preview whichever spritesheet the user just picked in the
 * upload/edit form, before the page has even been submitted.
 */
function initUploadPreview() {
    const fileInput = document.getElementById("id_file_path");
    const previewImg = document.getElementById("upload-preview");
    if (!fileInput || !previewImg) return;

    fileInput.addEventListener("change", function () {
        const file = fileInput.files && fileInput.files[0];
        if (!file) return;
        previewImg.src = URL.createObjectURL(file);
        previewImg.hidden = false;
    });
}

/**
 * The sprite animator: slices an uploaded spritesheet into
 * frame_width x frame_height tiles and loops through them on a
 * <canvas>, with play/pause, frame-stepping, an fps control, and a
 * background switcher for checking sprite edges against light/dark/
 * transparent backdrops.
 */
function initSpriteAnimator() {
    const canvas = document.getElementById("sprite-canvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    const frameWidth = parseInt(canvas.dataset.frameWidth, 10) || 32;
    const frameHeight = parseInt(canvas.dataset.frameHeight, 10) || 32;
    const src = canvas.dataset.src;

    const stage = document.getElementById("canvas-stage");
    const playPauseBtn = document.getElementById("play-pause-btn");
    const prevBtn = document.getElementById("prev-frame-btn");
    const nextBtn = document.getElementById("next-frame-btn");
    const fpsSlider = document.getElementById("fps-slider");
    const fpsValue = document.getElementById("fps-value");
    const frameLabel = document.getElementById("frame-label");
    const bgButtons = document.querySelectorAll(".bg-swatch");

    let columns = 1;
    let rows = 1;
    let totalFrames = 1;
    let currentFrame = 0;
    let playing = false;
    let fps = 8;
    let lastTime = 0;
    let rafId = null;

    const image = new Image();

    image.onload = function () {
        columns = Math.max(1, Math.floor(image.naturalWidth / frameWidth));
        rows = Math.max(1, Math.floor(image.naturalHeight / frameHeight));
        totalFrames = Math.max(1, columns * rows);

        canvas.width = frameWidth;
        canvas.height = frameHeight;

        drawFrame(0);
        updateFrameLabel();
        play();
    };

    image.onerror = function () {
        if (stage) {
            stage.innerHTML = '<p class="canvas-error">Could not load this image for preview.</p>';
        }
    };

    image.src = src;

    function drawFrame(index) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const col = index % columns;
        const row = Math.floor(index / columns);
        ctx.drawImage(
            image,
            col * frameWidth, row * frameHeight, frameWidth, frameHeight,
            0, 0, frameWidth, frameHeight
        );
    }

    function updateFrameLabel() {
        if (frameLabel) {
            frameLabel.textContent = "Frame " + (currentFrame + 1) + " / " + totalFrames;
        }
    }

    function step(timestamp) {
        if (!playing) return;
        if (timestamp - lastTime >= 1000 / fps) {
            currentFrame = (currentFrame + 1) % totalFrames;
            drawFrame(currentFrame);
            updateFrameLabel();
            lastTime = timestamp;
        }
        rafId = requestAnimationFrame(step);
    }

    function play() {
        if (playing || totalFrames <= 1) return;
        playing = true;
        if (playPauseBtn) playPauseBtn.textContent = "Pause";
        lastTime = 0;
        rafId = requestAnimationFrame(step);
    }

    function pause() {
        playing = false;
        if (playPauseBtn) playPauseBtn.textContent = "Play";
        if (rafId) cancelAnimationFrame(rafId);
    }

    if (playPauseBtn) {
        playPauseBtn.addEventListener("click", function () {
            if (playing) pause(); else play();
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", function () {
            pause();
            currentFrame = (currentFrame - 1 + totalFrames) % totalFrames;
            drawFrame(currentFrame);
            updateFrameLabel();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", function () {
            pause();
            currentFrame = (currentFrame + 1) % totalFrames;
            drawFrame(currentFrame);
            updateFrameLabel();
        });
    }

    if (fpsSlider) {
        fpsSlider.addEventListener("input", function () {
            fps = parseInt(fpsSlider.value, 10) || 1;
            if (fpsValue) fpsValue.textContent = fps + " fps";
        });
    }

    bgButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
            bgButtons.forEach(function (b) { b.classList.remove("active"); });
            btn.classList.add("active");
            if (stage) {
                stage.classList.remove("bg-light", "bg-dark", "bg-transparent");
                stage.classList.add("bg-" + btn.dataset.bg);
            }
        });
    });
}
