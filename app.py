"""
Crypto Compatibility Engine - Main FastAPI Application
Production-ready dating frame for Farcaster
"""
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import our modules
from database import db
from matching_algorithm.matchmaker import MatchmakerAI
from frame_generator.frame_builder import FrameGenerator
from comedy_generator import ComedyGenerator

load_dotenv()

# Initialize components
matchmaker = MatchmakerAI(use_mock_data=True)  # Change to False when you have real API keys
comedy_gen = ComedyGenerator()

# Get base URL from environment
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')
frame_generator = FrameGenerator(BASE_URL)

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Crypto Compatibility Engine...")
    try:
        await db.connect()
        print("✅ Database connected")
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("📝 Running without database (demo mode)")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")
    try:
        await db.disconnect()
    except:
        pass

# Create FastAPI app
app = FastAPI(
    title="Crypto Compatibility Engine",
    description="AI-powered crypto dating for Farcaster",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
os.makedirs("static", exist_ok=True)
os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# ============================================================================
# MAIN FRAME ENDPOINTS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main entry point - initial frame"""
    frame_data = frame_generator.generate_start_frame()
    html = frame_generator.generate_frame_html(
        frame_data,
        title="🚀 Find Your Crypto Soulmate!"
    )
    return HTMLResponse(content=html)


@app.post("/api/analyze")
async def analyze_personality(request: Request):
    """Analyze user's crypto personality"""
    try:
        # Get FID from frame message
        body = await request.json()
        fid = body.get('untrustedData', {}).get('fid')
        
        if not fid:
            return JSONResponse(
                content=frame_generator.generate_error_frame("Could not identify user"),
                status_code=400
            )
        
        # Check rate limit
        try:
            within_limit = await db.check_rate_limit(fid)
            if not within_limit:
                return JSONResponse(
                    content=frame_generator.generate_rate_limit_frame()
                )
        except:
            pass  # Continue if database is not available
        
        # Analyze personality
        analysis = await matchmaker.analyze_user_personality(fid)
        
        # Save to database
        try:
            await db.save_user(
                fid=fid,
                username=analysis.get('username', f'user_{fid}'),
                personality_type=analysis['personality_type'],
                personality_scores=analysis['scores']
            )
            
            # Log analytics
            await db.log_analytics('personality_analyzed', fid, {
                'personality_type': analysis['personality_type']
            })
        except:
            pass  # Continue if database is not available
        
        # Generate result frame
        frame_data = frame_generator.generate_personality_result_frame(analysis)
        return JSONResponse(content=frame_data)
    
    except Exception as e:
        print(f"Error in analyze: {e}")
        return JSONResponse(
            content=frame_generator.generate_error_frame(str(e)),
            status_code=500
        )


@app.post("/api/find-matches")
async def find_matches(request: Request):
    """Find compatible matches for user"""
    try:
        # Get FID from frame message
        body = await request.json()
        fid = body.get('untrustedData', {}).get('fid')
        
        if not fid:
            return JSONResponse(
                content=frame_generator.generate_error_frame("Could not identify user"),
                status_code=400
            )
        
        # Find matches
        matches = await matchmaker.find_matches(fid, limit=5)
        
        if not matches:
            return JSONResponse(
                content=frame_generator.generate_no_matches_frame()
            )
        
        # Save matches to database
        try:
            for match in matches:
                await db.save_match(
                    user_fid=fid,
                    match_fid=match['match_fid'],
                    compatibility_score=match['compatibility_score'],
                    match_details=match
                )
            
            # Log analytics
            await db.log_analytics('matches_found', fid, {
                'match_count': len(matches),
                'top_score': matches[0]['compatibility_score']
            })
        except:
            pass
        
        # Show first match
        frame_data = frame_generator.generate_matches_frame(matches, current_index=0)
        return JSONResponse(content=frame_data)
    
    except Exception as e:
        print(f"Error in find_matches: {e}")
        return JSONResponse(
            content=frame_generator.generate_error_frame(str(e)),
            status_code=500
        )


@app.post("/api/match/{index}")
async def view_match(index: int, request: Request):
    """View specific match by index"""
    try:
        body = await request.json()
        fid = body.get('untrustedData', {}).get('fid')
        
        # Get user's matches from database
        try:
            matches = await db.get_top_matches(fid, limit=10)
        except:
            # Fallback: recalculate
            matches = await matchmaker.find_matches(fid, limit=5)
        
        if not matches or index >= len(matches):
            return JSONResponse(
                content=frame_generator.generate_no_matches_frame()
            )
        
        frame_data = frame_generator.generate_matches_frame(matches, current_index=index)
        return JSONResponse(content=frame_data)
    
    except Exception as e:
        print(f"Error in view_match: {e}")
        return JSONResponse(
            content=frame_generator.generate_error_frame(str(e)),
            status_code=500
        )


@app.post("/api/match-details/{index}")
async def match_details(index: int, request: Request):
    """View detailed match analysis"""
    try:
        body = await request.json()
        fid = body.get('untrustedData', {}).get('fid')
        
        # Get matches
        try:
            matches = await db.get_top_matches(fid, limit=10)
        except:
            matches = await matchmaker.find_matches(fid, limit=5)
        
        if not matches or index >= len(matches):
            return JSONResponse(
                content=frame_generator.generate_no_matches_frame()
            )
        
        match_data = matches[index]
        frame_data = frame_generator.generate_match_details_frame(match_data)
        return JSONResponse(content=frame_data)
    
    except Exception as e:
        print(f"Error in match_details: {e}")
        return JSONResponse(
            content=frame_generator.generate_error_frame(str(e)),
            status_code=500
        )


@app.post("/api/share/{index}")
@app.post("/api/share-details")
async def share_match(request: Request, index: int = 0):
    """Generate shareable frame"""
    try:
        body = await request.json()
        fid = body.get('untrustedData', {}).get('fid')
        
        # Get matches
        try:
            matches = await db.get_top_matches(fid, limit=10)
        except:
            matches = await matchmaker.find_matches(fid, limit=5)
        
        if not matches or index >= len(matches):
            return JSONResponse(
                content=frame_generator.generate_error_frame("No matches found")
            )
        
        match_data = matches[index]
        
        # Log share event
        try:
            await db.log_analytics('match_shared', fid, {
                'match_fid': match_data['match_fid'],
                'compatibility_score': match_data['compatibility_score']
            })
        except:
            pass
        
        frame_data = frame_generator.generate_share_frame(match_data)
        return JSONResponse(content=frame_data)
    
    except Exception as e:
        print(f"Error in share: {e}")
        return JSONResponse(
            content=frame_generator.generate_error_frame(str(e)),
            status_code=500
        )


@app.post("/api/info")
async def info():
    """Information about how it works"""
    frame_data = frame_generator.generate_info_frame()
    return JSONResponse(content=frame_data)


# ============================================================================
# API ENDPOINTS (for external use)
# ============================================================================

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Crypto Compatibility Engine"
    }


@app.get("/api/personalities")
async def list_personalities():
    """List all available personality types"""
    personalities = matchmaker.personality_analyzer.get_all_personalities()
    return {"personalities": personalities}


@app.get("/api/user/{fid}")
async def get_user_analysis(fid: int):
    """Get personality analysis for a specific user"""
    try:
        analysis = await matchmaker.analyze_user_personality(fid)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/compatibility/{fid1}/{fid2}")
async def check_compatibility(fid1: int, fid2: int):
    """Check compatibility between two users"""
    try:
        match_data = await matchmaker.get_match_details(fid1, fid2)
        return match_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/analytics")
async def get_analytics():
    """Get platform analytics (requires authentication in production)"""
    try:
        stats = await db.get_analytics_summary(days=7)
        return stats
    except Exception as e:
        return {
            "error": "Analytics not available",
            "message": str(e)
        }


# ============================================================================
# IMAGE GENERATION ENDPOINTS (Placeholder)
# ============================================================================

@app.get("/api/generate-image/personality")
async def generate_personality_image(data: str):
    """Generate personality result image"""
    # TODO: Implement image generation using PIL or similar
    # For now, return placeholder
    return Response(
        content=open('static/images/placeholder.png', 'rb').read() if os.path.exists('static/images/placeholder.png') else b'',
        media_type='image/png'
    )


@app.get("/api/generate-image/match")
async def generate_match_image(data: str):
    """Generate match result image"""
    # TODO: Implement image generation
    return Response(
        content=open('static/images/placeholder.png', 'rb').read() if os.path.exists('static/images/placeholder.png') else b'',
        media_type='image/png'
    )


@app.get("/api/generate-image/details")
async def generate_details_image(data: str):
    """Generate detailed analysis image"""
    # TODO: Implement image generation
    return Response(
        content=open('static/images/placeholder.png', 'rb').read() if os.path.exists('static/images/placeholder.png') else b'',
        media_type='image/png'
    )


@app.get("/api/generate-image/share")
async def generate_share_image(data: str):
    """Generate shareable image"""
    # TODO: Implement image generation
    return Response(
        content=open('static/images/placeholder.png', 'rb').read() if os.path.exists('static/images/placeholder.png') else b'',
        media_type='image/png'
    )


# ============================================================================
# FARCASTER MINI APP MANIFEST
# ============================================================================

@app.get("/.well-known/farcaster.json")
async def farcaster_manifest():
    """Farcaster Mini App Manifest - Required for Mini App registration"""
    return {
        "accountAssociation": {
            "header": "",
            "payload": "",
            "signature": ""
        },
        "frame": {
            "version": "next",
            "imageUrl": f"{BASE_URL}/static/images/og-image.png",
            "button": {
                "title": "Find Your Match 💕",
                "action": {
                    "type": "launch_frame",
                    "name": "Crypto Compatibility",
                    "url": BASE_URL,
                    "splashImageUrl": f"{BASE_URL}/static/images/splash.png",
                    "splashBackgroundColor": "#6366f1"
                }
            }
        },
        "name": "Crypto Compatibility Engine",
        "shortName": "CryptoMatch",
        "description": "Find your crypto soulmate! AI-powered personality analysis and smart matching for crypto degens 💎🤝",
        "homeUrl": BASE_URL,
        "iconUrl": f"{BASE_URL}/static/images/icon-512.png",
        "splashImageUrl": f"{BASE_URL}/static/images/splash.png",
        "splashBackgroundColor": "#6366f1",
        "webhookUrl": f"{BASE_URL}/api/webhook"
    }


@app.post("/api/webhook")
async def mini_app_webhook(request: Request):
    """Webhook endpoint for Mini App events"""
    try:
        body = await request.json()
        print(f"📱 Mini App webhook received: {body}")
        
        # Log to analytics if available
        try:
            await db.log_analytics('mini_app_event', 0, body)
        except:
            pass
        
        return {"status": "ok", "message": "Webhook received"}
    except Exception as e:
        print(f"⚠️ Webhook error: {e}")
        return {"status": "error", "message": str(e)}


# Placeholder images endpoints
@app.get("/images/{image_name}")
async def serve_image(image_name: str):
    """Serve static images"""
    image_path = f"static/images/{image_name}"
    if os.path.exists(image_path):
        return Response(
            content=open(image_path, 'rb').read(),
            media_type='image/png'
        )
    # Return placeholder if image doesn't exist
    return Response(content=b'', media_type='image/png')


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv('APP_PORT', 8000))
    host = os.getenv('APP_HOST', '0.0.0.0')
    
    print(f"""
    ╔══════════════════════════════════════════════╗
    ║  🚀 Crypto Compatibility Engine Started!    ║
    ║                                              ║
    ║  🌐 Server: http://{host}:{port}          ║
    ║  📚 Docs: http://{host}:{port}/docs        ║
    ║  ❤️  Frames: http://{host}:{port}/         ║
    ╚══════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
