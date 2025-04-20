# Weather Chat Bot Frontend

A modern web interface for interacting with an AWS Lex V2 weather chatbot.

## Features
- Real-time chat interface with AWS Lex V2
- Modern, responsive design
- Typing indicators
- Message history
- Mobile-friendly layout

## Prerequisites
- AWS Account with access to Amazon Lex V2
- OpenWeather API key (get it from [OpenWeather](https://openweathermap.org/api))
- A configured Lex V2 bot with weather intent
- AWS IAM user with appropriate permissions

## Setup Instructions

### 1. AWS Lex V2 Configuration
1. Create and configure your Lex V2 bot in AWS Console
2. Build and publish a version of your bot
3. Create an alias (e.g., "Prod") for the published version
4. Note down the following values from your Lex console:
   - Bot ID
   - Bot Alias ID
   - Bot Name

### 2. AWS IAM Setup
1. Create an IAM user in AWS Console:
   - Go to IAM service
   - Click "Users" → "Create user"
   - Enter a user name
   - Select "Access key - Programmatic access"

2. Attach required managed policies:
   - In the "Set permissions" step, choose "Attach existing policies directly"
   - Search and select the following AWS managed policies:
     - `AmazonLexFullAccess`
     - `AmazonS3FullAccess`
   - Click "Next" and complete user creation

3. Generate and secure credentials:
   - After user creation, you'll see the Access Key ID and Secret Access Key
   - Download the credentials CSV file or copy the keys
   - Store these credentials securely - you'll need them for the frontend configuration
   - Note: This is your only chance to view/download the secret key

4. Best practices for security:
   - Never share or commit your access keys
   - Consider using AWS Secrets Manager or Parameter Store for production
   - Regularly rotate your access keys
   - Enable MFA for the IAM user

### 3. OpenWeather API Setup
1. Sign up for an OpenWeather account
2. Generate an API key from your account dashboard
3. Update the Lambda function with your API key:
   - Open `lambda_function.py`
   - Replace `YOUR_OPENWEATHER_API_KEY` with your actual API key

### 4. Frontend Configuration
1. Update `config.js` with your AWS credentials and bot details:
   ```javascript
   const config = {
       aws: {
           region: 'YOUR_REGION',
           credentials: {
               accessKeyId: 'YOUR_AWS_ACCESS_KEY_ID',
               secretAccessKey: 'YOUR_AWS_SECRET_ACCESS_KEY'
           }
       },
       lex: {
           botName: 'YOUR_BOT_NAME',
           v2BotAliasId: 'YOUR_BOT_ALIAS_ID',
           v2BotId: 'YOUR_BOT_ID'
       }
   };
   ```

### 5. Lambda Function Setup
1. Create a new Lambda function
2. Copy the content of `lambda_function.py` code
3. Add the following environment variable:
   - Key: `OPENWEATHER_API_KEY`
   - Value: Your OpenWeather API key
4. Add the requests layer:
   1. Go to Layers → Create layer
   2. Upload the provided `requests-layer.zip` file from this repository
   3. Choose compatible runtimes (Python 3.13, etc.)
   4. Create the layer
   5. Go back to your Lambda function
   6. Click on Layers → Add a layer
   7. Choose "Custom layers" and select your created requests layer
   8. Add the layer to your function

### 6. S3 Bucket Setup (for hosting)
1. Create an S3 bucket
2. Enable static website hosting
3. Add CORS configuration:
   ```json
   [
       {
           "AllowedHeaders": ["*"],
           "AllowedMethods": ["GET", "POST"],
           "AllowedOrigins": ["*"],
           "ExposeHeaders": []
       }
   ]
   ```
4. Add bucket policy for public access:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "PublicReadGetObject",
               "Effect": "Allow",
               "Principal": "*",
               "Action": "s3:GetObject",
               "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
           }
       ]
   }
   ```
5. Upload the following files from the `frontend` directory of this repository to your S3 bucket:
   - `app.js` - Main application logic
   - `config.js` - AWS configuration (make sure to update with your credentials)
   - `index.html` - Main HTML file
   - `styles.css` - Application styling

## Security Considerations
- Never commit actual credentials to version control
- Keep your OpenWeather API key secure
- Consider using AWS Cognito for authentication in production //ToDO
- Implement proper CORS restrictions in production
- Regular security audits and updates

## Local Development
1. Clone the repository
2. Update configuration files with your AWS details
3. Go to your S3 bucket and open the link to your chatbot under "Bucket website endpoint"

## Deployment
1. Upload all files to your S3 bucket:
   - index.html
   - styles.css
   - app.js
   - config.js
2. Access your website through the S3 bucket's static website hosting URL

## Troubleshooting
1. Check browser console for errors
2. Verify AWS credentials and permissions
3. Ensure Lex bot is properly built and published
4. Verify CORS configuration if accessing from different domain
5. Check network tab for API call details

## Common Issues
- 404 Error: Check Bot ID and Alias ID
- Authentication errors: Verify AWS credentials
- CORS errors: Check S3 bucket CORS configuration
- Bot not responding: Verify Lex bot status and permissions
- Weather not working: Verify OpenWeather API key

## Support
For issues and feature requests, please create an issue in the repository.
