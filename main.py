import discord
from discord.ext import commands
import datetime
from datetime import time
from selenium import webdriver
import re
import smtplib, ssl
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client= commands.Bot(command_prefix="!", intents = intents, description='Hi' ) # assigns the command prefix as being *!*
client.remove_command('help')# removes the command help
emails = list()

@client.event
async def on_ready(): #This code will run when the bot is first ran.
    global start_time #making the variable start_time a global variable because it is going to be used within other functions
    start_time = time.time() #using the time module to get he start time, as start_time is used later in the code to work out the up time of the bot

    bot_activity = discord.Game(name="Corona Virus Helpline ", type=3)#Assigns what the bot is playing (Coronavirus helpline) to the variable bot_activity
    await client.change_presence(status=discord.Status.online, activity=bot_activity)#Sets the bot's presence to online
    print("The bot is running") # outputs on the command line that the bot is running, this is more for debugging

    for server in client.guilds: # returns a generator that the bot can see in the server
        channel = discord.utils.get(server.text_channels) # assigns the bot to all the text channels on the server, and then stores in a variable
        message = "Hello, I am the Northumbria University Corona Virus Helpline\nType !help to get started" # defines the contents of the message

        await channel.send(content=message) # sends the contents of message

@client.event # a client event works out what event is an generates the objects that were sent by the event
async def on_member_join(ctx,member): # defines the name of the function and uses the parameters of member, to be called in the f string
    join = (f"{member} has joined the server.")# uses a f string to call the parameter *member*
    await ctx.send(join) # sends the contents of the variable *join*
@client.event
async def on_member_remove(ctx,member):
    await ctx.send((f"{member} has been removed from the server")) # uses a f string to call the parameter *member*


@client.event
async def on_command_error(ctx, error): #name of the event, with the parameter ctx and error. error being used in the detet
    if isinstance(error, commands.CommandNotFound): # this checks if the command that is inputted has been defined
        await ctx.send("Please input a valid command") # prompts the user that the command that they inputted is valid


@client.command(pass_context=True)
async def help(ctx):

    help = discord.Embed(colour = discord.Colour.blue())#This outlines how the embeded message is going to look.
    help.set_author(name='Northumbria University Coronavirus Helpline')#Outlines the heading of the embeded message
    #Below are the fields of the embeded message, the embeded message has the name on the top of the value and is not nline
    help.add_field(name="!symptoms", value="Returns the symptoms of the coronavirus", inline=False)# adds a field with the value, and doesn't the value on top of the name
    help.add_field(name='!temperature', value="Asks for your temperature and tells you if you need to get a test or not", inline=False)# adds a field with the value, and doesn't the value on top of the name
    help.add_field(name="!tutorial", value="Shows you a video tutorial on how to use the coronavirus tests", inline=False)# adds a field with the value, and doesn't the value on top of the name
    help.add_field(name="!info", value = "Opens the NHS Coronavirus web-page", inline=False)# adds a field with the value, and doesn't the value on top of the name
    help.add_field(name="!test", value = "Allows you to book a Coronavirus test", inline=False) # adds a field with the value, and doesn't the value on top of the name
    help.add_field(name="!other", value="More options")# adds another field with a value
    await ctx.send(embed=help)#Sends the embeded message when called.

@client.command(aliases=['temp'])
async def temperature(ctx):
    while True: # while true loop to make sure that the input is a number not a letter
        try:
            await ctx.send('Please enter your body temperature and I will decide if you should be getting a corona virus test.') # prompts the user of what this command does
            user_temp = await client.wait_for('message', check=lambda message: message.author == ctx.author) # checks that the author of the message is the rigt one
            user_temp = user_temp.content # takes the input of the user and stores it in a variable
            user_temp = int(user_temp) # turns the input from a string to an integer
        except ValueError:
            await ctx.send("Sorry i didn't understand that") # tells the user that it didn't understand the input
            continue # tells the code to continue to the next iteration of the loop
        else:
             break # breaks the loop
    if user_temp > 37: # if the user input was over 37 the code below would run
        response = "You have a temperature, it is advised that you get a coronavirus test." # this reponse
        await ctx.send(content=response) # this outputs the response
    elif user_temp == 37: # if the user input was equl to 37 the code below would run
        response = "Your body temperature is normal!\nHowever if you are showing any other symptoms of the coronavirus then you need to get a test." # this is the content of the response
        await ctx.send(content=response) # this outputs the response
    else: # if there was any other response, that was below 37 the code below would be executed
        response = "Your body temperature is low, you should go see a doctor." # this is text for the response
        await ctx.send(content=response) # this outputs the response



@client.command(pass_conext = True, aliases=['tut'])
async def tutorial(ctx): # defines the name of the command
    author = ctx.message.author # this defines the author, by taking the message that the user wrote in the channel
    message = "Below are the instructions on how to take the lateraly flow coronavirus test" # this is the contents of message 1
    message2 = "https://www.youtube.com/watch?v=kZhSPnnXyPo" # this is the contents of message 2
    await author.send(content = message) # sends the contents of message 1 to the author of the message, rather than the channel
    await author.send(content = message2) # sends the contents of message 2 to the author of the message, rather channel


@client.command(pass_context = True)
async def other(ctx):
    embed= discord.Embed(colour=discord.Colour.blue()) # this is the outline for the embeded message
    embed.set_author(name='Northumbria University Coronavirus Helpline') # sets the author of the embeded message
    embed.add_field(name = "!latency", value = "Returns the latency of the bot to the server", inline=False) # adds the field with the value next to it
    embed.add_field(name = "!uptime", value = "Returns the uptime of the bot", inline=False)# adds the field with the value next to it
    await ctx.send(embed=embed) # this sends the embeded message


@client.command(aliases = ['ping']) # marks the function as being a command, and the aliases are the other commands that could be used to call the function
async def latency(ctx):
    await ctx.send(f'The latency is: {round(client.latency*1000)}ms')#Returns the latency of the bot, original number is multiplyed by 1000 so that it is in millisecond


@client.command(pass_conext = True, aliases=['up', 'time']) #Marks a callback as wanting to receive the current context object as first argument. Also the aliases are the other commands thay could call the function
async def uptime(ctx):
    current_time=time.time() # takes the current time
    up_time = str(datetime.timedelta(seconds=(int(round(current_time - start_time))))) # works out the up time by taking the curernt time and then taking away the start time
    embed_uptime = discord.Embed(colour=discord.Colour.blue()) # sets out the embeded time
    embed_uptime.add_field(name="Uptime: ", value=up_time, inline=True) # adds the field
    embed_uptime.set_footer(text="Northumbria University Coronavirus Helpline Bot")# sets the footr
    try:
        await ctx.send(embed=embed_uptime) # sends the uptime
    except discord.HTTPException:
        await ctx.send("Current uptime: " + up_time) # creates an exceptoooon

@client.command(pass_context = True, aliases = ['information'])
async def info(ctx):
    await ctx.send("Below is the information about Coronavirus:\n\nhttps://www.nhs.uk/conditions/coronavirus-covid-19/") # opens the nhs web page


@client.command(pass_context = True) # this marks a callback as wanting to receive the current context object as first argument.
async def symptoms(ctx): # calls the function *symptoms* and also outlines the name of the function and the name of the command needed to call the function
    with open('symptoms.txt', 'r') as file:
        data = file.read().replace('\n', '') #openn the file in read mode and assigns the contents to a variablex
        await ctx.send(data)

@client.command(pass_context = True)
async def vaccine(ctx):
    await ctx.send("Have you had the cornonavirus vaccine?")
    user_response = await client.wait_for('message', check=lambda message: message.author == ctx.author)  # checks the user inputing the date is the correct user
    user_response = user_response.content  # assigns the user input to a variable
    user_response = user_response.lower()
    if user_response == "yes":
        await ctx.send("Brilliant. Make sure that you book the second dose")
    elif user_response == "no":
        await ctx.send("Clikc the link below to see if you are the elligible to the coronavirus vaccine: \n\nhttps://www.nhs.uk/conditions/coronavirus-covid-19/coronavirus-vaccination/coronavirus-vaccine/")



@client.command(pass_context = True) # defines it as being a command and not a client event
async def test(ctx): # defines the name of the function and also the name of the command needed to run it
    await ctx.send("In order to book your COVID-19 test, we require some basic information")
    time.sleep(0.5) # stops the code from executing for 0.5 seconds
    await ctx.send("Please enter your full name") # prompts the user to input their full name
    user_name = await client.wait_for('message', check=lambda message: message.author == ctx.author) # checks the user inputing the date is the correct user
    user_name = user_name.content # assigns the user input to a variable
    while True: #An infinite while-loop, will execute code repeatedly as long as a given boolean condition evaluates to True
        try:
            await ctx.send("Please enter your date of birth\nFormat: DD-MM-YYYY") # prompts the suer to input a date and gives the required formatr
            format = "%d-%m-%Y" # this is reuquired format for the date
            user_dob = await client.wait_for('message', check=lambda message: message.author == ctx.author) # checks that the user inputting the email is the correrct user
            user_dob = user_dob.content # assigns the user input to a variable
            datetime.datetime.strptime(user_dob, format) # this creates a datetime object from a string representing a date and a corresponding format string.
            break #breaks the while loop
        except ValueError:
            await ctx.send("This is not the correct format") # informs the user that the email is invalid
    while True: #An infinite while-loop, will execute code repeatedly as long as a given boolean condition evaluates to True
        try:
            await ctx.send("Please enter your email address\nFormat: email@example.com") # prompts the user to input a email and gives the desired format
            regex = "^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$" # this is the regex for a valid email
            user_email = await client.wait_for('message', check=lambda message: message.author == ctx.author) #checks that the user inputting is the correct user
            user_email = user_email.content # assigns the user input to the variable
            if re.search(regex, user_email): #checks the email regex against the formatting of the email that the user inputted
                 break #breaks te while loop

        except NameError: # the code below is ran if the formatting of the email is incorrect
            await ctx.send("Invalid email") # prompts the user that the email they inputted is invalid

    await ctx.send("Please enter the first line of your address") # asks the user for the first line of their address
    user_address = await client.wait_for('message', check=lambda message: message.author == ctx.author) # checks that the user is the correct user
    user_address = user_address.content # assigns the user input to the variable
    time.sleep(0.5) #stops the program from running for 0.5 seconds
    while True: #An infinite while-loop, will execute code repeatedly as long as a given boolean condition evaluates to True
        try:
            await ctx.send("Please enter your postcode\nFormat: AB123 C45") # asks the user to input their postocde and gives the format required
            postcode_regex = "([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})" # this is the regex for a uk postcode
            user_postcode = await client.wait_for('message', check=lambda message: message.author == ctx.author) #checks that the user is the correct user
            user_postcode = user_postcode.content # assigns what the user input to the variable
            if re.search(postcode_regex,user_postcode):# checks the postcode regex against the user input postcode, if the formatting is correc the loop will break
                break # breaks the infinite loop
        except NameError: # the code below will run if the formatting of the user postcode is incorrect
            await ctx.send("Invalid postcode") # prompts the user that their input is not valid

    while True:#An infinite while-loop, will execute code repeatedly as long as a given boolean condition evaluates to True
        try:
            await ctx.send("Please enter a valid UK number from which we can contact you") # asks for a uk telephone number
            phone_regex = "^(07[\d]{8,12}|447[\d]{7,11})$" # this is the regex for a uk phon number, this will act as as the verifier that the user inputs a vaid phone number
            user_phone= await client.wait_for('message', check=lambda message: message.author == ctx.author)#verify that the user is the corerct user
            user_phone = user_phone.content # assigns the user input to the variable
            if re.search(phone_regex, user_phone): #this checks the phone regex against the user, and if the formatting is correct then the while loop will break
                break #breaks the while loop
        except NameError: #the code below will run if the phone number is not valid
            await ctx.send("Invalid phone number")
    while True:#An infinite while-loop, will execute code repeatedly as long as a given boolean condition evaluates to True
        try:
            await ctx.send("Please enter the day of the week that you would like to have your COVID-19 test\n1. Monday\n2. Tuesday\n3. Wednesday\n4. Thursday\n5. Friday")
            user_choice = await client.wait_for('message', check=lambda message: message.author == ctx.author) # verfies that the message author is the corerct user
            user_choice = user_choice.content # assigns the string that the user inputted to the variable
            user_choice = int(user_choice) # changes the user input froma string to an integer, stops run-time errors
            if user_choice == 1:
                user_choice = "Monday"#changes the content of the *user_choice*, this is for the formatting of the email
                break
            if user_choice == 2:
                user_choice = "Tuesday"
                break
            if user_choice == 3:
                user_choice = "Wednesday"
                break
            if user_choice == 4:
                user_choice = "Thursday"
                break
            if user_choice == 5:
                user_choice = "Friday"
                break

        except NameError:
            await ctx.send("Please enter a valid day of the week") # a prompt to ask th suer to enter a valid input

    while True: #An infinite while-loop, will execute code repeatedly as long as a given boolean condition evaluates to True
        try:
            await ctx.send("Please enter a time when you would like to book your COIVD test for\n1. 09:00\n2. 10:00\n3. 11:00\n4. 12:00\n5. 13:00\n6. 14:00\n7. 15:00\n8. 16:00\n9. 17:00")
            user_time = await client.wait_for('message', check=lambda message: message.author == ctx.author) #this verifies the message author is the correct user
            user_time = user_time.content # assigns the string that the user inputted to the variable
            user_time = int(user_time)#changes the user input from a string to an integer, stops run-time errors
            if user_time == 1:
                user_time = "9:00" # this changes the variable content, this is for the formatting of the email that is sent to the user
                break #this breaks the loop
            if user_time == 2:
                user_time = "10:00"
                break
            if user_time == 3:
                user_time = "11:00"
                break
            if user_time == 4:
                user_time = "12:00"
                break
            if user_time == 5:
                user_time = "13:00"
                break
            if user_time == 6:
                user_time = "14:00"
                break
            if user_time == 7:
                user_time = "15:00"
                break
            if user_time == 8:
                user_time = "16:00"
                break
            if user_time == 9:
                user_time = "17:00"
                break
        except NameError:
            await ctx.send("Please enter a valid time do book your COVID test")# if the user doesn't select a time in the correct format this code will run, prompting the user to select a proper time

    sender_email = "sender email goes here""
    sender_password = "sender passowrd goes here"
    receiver_email = user_email #will use the email that the user inputted as the receiver email


    message = MIMEMultipart("alternative")#this  will make the email into multiple arts
    message["Subject"] = "Coronavirus Helpline - email conformation"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text version of the message, no need to use HTML as it is only one sentence
    text = ("Hello\n\n\nThis is email conformation that: " + user_name + " has a coronavirus test booked for " + user_choice + " at " + str(user_time))


    # this will turn the message into plain MIMEText objects
    part = MIMEText(text, "plain")



    #this will attatch the message for the client to send
    message.attach(part)


    # this will create a secure connection to the server and then sending the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)#will use the email and password to login
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
























client.run('client token goes here')
