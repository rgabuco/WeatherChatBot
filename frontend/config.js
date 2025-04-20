// AWS Configuration
const config = {
    aws: {
        region: 'us-east-1', // Replace with your AWS region
        credentials: {
            accessKeyId: 'YOUR_AWS_ACCESS_KEY_ID', // Your access key
            secretAccessKey: 'YOUR_AWS_SECRET_ACCESS_KEY' // Your secret key
        }
    },
    lex: {
        botName: 'YOUR_BOT_NAME', // Replace with your bot name
        v2BotAliasId: 'YOUR_BOT_ALIAS_ID', // Get this from Lex console under Aliases
        v2BotId: 'YOUR_BOT_ID'         // Get this from Lex console Bot overview
    }
};

// Export configuration
export default config; 