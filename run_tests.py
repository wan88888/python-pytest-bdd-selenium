#!/usr/bin/env python
"""
Test runner script for the pytest-bdd-selenium framework.
This script provides a convenient way to run tests with various options.
"""

import os
import sys
import argparse
import subprocess
import datetime
import logging


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run automation tests")
    parser.add_argument("--browser", "-b", choices=["chrome", "firefox", "edge"],
                        default="chrome", help="Browser to use for tests")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--path", "-p", default="tests", help="Path to test files/directories")
    parser.add_argument("--markers", "-m", help="Run tests with specific pytest markers")
    parser.add_argument("--report", "-r", action="store_true", help="Generate HTML report")
    parser.add_argument("--report-name", default=None,
                        help="Custom report name (default: report_<timestamp>.html)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--parallel", "-n", type=int, default=0,
                        help="Number of parallel processes (default: 0 for no parallelism)")
    parser.add_argument("--reruns", type=int, default=0, 
                        help="Number of times to retry failed tests (default: 0)")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        default="INFO", help="Set logging level")
    parser.add_argument("--tags", help="Run tests with specific BDD tags")
    parser.add_argument("--skip-browser-update", action="store_true", 
                        help="Skip automatic browser driver update")
    parser.add_argument("--clean", action="store_true", 
                        help="Clean reports and screenshots before running")
    
    return parser.parse_args()


def clean_directories():
    """Clean reports and screenshots directories."""
    import shutil
    directories = ["reports", "logs"]
    
    for directory in directories:
        if os.path.exists(directory):
            logging.info(f"Cleaning directory: {directory}")
            shutil.rmtree(directory)
            os.makedirs(directory)
    
    logging.info("Clean-up completed")


def run_tests(args):
    """Run tests with the specified options."""
    # Set environment variables
    env = os.environ.copy()
    env["BROWSER"] = args.browser
    env["HEADLESS"] = str(args.headless).lower()
    
    if args.skip_browser_update:
        env["WDM_PROGRESS_BAR"] = "0"
        env["WDM_LOG_LEVEL"] = "0"
    
    env["PYTHONPATH"] = os.getcwd()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Clean directories if requested
    if args.clean:
        clean_directories()
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Build command
    cmd = [sys.executable, "-m", "pytest"]
    
    if args.verbose:
        cmd.append("-v")
    
    if args.markers:
        cmd.append(f"-m={args.markers}")
    
    if args.tags:
        cmd.append(f"--bdd-tags={args.tags}")
    
    # Handle parallel testing
    if args.parallel > 0:
        cmd.append(f"-n={args.parallel}")
    
    # Handle test retries
    if args.reruns > 0:
        cmd.append(f"--reruns={args.reruns}")
    
    # Handle report generation
    if args.report:
        # Generate report filename with timestamp if not specified
        if not args.report_name:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"report_{timestamp}.html"
        else:
            report_name = args.report_name
        
        report_path = os.path.join("reports", report_name)
        cmd.append(f"--html={report_path}")
        cmd.append("--self-contained-html")
    
    # Add test path
    cmd.append(args.path)
    
    # Run the tests
    logging.info(f"Running command: {' '.join(cmd)}")
    process = subprocess.run(cmd, env=env)
    
    return process.returncode


if __name__ == "__main__":
    args = parse_args()
    sys.exit(run_tests(args)) 