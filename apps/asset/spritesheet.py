"""Automatic frame-grid detection for spritesheets.

Most spritesheets are a regular grid of equally sized cells with a bit of
empty space between the characters.  We exploit that:

1. Build a "content mask" (which pixels are sprite, which are background).
2. Project the mask onto the X and Y axes -> which columns / rows contain
   any sprite pixels at all.
3. For each axis, find the *largest* number of equal cells such that every
   cell boundary lands in empty space (no sprite is cut in half) and every
   cell contains something.

Only Pillow is needed (it is already a dependency for ImageField).
"""

from collections import Counter

from PIL import Image, ImageChops

MIN_FRAME_PX = 4          # never suggest frames smaller than this
MAX_FRAMES_PER_AXIS = 64  # sanity cap on the search
BG_TOLERANCE = 24         # per-channel colour distance still counted as background
ALPHA_CUTOFF = 16         # alpha at/below this counts as transparent
TRANSPARENT_SHARE = 0.01  # >= this fraction see-through => use alpha as the mask


def _background_colour(rgb):
    """Most common colour among the four corners (ties -> first corner)."""
    w, h = rgb.size
    corners = [rgb.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    return Counter(corners).most_common(1)[0][0]


def _content_mask(im):
    """Return an 'L' image: 255 where there is sprite, 0 where there is background."""
    im = im.convert("RGBA")
    alpha = im.getchannel("A")

    # Sheets with a genuinely transparent backdrop: the alpha channel *is* the
    # mask.  "Genuinely" matters - exported sheets often have a few stray
    # semi-transparent edge pixels on an otherwise opaque backdrop, so we
    # require a meaningful share of the image to be see-through.
    histogram = alpha.histogram()
    transparent_share = sum(histogram[: ALPHA_CUTOFF + 1]) / (im.width * im.height)
    if transparent_share >= TRANSPARENT_SHARE:
        return alpha.point(lambda a: 255 if a > ALPHA_CUTOFF else 0)

    # Opaque sheets (e.g. a white or flat-coloured backdrop): anything that
    # differs from the backdrop colour is sprite.
    rgb = im.convert("RGB")
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, _background_colour(rgb)))
    r, g, b = diff.split()
    biggest = ImageChops.lighter(ImageChops.lighter(r, g), b)
    return biggest.point(lambda v: 255 if v > BG_TOLERANCE else 0)


def _cells_for_axis(profile):
    """Largest n that splits this axis into n equal cells cleanly (1 if none).

    `profile[i]` is truthy when column/row i contains any sprite pixels.
    Boundaries are checked at exactly the positions the browser animator will
    use (multiples of length // n), so what we validate is what gets drawn.
    """
    length = len(profile)
    for n in range(min(MAX_FRAMES_PER_AXIS, length // MIN_FRAME_PX), 1, -1):
        size = length // n
        cuts = [size * k for k in range(1, n)]
        # A boundary is fine if no sprite pixels sit on *both* sides of it.
        if any(profile[c - 1] and profile[c] for c in cuts):
            continue
        # Every cell must contain something (rules out "one sprite in a big margin").
        if all(any(profile[k * size:(k + 1) * size]) for k in range(n)):
            return n
    return 1


def detect_frame_grid(fileobj):
    """Inspect an image file and guess its frame grid.

    Returns a dict: ``frame_width``, ``frame_height``, ``cols``, ``rows``.
    A 1x1 grid means "no repeating frames found" (the whole image is one frame).
    """
    if hasattr(fileobj, "seek"):
        fileobj.seek(0)
    try:
        with Image.open(fileobj) as im:
            width, height = im.size
            x_profile, y_profile = _content_mask(im).getprojection()
    finally:
        if hasattr(fileobj, "seek"):
            fileobj.seek(0)

    cols = _cells_for_axis(x_profile)
    rows = _cells_for_axis(y_profile)
    return {
        "frame_width": width // cols,
        "frame_height": height // rows,
        "cols": cols,
        "rows": rows,
    }
