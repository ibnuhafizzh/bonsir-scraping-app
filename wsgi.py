from app import app

# Vercel expects 'app' to be called as a serverless function
def handler(event, context):
    return app(event, context)
