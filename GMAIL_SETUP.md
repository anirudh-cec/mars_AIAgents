# Gmail API Setup Instructions

To enable Gmail integration for downloading email attachments, you need to set up Google API credentials.

## Step 1: Enable Gmail API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click on it and press "Enable"

## Step 2: Create Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in the required fields:
     - App name: "Mars AI Agents"
     - User support email: your email
     - Developer contact email: your email
   - Add scopes: `https://www.googleapis.com/auth/gmail.readonly`
   - Add test users if needed (add the Gmail account you want to access)
4. Create OAuth client ID:
   - Application type: "Desktop application"
   - Name: "Mars AI Agents Gmail Client"
5. Download the credentials file

## Step 3: Setup Credentials File

1. Rename the downloaded file to `credentials.json`
2. Place it in the root directory of your project:
   ```
   /Users/anirudh/Downloads/Mars_Project/mars_AIAgents/credentials.json
   ```

## Step 4: Test the Setup

1. Start the FastAPI server:
   ```bash
   cd /Users/anirudh/Downloads/Mars_Project/mars_AIAgents
   python api_server.py
   ```

2. In another terminal, start the React app:
   ```bash
   cd /Users/anirudh/Downloads/Mars_Project/mars_AIAgents
   npm start
   ```

3. Click "Start Processing" button
4. On first run, it will open a browser for OAuth authentication
5. Grant the requested permissions
6. The system will then check for emails from `demotest.tcs@gmail.com`

## Important Notes

- The `credentials.json` file should never be committed to version control
- The first authentication will create a `token.json` file for future use
- The app will only read emails (readonly access)
- Only emails from `demotest.tcs@gmail.com` with attachments are processed
- Attachments are saved to the `data/` folder, organized by date

## Troubleshooting

### Common Issues:

1. **"credentials.json not found"**
   - Ensure the file is in the correct location
   - Check file permissions

2. **"OAuth error"**
   - Verify the OAuth consent screen is configured
   - Add your Gmail account as a test user
   - Ensure Gmail API is enabled

3. **"No emails found"**
   - Send a test email with attachment from `demotest.tcs@gmail.com`
   - Check if the email has attachments
   - Verify the date range (last 24 hours by default)

4. **Port conflicts**
   - FastAPI runs on port 8000
   - React runs on port 3000
   - Ensure both ports are available

## Security

- Never share your `credentials.json` or `token.json` files
- Use appropriate firewall rules if deploying to production
- Consider using service account credentials for production deployments