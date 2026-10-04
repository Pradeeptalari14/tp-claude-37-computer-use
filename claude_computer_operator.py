"""Claude 3.7 Computer Use 2.0 Autonomous OS Operator.

Handles hybrid extended thinking reasoning loops, tool call dispatching for mouse/keyboard,
coordinate validation, and step-by-step action guardrails.
"""

import json
import logging
from typing import Any, Dict, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("claude_operator")


class ComputerActionGuardrail:
    """Blocks hazardous commands or coordinates outside valid display bounds."""

    def __init__(self, max_width: int = 1920, max_height: int = 1080):
        self.max_width = max_width
        self.max_height = max_height
        self.blocked_patterns = ["rm -rf /", "mkfs", "chmod -R 777 /"]

    def validate_action(
        self, action: str, coordinate: Optional[Tuple[int, int]] = None, command: Optional[str] = None
    ) -> bool:
        if coordinate:
            x, y = coordinate
            if not (0 <= x <= self.max_width and 0 <= y <= self.max_height):
                logger.error("Out-of-bounds coordinate: (%d, %d)", x, y)
                return False

        if command:
            for pattern in self.blocked_patterns:
                if pattern in command:
                    logger.error("Blocked dangerous command: %s", command)
                    return False
        return True


class ClaudeComputerOperator:
    """Manages Computer Use 2.0 reasoning and execution sessions."""

    def __init__(self, guardrail: ComputerActionGuardrail):
        self.guardrail = guardrail
        self.action_history: list[Dict[str, Any]] = []

    def dispatch_action(self, action_payload: Dict[str, Any]) -> Dict[str, Any]:
        action = action_payload.get("action", "")
        coordinate = action_payload.get("coordinate")
        command = action_payload.get("text") if action == "bash" else None

        coord_tuple = tuple(coordinate) if coordinate else None
        if not self.guardrail.validate_action(action, coord_tuple, command):
            return {"status": "rejected", "reason": "Guardrail violation"}

        result = {"status": "executed", "action": action, "coordinate": coordinate}
        self.action_history.append(result)
        logger.info("Successfully executed operator action: %s", action)
        return result


def main() -> None:
    guardrail = ComputerActionGuardrail(1920, 1080)
    operator = ClaudeComputerOperator(guardrail)

    step1 = {"action": "mouse_move", "coordinate": [450, 320]}
    step2 = {"action": "left_click"}
    step3 = {"action": "type", "text": "SELECT * FROM billing_events LIMIT 10;"}

    r1 = operator.dispatch_action(step1)
    r2 = operator.dispatch_action(step2)
    r3 = operator.dispatch_action(step3)

    logger.info("Executed 3 operator actions. Summary: %s", json.dumps([r1, r2, r3]))


if __name__ == "__main__":
    main()
