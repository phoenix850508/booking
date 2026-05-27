"""
Race condition test for the naive booking endpoint.

Setup before running:
  1. Server must be running: pdm run uvicorn app.main:app --reload
  2. Set a small seat count in DB:
       UPDATE ticket_tiers SET available_seats = 5 WHERE id = 1;

Run:
  pdm run python tests/race_condition.py
"""

import asyncio
import httpx

BASE_URL = "http://localhost:8000"
CONCERT_ID = 1
TIER_ID = 1
NUM_CONCURRENT = 20  # intentionally more than available_seats


async def login(client: httpx.AsyncClient, user_num: int) -> str:
    r = await client.post(
        f"{BASE_URL}/auth/login",
        json={"username": f"user_{user_num}", "password": f"password_{user_num}"},
    )
    r.raise_for_status()
    return r.json()["access_token"]


async def book(client: httpx.AsyncClient, token: str, user_num: int) -> dict:
    r = await client.post(
        f"{BASE_URL}/concerts/{CONCERT_ID}/book",
        json={"ticket_tier_id": TIER_ID, "quantity": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    return {"user": user_num, "status": r.status_code, "body": r.json()}


async def get_tier(client: httpx.AsyncClient) -> dict:
    r = await client.get(f"{BASE_URL}/concerts/{CONCERT_ID}/tiers")
    r.raise_for_status()
    tiers = r.json()
    return next(t for t in tiers if t["id"] == TIER_ID)


async def main():
    async with httpx.AsyncClient(timeout=30) as client:
        tier = await get_tier(client)
        seats_before = tier["available_seats"]
        print(f"Tier: '{tier['name']}'")
        print(f"available_seats BEFORE: {seats_before}")
        print(f"Firing {NUM_CONCURRENT} concurrent requests...\n")

        # Login all users first, then fire all bookings at the same time
        tokens = await asyncio.gather(
            *[login(client, i) for i in range(1, NUM_CONCURRENT + 1)]
        )
        results = await asyncio.gather(
            *[book(client, token, i + 1) for i, token in enumerate(tokens)]
        )

        successes = [r for r in results if r["status"] == 201]
        failures  = [r for r in results if r["status"] != 201]

        print(f"✅ Succeeded : {len(successes)}")
        print(f"❌ Failed    : {len(failures)}")

        tier = await get_tier(client)
        seats_after = tier["available_seats"]
        print(f"\navailable_seats AFTER : {seats_after}")

        expected = seats_before - len(successes)
        print(f"Expected              : {expected}")

        if seats_after != expected:
            diff = expected - seats_after
            print(f"\n🚨 RACE CONDITION DETECTED — oversold by {diff} seat(s)!")
            print(f"   {len(successes)} bookings accepted but only {seats_before} seats were available")
        elif len(successes) > seats_before:
            print(f"\n🚨 RACE CONDITION DETECTED — {len(successes)} bookings accepted for {seats_before} seats!")
        else:
            print("\n✅ No overselling detected this run (try again or increase NUM_CONCURRENT)")


if __name__ == "__main__":
    asyncio.run(main())
