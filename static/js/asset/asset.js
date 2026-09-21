document.addEventListener("DOMContentLoaded", function () {
    initUploadPreview();
    initSpritesheetToggle();
    initSpriteAnimator();
});

/**
 * Upload/edit form: the frame-size options only make sense for animated
 * spritesheets, so reveal them only while that box is ticked.
 */
function initSpritesheetToggle() {
    const checkbox = document.getElementById("id_is_spritesheet");
    const options = document.getElementById("spritesheet-options");
    if (!checkbox || !options) return;

    function sync() { options.hidden = !checkbox.checked; }
    checkbox.addEventListener("change", sync);
    sync();
}

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
 * The sprite viewer.
 *
 * - Static sprite (default): shows the whole image, scaled to fit the stage.
 * - Animated spritesheet: slices the sheet into frame_width x frame_height
 *   tiles and loops through them on a <canvas>, with play/pause,
 *   frame-stepping and an fps control.
 *
 * Either way the canvas is scaled so the WHOLE frame is visible, using the
 * largest whole-number zoom that fits (keeps pixel art crisp), and it re-fits
 * when the window is resized. A background switcher lets you check sprite
 * edges against light / dark / transparent backdrops.
 */
function initSpriteAnimator() {
    const canvas = document.getElementById("sprite-canvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    const src = canvas.dataset.src;
    const isAnimated = canvas.dataset.animated === "true";

    const stage = document.getElementById("canvas-stage");
    const playPauseBtn = document.getElementById("play-pause-btn");
    const prevBtn = document.getElementById("prev-frame-btn");
    const nextBtn = document.getElementById("next-frame-btn");
    const fpsSlider = document.getElementById("fps-slider");
    const fpsValue = document.getElementById("fps-value");
    const frameLabel = document.getElementById("frame-label");
    const bgButtons = document.querySelectorAll(".bg-swatch");

    let frameWidth = 0;
    let frameHeight = 0;
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
        const naturalW = image.naturalWidth;
        const naturalH = image.naturalHeight;

        if (isAnimated) {
            // Never let a frame be bigger than the image itself.
            frameWidth = Math.min(parseInt(canvas.dataset.frameWidth, 10) || naturalW, naturalW);
            frameHeight = Math.min(parseInt(canvas.dataset.frameHeight, 10) || naturalH, naturalH);
        } else {
            frameWidth = naturalW;
            frameHeight = naturalH;
        }

        columns = Math.max(1, Math.floor(naturalW / frameWidth));
        rows = Math.max(1, Math.floor(naturalH / frameHeight));
        totalFrames = isAnimated ? Math.max(1, columns * rows) : 1;

        canvas.width = frameWidth;
        canvas.height = frameHeight;

        fitCanvas();
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

    /**
     * Size the canvas so the whole frame fits inside the stage. Zooms in by
     * whole numbers when the frame is small (crisp pixels) and scales down
     * smoothly when the frame is bigger than the stage.
     */
    function fitCanvas() {
        if (!stage || !frameWidth || !frameHeight) return;
        const css = getComputedStyle(stage);
        const availW = stage.clientWidth - parseFloat(css.paddingLeft) - parseFloat(css.paddingRight);
        const availH = stage.clientHeight - parseFloat(css.paddingTop) - parseFloat(css.paddingBottom);

        let scale = Math.min(availW / frameWidth, availH / frameHeight);
        scale = scale >= 1 ? Math.min(Math.floor(scale), 32) : Math.max(scale, 0.05);

        canvas.style.width = Math.round(frameWidth * scale) + "px";
        canvas.style.height = Math.round(frameHeight * scale) + "px";
        canvas.style.imageRendering = scale >= 1 ? "pixelated" : "auto";
    }

    window.addEventListener("resize", fitCanvas);

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
