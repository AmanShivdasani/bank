from twilio.rest import Client
import os
import math
import random

# putting necessary information regarding twilio account
account_sid = "AC1783aec77916e6d3a2a254047f076905"
auth_token = '913ea5555b98f6a82a82b0eb4668c4de'
client = Client(account_sid, auth_token)

# generating random otp
digits = "0123456789"
OTP = ""
for i in range(6):
    OTP += digits[math.floor(random.random() * 10)]
otp = OTP
msg = str(otp) + " is your OTP"

# getting number to sent otp
num_to_send = input("Enter number to send OTP: ")

message = client.messages.create(
    body=msg,
    from_="+91 9116927782",
    to=num_to_send)