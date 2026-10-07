import argparse
import json
import urllib.request

BASE = "http://127.0.0.1:8000"


def request(method: str, path: str, payload: dict | None = None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def main():
    parser = argparse.ArgumentParser(description="Self-service deployment CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    deploy = sub.add_parser("deploy")
    deploy.add_argument("application")
    deploy.add_argument("version")
    deploy.add_argument("environment")
    deploy.add_argument("--simulate-failure", action="store_true")
    status = sub.add_parser("status")
    status.add_argument("id")
    events = sub.add_parser("events")
    events.add_argument("id")
    args = parser.parse_args()
    if args.command == "deploy":
        print(json.dumps(request("POST", "/deployments", {"application": args.application, "version": args.version, "environment": args.environment, "simulate_failure": args.simulate_failure}), indent=2))
    elif args.command == "status":
        print(json.dumps(request("GET", f"/deployments/{args.id}"), indent=2))
    else:
        print(json.dumps(request("GET", f"/deployments/{args.id}/events"), indent=2))


if __name__ == "__main__":
    main()
