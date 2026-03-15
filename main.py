import argparse
import asyncio
from src.evaluator import run_evaluation
from src.evaluator_phase2 import run_phase2
def main():
    parser = argparse.ArgumentParser(description="LLM Injection Benchmarking")
    parser.add_argument("--phase", type=int, choices=[1, 2], default=1, help="Which phase to run")
    parser.add_argument("--limit", type=int, default=5, help="Number of injections per tier per model")
    
    args = parser.parse_args()
    
    if args.phase == 1:
        print("Starting Phase 1 Benchmark (Vulnerability Rates)...")
        asyncio.run(run_evaluation(limit=args.limit))
    elif args.phase == 2:
        print("Starting Phase 2 Benchmark (Defense Metrics)...")
        asyncio.run(run_phase2(limit=args.limit))

if __name__ == "__main__":
    main()
