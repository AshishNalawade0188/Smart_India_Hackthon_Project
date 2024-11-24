import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# File paths
input_file = r"E:\Project\feedback\feedback_with_sentiment.csv"

# Email configuration
sender_email = "kutemanjusha4@gmail.com"
receiver_email = "ashishnalawade683@gmail.com"
email_password = "ryuu mpuz nkpk xipd"
# Replace with your email password (use app-specific password if needed)

# Function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Process the dataset and update sentiment
def process_dataset():
    try:
        # Load the dataset
        if not os.path.exists(input_file):
            print(f"File '{input_file}' not found.")
            return None

        data = pd.read_csv(input_file, encoding='utf-8')

        # Analyze sentiment if not already analyzed
        if 'Sentiment' not in data.columns:
            data['Sentiment'] = data['Feedback'].apply(analyze_sentiment)

        # Count sentiment values
        sentiment_counts = data['Sentiment'].value_counts()

        # Save updated dataset
        data.to_csv(input_file, index=False, encoding='utf-8')
        return data, sentiment_counts
    except Exception as e:
        print(f"Error processing dataset: {e}")
        return None, None

# Generate a pie chart
def generate_pie_chart(sentiment_counts):
    try:
        plt.figure(figsize=(6, 6))
        plt.pie(
            sentiment_counts,
            labels=sentiment_counts.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=['#28a745', '#dc3545', '#ffc107']
        )
        plt.title("Sentiment Analysis of Feedback")
        plt.savefig("sentiment_pie_chart.png")  # Save the chart as an image
        plt.show()
    except Exception as e:
        print(f"Error generating pie chart: {e}")

# Generate recommendations
def generate_recommendations(sentiment_counts):
    recommendations = ""
    total_feedback = sentiment_counts.sum()
    positive = sentiment_counts.get('Positive', 0)
    negative = sentiment_counts.get('Negative', 0)
    neutral = sentiment_counts.get('Neutral', 0)

    recommendations += f"Sentiment Summary:\n"
    recommendations += f"- Total Feedback: {total_feedback}\n"
    recommendations += f"- Positive: {positive}\n"
    recommendations += f"- Negative: {negative}\n"
    recommendations += f"- Neutral: {neutral}\n\n"

    if negative > positive:
        recommendations += "Recommendations:\n- High negative feedback detected. Consider addressing user complaints and improving services.\n"
    elif positive > negative:
        recommendations += "Recommendations:\n- Feedback is mostly positive. Continue the current strategies and reward loyal customers.\n"
    else:
        recommendations += "Recommendations:\n- Feedback is balanced. Focus on converting neutral and negative feedback into positive experiences.\n"

    print(recommendations)
    return recommendations

# Send an email with recommendations
def send_email(recommendations):
    try:
        # Create email message
        subject = "Feedback Analysis and Recommendations"
        body = recommendations
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Attach pie chart image
        filename = "sentiment_pie_chart.png"
        if os.path.exists(filename):
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            msg.attach(part)

        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main script
if __name__ == "__main__":
    data, sentiment_counts = process_dataset()
    if sentiment_counts is not None:
        generate_pie_chart(sentiment_counts)
        recommendations = generate_recommendations(sentiment_counts)
        send_email(recommendations)
