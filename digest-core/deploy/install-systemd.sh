#!/bin/bash
# Install ActionPulse systemd user timer + service.
# Run as the target user (not root).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UNIT_DIR="${HOME}/.config/systemd/user"

echo "Installing ActionPulse systemd units..."

# Create directories
mkdir -p "$UNIT_DIR"
mkdir -p "${HOME}/.config/actionpulse"

# Copy unit files
cp "$SCRIPT_DIR/actionpulse-digest.service" "$UNIT_DIR/actionpulse-digest@.service"
cp "$SCRIPT_DIR/actionpulse-digest.timer"   "$UNIT_DIR/actionpulse-digest.timer"

# Create env file if it doesn't exist
if [ ! -f "${HOME}/.config/actionpulse/env" ]; then
    cp "$SCRIPT_DIR/env.example" "${HOME}/.config/actionpulse/env"
    chmod 600 "${HOME}/.config/actionpulse/env"
    echo "Created ${HOME}/.config/actionpulse/env — fill in your secrets."
else
    echo "Env file already exists, skipping."
fi

# Reload and enable
systemctl --user daemon-reload
systemctl --user enable actionpulse-digest.timer
systemctl --user start actionpulse-digest.timer

echo ""
echo "Installed. Verify with:"
echo "  systemctl --user status actionpulse-digest.timer"
echo "  systemctl --user list-timers"
echo ""
echo "Manual test run:"
echo "  systemctl --user start actionpulse-digest@\$(whoami).service"
echo ""
echo "View logs:"
echo "  journalctl --user -u actionpulse-digest@\$(whoami) -f"
