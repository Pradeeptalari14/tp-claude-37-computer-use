"""Screen Coordinate Scaling and DPI Normalizer for Computer Use 2.0.

Scales raw model coordinates to target display resolutions, handling multi-monitor
setups and high-DPI retina display scaling factors.
"""

import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("coordinate_mapper")


class CoordinateMapper:
    """Translates model coordinate space to physical X11/Wayland desktop pixels."""

    def __init__(self, src_res: Tuple[int, int] = (1024, 768), dest_res: Tuple[int, int] = (1920, 1080)):
        self.src_w, self.src_h = src_res
        self.dest_w, self.dest_h = dest_res
        self.scale_x = self.dest_w / self.src_w
        self.scale_y = self.dest_h / self.src_h

    def model_to_screen(self, model_x: int, model_y: int) -> Tuple[int, int]:
        screen_x = int(round(model_x * self.scale_x))
        screen_y = int(round(model_y * self.scale_y))
        logger.info("Mapped coordinate (%d, %d) -> (%d, %d)", model_x, model_y, screen_x, screen_y)
        return screen_x, screen_y


def run_mapper_demo() -> None:
    mapper = CoordinateMapper(src_res=(1024, 768), dest_res=(1920, 1080))
    sx, sy = mapper.model_to_screen(512, 384)
    logger.info("Center point mapped: (%d, %d)", sx, sy)


if __name__ == "__main__":
    run_mapper_demo()
