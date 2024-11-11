# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from azure.ai.textanalytics import TextAnalyticsClient


class EchoBot(ActivityHandler):
    def __init__(self, text_analytics_client: TextAnalyticsClient):
        super().__init__()
        self.text_analytics_client = text_analytics_client

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text

        # Analyze sentiment of the user's message
        response = self.text_analytics_client.analyze_sentiment([user_message])
        sentiment = response[0].sentiment
        confidence_scores = response[0].confidence_scores

        # Construct a response message based on sentiment analysis
        sentiment_message = (
            f"Sentiment: {sentiment}\n"
            f"Confidence Scores - Positive: {confidence_scores.positive:.2f}, "
            f"Neutral: {confidence_scores.neutral:.2f}, Negative: {confidence_scores.negative:.2f}"
        )
        

        # Send both echo and sentiment analysis response
        await turn_context.send_activity(MessageFactory.text(f"Echo: {user_message[::-1]}"))
        await turn_context.send_activity(MessageFactory.text(sentiment_message))
