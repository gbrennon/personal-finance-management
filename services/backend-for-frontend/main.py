from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import os
from typing import Optional, Dict, Any
import asyncio

app = FastAPI(title="Personal Finance BFF", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
FINANCE_SERVICE_URL = os.getenv("FINANCE_SERVICE_URL", "http://localhost:8001")
RETIREMENT_SERVICE_URL = os.getenv("RETIREMENT_SERVICE_URL", "http://localhost:8002")

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    # In a real implementation, you would validate the JWT token here
    # For now, we'll just pass through the authorization header
    return credentials.credentials


@app.get("/")
async def root():
    return {"message": "Personal Finance BFF API"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            finance_health = await client.get(
                f"{FINANCE_SERVICE_URL}/api/", timeout=5.0
            )
            retirement_health = await client.get(
                f"{RETIREMENT_SERVICE_URL}/api/", timeout=5.0
            )

        return {
            "status": "healthy",
            "services": {
                "finance": finance_health.status_code == 200,
                "retirement": retirement_health.status_code == 200,
            },
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


# Finance Service Endpoints
@app.get("/api/finance/transactions")
async def get_transactions(token: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FINANCE_SERVICE_URL}/api/transactions/",
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.post("/api/finance/transactions")
async def create_transaction(
    transaction_data: Dict[str, Any], token: str = Depends(get_current_user)
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FINANCE_SERVICE_URL}/api/transactions/",
            json=transaction_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code not in [200, 201]:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.get("/api/finance/transactions/summary")
async def get_transactions_summary(token: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FINANCE_SERVICE_URL}/api/transactions/summary/",
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.get("/api/finance/categories")
async def get_categories(token: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FINANCE_SERVICE_URL}/api/categories/",
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.post("/api/finance/categories")
async def create_category(
    category_data: Dict[str, Any], token: str = Depends(get_current_user)
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FINANCE_SERVICE_URL}/api/categories/",
            json=category_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code not in [200, 201]:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.get("/api/finance/budgets")
async def get_budgets(token: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FINANCE_SERVICE_URL}/api/budgets/",
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.post("/api/finance/budgets")
async def create_budget(
    budget_data: Dict[str, Any], token: str = Depends(get_current_user)
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FINANCE_SERVICE_URL}/api/budgets/",
            json=budget_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code not in [200, 201]:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


# Retirement Service Endpoints
@app.get("/api/retirement/plans")
async def get_retirement_plans(token: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{RETIREMENT_SERVICE_URL}/api/plans/",
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.post("/api/retirement/plans")
async def create_retirement_plan(
    plan_data: Dict[str, Any], token: str = Depends(get_current_user)
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{RETIREMENT_SERVICE_URL}/api/plans/",
            json=plan_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code not in [200, 201]:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.get("/api/retirement/goals")
async def get_retirement_goals(token: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{RETIREMENT_SERVICE_URL}/api/goals/",
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.post("/api/retirement/goals")
async def create_retirement_goal(
    goal_data: Dict[str, Any], token: str = Depends(get_current_user)
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{RETIREMENT_SERVICE_URL}/api/goals/",
            json=goal_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code not in [200, 201]:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


# Combined Dashboard Endpoint
@app.get("/api/dashboard")
async def get_dashboard_data(token: str = Depends(get_current_user)):
    """Get combined dashboard data from all services"""
    async with httpx.AsyncClient() as client:
        try:
            # Fetch data from both services concurrently
            finance_summary_task = client.get(
                f"{FINANCE_SERVICE_URL}/api/transactions/summary/",
                headers={"Authorization": f"Bearer {token}"},
            )
            retirement_plans_task = client.get(
                f"{RETIREMENT_SERVICE_URL}/api/plans/",
                headers={"Authorization": f"Bearer {token}"},
            )

            finance_summary_response, retirement_plans_response = await asyncio.gather(
                finance_summary_task, retirement_plans_task, return_exceptions=True
            )

            dashboard_data = {}

            # Process finance data
            if (
                isinstance(finance_summary_response, httpx.Response)
                and finance_summary_response.status_code == 200
            ):
                dashboard_data["finance_summary"] = finance_summary_response.json()
            else:
                dashboard_data["finance_summary"] = {
                    "error": "Unable to fetch finance data"
                }

            # Process retirement data
            if (
                isinstance(retirement_plans_response, httpx.Response)
                and retirement_plans_response.status_code == 200
            ):
                dashboard_data["retirement_plans"] = retirement_plans_response.json()
            else:
                dashboard_data["retirement_plans"] = {
                    "error": "Unable to fetch retirement data"
                }

            return dashboard_data

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching dashboard data: {str(e)}"
            )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8003)
