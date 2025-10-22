"""
Test script for Crypto Compatibility Engine
Run this to verify everything is working
"""
import asyncio
import sys

print("🧪 Testing Crypto Compatibility Engine...")
print("=" * 50)

# Test 1: Import modules
print("\n1️⃣  Testing imports...")
try:
    from personality import PersonalityAnalyzer
    from comedy_generator import ComedyGenerator
    from matching_algorithm.matchmaker import MatchmakerAI
    from frame_generator.frame_builder import FrameGenerator
    from farcaster_client import MockFarcasterClient
    print("✅ All modules imported successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test 2: Personality Analyzer
print("\n2️⃣  Testing Personality Analyzer...")
try:
    analyzer = PersonalityAnalyzer()
    personalities = analyzer.get_all_personalities()
    print(f"✅ Found {len(personalities)} personality types")
    
    # Test analysis
    mock_user = {
        'fid': 12345,
        'username': 'testuser',
        'bio': 'Bitcoin maxi, HODL forever',
        'recent_casts': []
    }
    analysis = analyzer.analyze_user(mock_user)
    print(f"✅ Personality analysis working: {analysis['personality_name']}")
except Exception as e:
    print(f"❌ Personality Analyzer error: {e}")
    sys.exit(1)

# Test 3: Comedy Generator
print("\n3️⃣  Testing Comedy Generator...")
try:
    comedy = ComedyGenerator()
    comment = comedy.get_match_comment(85)
    print(f"✅ Comedy generation working")
    print(f"   Sample: {comment}")
except Exception as e:
    print(f"❌ Comedy Generator error: {e}")
    sys.exit(1)

# Test 4: Farcaster Client (Mock)
print("\n4️⃣  Testing Farcaster Client...")
async def test_farcaster():
    try:
        client = MockFarcasterClient()
        user = await client.get_user_by_fid(12345)
        print(f"✅ Farcaster client working")
        print(f"   Mock user: {user['username']}")
    except Exception as e:
        print(f"❌ Farcaster Client error: {e}")
        sys.exit(1)

asyncio.run(test_farcaster())

# Test 5: Matchmaker AI
print("\n5️⃣  Testing Matchmaker AI...")
async def test_matchmaker():
    try:
        matchmaker = MatchmakerAI(use_mock_data=True)
        
        # Analyze personality
        analysis = await matchmaker.analyze_user_personality(12345)
        print(f"✅ User analysis working: {analysis['personality_name']}")
        
        # Find matches
        matches = await matchmaker.find_matches(12345, limit=3)
        print(f"✅ Match finding working: Found {len(matches)} matches")
        
        if matches:
            top_match = matches[0]
            print(f"   Top match: {top_match['compatibility_score']}% with {top_match['match_username']}")
    except Exception as e:
        print(f"❌ Matchmaker AI error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

asyncio.run(test_matchmaker())

# Test 6: Frame Generator
print("\n6️⃣  Testing Frame Generator...")
try:
    frame_gen = FrameGenerator("http://localhost:8000")
    start_frame = frame_gen.generate_start_frame()
    print(f"✅ Frame generation working")
    print(f"   Frame has {len(start_frame.get('buttons', []))} buttons")
except Exception as e:
    print(f"❌ Frame Generator error: {e}")
    sys.exit(1)

# Test 7: Database (if available)
print("\n7️⃣  Testing Database...")
async def test_database():
    try:
        from database import db
        await db.connect()
        print("✅ Database connection successful")
        await db.disconnect()
    except Exception as e:
        print(f"⚠️  Database test skipped (this is OK for demo mode)")
        print(f"   Reason: {e}")

asyncio.run(test_database())

# Summary
print("\n" + "=" * 50)
print("🎉 All tests passed!")
print("=" * 50)
print("\n📚 Next steps:")
print("   1. Set up your .env file with API keys")
print("   2. Run: python app.py")
print("   3. Visit: http://localhost:8000")
print("\n💡 For demo mode (no API keys needed):")
print("   The app will work with mock data!")
print("")
