from ebooklib import epub
import os



# Read a web page and fetch html content
import requests
url ="https://the-soulful-entrepreneur.beehiiv.com/p/attention-new-oil"
r = requests.get(url)
html_content = r.text

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, "html.parser")


# Find the heading of the page
heading = soup.find("h1")
#get heading content with the tags
heading = str(heading)

# Find all the text elements on the page
text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li','img'])





# Create a string to hold the text
text = ""

# Create an ePUB book
book = epub.EpubBook()

# Loop through the text elements and add them to the string
for element in text_elements:
    if element.name == "img":
        img_url = element['src']
        img_name = img_url.split("/")[-1]
        img_data = requests.get(img_url).content
        element['src'] = img_name

        image = epub.EpubItem(file_name=img_name, content=img_data, media_type='image/jpeg')
        book.add_item(image)


    text += str(element)


# Set the metadata
book.set_identifier("mybook")
book.set_title("My Book")
book.set_language("en")


# Create a chapter and add it to the book
chapter = epub.EpubHtml(title="Chapter 1", file_name="ch1.html", lang="en")
chapter.content = text

#preserve the new lines
chapter.content = chapter.content.replace("\n", "<br/>")
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

