#!/bin/bash
# Standalone burn-in loop for flaky test detection

ITERATIONS=${1:-10} # Default to 10 iterations

echo "🔥 Starting burn-in loop for $ITERATIONS iterations - detecting flaky tests"
for i in $(seq 1 $ITERATIONS); do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔥 Burn-in iteration $i/$ITERATIONS"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  npm run test:e2e || { echo "Burn-in failed on iteration $i"; exit 1; }
done
echo "✅ Burn-in complete - no flaky tests detected after $ITERATIONS iterations"
