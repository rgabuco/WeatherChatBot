# Weather Chat Bot Project

The Weather Chat Bot is a web application that combines AWS Lex V2's conversational AI with OpenWeather API to provide real-time weather information through a natural chat interface. Users can inquire about weather conditions worldwide using natural language, with the system capable of understanding various query formats and providing detailed weather reports including temperature, humidity, wind speed, and sunrise/sunset times. The application features a responsive design that works seamlessly across desktop and mobile devices, with a modern interface that includes typing indicators and real-time updates to enhance user experience.

## Features

### Conversational Capabilities
- Natural language processing for weather queries using AWS Lex V2
- Context-aware conversations with country and city recognition
- Intelligent city suggestions when only a country is specified
- Support for various query formats (direct city, city-country pairs, abbreviations)
- Helpful responses for unknown locations or invalid inputs

### Weather Information
- Real-time weather data from OpenWeather API
- Temperature reporting in Celsius
- Detailed weather conditions and descriptions
- Humidity and wind speed information
- Sunrise and sunset times for locations
- Smart weather descriptions based on current conditions

### Location Support
- Global coverage for major cities worldwide
- Support for city-country pair queries (e.g., "Paris, France")
- Recognition of common city abbreviations (NYC, LA, SF, etc.)
- Comprehensive country code mapping (200+ countries)
- Major city suggestions for supported countries

### User Interface
- Responsive web design for desktop and mobile devices
- Real-time chat interface
- Typing indicators for better user experience
- Clean and modern styling
- Mobile-friendly layout

### Technical Features
- AWS Lambda integration for backend processing
- Error handling and graceful fallbacks
- Environment variable configuration for API keys
- CORS-enabled for cross-origin requests
- S3 static website hosting support

## Technology Stack

- **Frontend Technologies**
  - HTML5, CSS3, JavaScript (ES6+)
  - AWS SDK for JavaScript v3
  - Responsive design with modern CSS

- **Backend & Cloud Services**
  - AWS Lambda (Python 3.13)
  - AWS Lex V2 for Natural Language Processing
  - Amazon S3 for static web hosting
  - AWS IAM for access management

- **External Services & Libraries**
  - OpenWeather API for real-time weather data retrieval
  - Python Requests library
  - CORS configuration
  - Environment variables

## Sample Prompts
Here are valid examples you can try with the chatbot:

1. Basic City Queries
- "Weather in Tokyo"
- "What's the weather in New York"
- "How's the weather in London"
- "Temperature in Paris"
- "Current temperature in Paris"

2. City with Country Format
- "Weather in Paris, France"
- "Temperature in Tokyo, Japan"
- "What's the weather in Rome, Italy"
- "How's the weather in Berlin, Germany"

Note: The chatbot can understand variations of prompts using country and will help suggest major cities if a location is not found.

3. Country Format
- "Weather in France"
- "Temperature in Japan"
- "What's the weather in Italy"
- "How's the weather in Germany"

## Prerequisites
- AWS Account with access to Amazon Lex V2
- OpenWeather API key (get it from [OpenWeather](https://openweathermap.org/api))
- A configured Lex V2 bot with weather intent
- AWS IAM user with appropriate permissions

## Setup Instructions

### 1. Lambda Function Setup
1. Create a new Lambda function:
   - Go to AWS Lambda console
   - Click "Create function"
   - Choose "Author from scratch"
   - Name your function (e.g., "WeatherBotFunction")
   - Select Runtime: Python 3.9 or later
   - Create the function

2. Copy the content of `lambda_function.py` code into the function

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

5. Configure Lambda permissions:
   - In the Configuration tab, select "Permissions"
   - Click on the execution role
   - Add the following managed policies:
     - `AWSLexRunBotsPolicy`
     - `AWSLambdaBasicExecutionRole`

### 2. AWS Lex V2 Configuration
1. Create and configure your Lex V2 bot in AWS Console
2. Build and publish a version of your bot
3. Create an alias (e.g., "Prod") for the published version
4. Link the Lambda function:
   - Go to your bot's "Languages" section
   - Under "Source and voice", select "AWS Lambda function"
   - Choose the Lambda function you created
   - Click "Save"
5. Note down the following values from your Lex console:
   - Bot ID
   - Bot Alias ID
   - Bot Name

### 3. AWS IAM Setup
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

### 4. OpenWeather API Setup
1. Sign up for an OpenWeather account
2. Generate an API key from your account dashboard
3. Update the Lambda function with your API key:
   - Open `lambda_function.py`
   - Replace `YOUR_OPENWEATHER_API_KEY` with your actual API key

### 5. Frontend Configuration
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


## Testing the chatbot with Postman
1. Set up the request:
   - Method: POST
   - URL: `https://runtime-v2-lex.{REGION}.amazonaws.com/bots/{BOT_ID}/botAliases/{ALIAS_ID}/botLocales/en_US/sessions/{SESSION_ID}/text`
   - Replace placeholders:
     - `{REGION}`: Your AWS region (e.g., us-east-1)
     - `{BOT_ID}`: Your Lex bot ID
     - `{ALIAS_ID}`: Your bot alias ID
     - `{SESSION_ID}`: Any unique session identifier

2. Add AWS authentication:
   - Type: AWS Signature
   - AccessKey: Your AWS access key
   - SecretKey: Your AWS secret key
   - AWS Region: Your region
   - Service Name: lex
   - Session Token: Leave empty unless using temporary credentials

3. Add request body:
   ```json
   {
       "text": "What's the weather in London?",
       "sessionId": "test"
   }
   ```

4. Add headers:
   - Content-Type: application/json
   - Accept: application/json

5. Common validation errors:
   - "Value at 'text' failed to satisfy constraint": Make sure to use "text" (not "inputText") in request body
   - "Member must not be null": The "text" field cannot be empty
   - "SessionId must not be null": Make sure to include a sessionId

6. Common response codes:
   - 200: Successful request
   - 400: Invalid request parameters
   - 403: Authentication failed
   - 404: Bot/alias not found

## Common Issues
- 404 Error: Check Bot ID and Alias ID
- Authentication errors: Verify AWS credentials
- CORS errors: Check S3 bucket CORS configuration
- Bot not responding: Verify Lex bot status and permissions
- Weather not working: Verify OpenWeather API key

## Support
For issues and feature requests, please create an issue in the repository.
