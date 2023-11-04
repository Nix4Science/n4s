import argparse
import math
import csv

PLANETS_GRAVITY = {"earth": 9.81, "moon": 5.21, "mars": 0.0}

def simulation(filename, v0=1, alpha=0.25*math.pi, x0=0, y0=0, planet="earth"):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["time", "x", "y", "v0", "alpha", "planet"])
        x = x0
        y = y0
        step = 0
        t = step * 0.001
        assert planet in PLANETS_GRAVITY.keys(), f"Planet {planet} is not supported"
        g = PLANETS_GRAVITY[planet]
        while y >= 0:
            writer.writerow([t, x, y, v0, alpha, planet])
            step += 1
            t = step * 0.001
            x = v0 * t * math.cos(alpha) + x0
            y = -0.5 * g * t * t + v0 * t * math.sin(alpha) + y0

def main():
    parser = argparse.ArgumentParser(description="Very complex simulation")
    parser.add_argument("--output", "-o", type=str, required=True, help="output file")
    parser.add_argument("--v0", type=float, required=True, help="initial speed")
    parser.add_argument("--alpha", type=float, required=True, help="angle in *degree*")

    args = parser.parse_args()
    assert args.alpha > 0 and args.alpha < 90, "Angle should be between 0 and 90 degrees"
    assert args.v0 > 0, "V0 should be positive"

    simulation(args.output, v0=args.v0, alpha=args.alpha * math.pi / 180, planet="earth")

if __name__ == "__main__":
    main()
