from app import app

# Export the app for Vercel
app = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)