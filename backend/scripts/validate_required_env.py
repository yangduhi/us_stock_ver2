import os


REQUIRED_KEYS = [
    "GEMINI_API_KEY",
    "FRED_API_KEY",
    "FINNHUB_API_KEY",
    "FMP_API_KEY",
    "DATABASE_URL",
    "REDIS_URL",
]


def main() -> int:
    missing = [key for key in REQUIRED_KEYS if not os.getenv(key)]

    if missing:
        print("Missing required environment keys:")
        for key in missing:
            print(f"- {key}")
        return 1

    print("All required environment keys are set.")
    for key in REQUIRED_KEYS:
        print(f"- {key}: SET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
