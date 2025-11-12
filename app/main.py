try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    from fastapi.exceptions import HTTPException
except ModuleNotFoundError as e:
    import sys
    print(f"Module not found: {e.name}")
    print("")
    print("It looks like required Python packages are not installed.")
    print("Recommended steps:")
    print("  1) Create and activate a virtual environment:")
    print("       python -m venv .venv")
    print("       .\\.venv\\Scripts\\activate   (Windows cmd)")
    print("       .\\.venv\\Scripts\\Activate.ps1   (PowerShell)")
    print("  2) Install dependencies:")
    print("       pip install -r requirements.txt")
    print("")
    sys.exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to handle application startup and shutdown events.
    """
    logger.info("Starting up Template Service...")
    try:
        # On startup: Create database tables
        await create_db_and_tables()
        logger.info("Database tables created (if not exist).")
        # TODO: Initialize Redis connection pool
        # TODO: Initialize RabbitMQ connection
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    yield  # The application is now running
    
    # On shutdown:
    logger.info("Shutting down Template Service...")
    await close_db_connection()
    # TODO: Close Redis connection pool
    # TODO: Close RabbitMQ connection
    logger.info("Shutdown complete.")

# Initialize the FastAPI app with the lifespan event handler
app = FastAPI(
    title="Template Service",
    description="Manages email and push notification templates for the HNG Distributed Notification System.",
    version="1.0.0",
    lifespan=lifespan
)

# --- Custom Exception Handler ---
# This ensures that even when an HTTPException occurs (like a 404),
# the response *still* follows your HNG BaseResponse format.
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(
            success=False,
            message="An error occurred.",
            error=exc.detail
        ).model_dump()
    )

# --- Include the API Routes ---
app.include_router(api_router, prefix="/api/v1")  # <-- INCLUDE THE ROUTER

@app.get("/health", response_model=BaseResponse, tags=["Monitoring"])
async def health_check():
    """
    Health check endpoint required by the HNG spec.
    """
    return BaseResponse(
        success=True,
        message="Template Service is healthy and running."
    )