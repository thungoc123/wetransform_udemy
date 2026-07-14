import asyncio

import httpx


async def test_api():
    base_url = "http://127.0.0.1:8000"

    async with httpx.AsyncClient() as client:
        # 1. Login to get token
        login_data = {
            "email": "admin@learning-analytics.com",
            "password": "adminpassword",
        }
        res = await client.post(f"{base_url}/api/v1/auth/login", json=login_data)
        json_res = res.json()
        print("Login response:", json_res)
        token = json_res.get("token")
        if not token:
            print("No token found")
            return

        headers = {"Authorization": f"Bearer {token}"}
        print("Logged in successfully.")

        # 2. Get Data Sources
        print("\n--- Getting Data Sources ---")
        res = await client.get(f"{base_url}/api/v1/data/sources", headers=headers)
        print("Status:", res.status_code)
        print("Response:", res.json())

        # 3. Connect Udemy
        print("\n--- Connecting Udemy ---")
        udemy_data = {
            "clientId": "test_client_id_123",
            "clientSecret": "test_client_secret_abc",
        }
        res = await client.post(
            f"{base_url}/api/v1/data/udemy-connection", json=udemy_data, headers=headers
        )
        print("Status:", res.status_code)
        print("Response:", res.json())

        # 4. Upload CSV
        print("\n--- Uploading CSV ---")
        with open("dummy_import.csv", "rb") as f:
            files = {"file": ("dummy_import.csv", f, "text/csv")}
            res = await client.post(
                f"{base_url}/api/v1/data/upload", files=files, headers=headers
            )
            print("Status:", res.status_code)
            print("Response:", res.json())


if __name__ == "__main__":
    asyncio.run(test_api())
