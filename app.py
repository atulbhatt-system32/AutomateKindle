from ebooklib import epub
import os



# Read a web page and fetch html content
import requests
url ="https://dev.to/atulbhattsystem32/not-5-but-6-things-to-ask-before-joining-a-new-organisation-if-youre-a-dev-or-sde-2a99"
r = requests.get(url)
html_content = r.text

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, "html.parser")
text = soup.get_text()



# Create an ePUB book
book = epub.EpubBook()

# Set the metadata
book.set_identifier("mybook")
book.set_title("My Book")
book.set_language("en")


# Create a chapter and add it to the book
chapter = epub.EpubHtml(title="Chapter 1", file_name="ch1.html", lang="en")
chapter.content = text
book.add_item(chapter)

# Add the book to the list of items
book.spine = ['nav', chapter]

# Write the ePUB file
epub.write_epub("output.epub", book)


# Send the file to kindle

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Replace sender_email, recipient_email, and password with your own values

from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Access the environment variables
sender_email = os.environ["EMAIL_ADDRESS"]
password = os.environ["EMAIL_PASSWORD"]
email_host = os.environ["EMAIL_HOST"]
email_port = os.environ["EMAIL_PORT"]

recipient_email = os.environ["RECIEVER_EMAIL"]

# Create the email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = "Kindle Test"

# Add the .epub file as an attachment
with open("mybook.epub", "rb") as epub:
    part = MIMEBase("application", "octet-stream")
    part.set_payload((epub).read())

# Encode the attachment in base64 and add it to the email
encoders.encode_base64(part)
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {'input_file.epub'}",
)
message.attach(part)

# Connect to the email server and send the email
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(sender_email, password)
server.sendmail(sender_email, recipient_email, message.as_string())
server.quit()

print("success")

# LET's FIRE it's either a bug or success
# LET's Try Again


# In the next part we'll see how we can convert this epub to mobi format and send it to our kindle device.