import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import os
import random
import smtplib
import pywhatkit as kit
import pickle
import cv2
import pyjokes
import pyautogui
import requests
import time
import instadownloader
import PyPDF2


engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices') #getting details of current voice
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio) 
    engine.runAndWait() #Without this command, speech will not be audible to us.

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Veer")
    elif hour>=12 and hour<18:
        speak("Goodafternoon Veer")
    else:
        speak("Goodevening Veer")
    
   # speak("I am your virtual Assistant")
    speak("Please tell me how may i help you ")

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")  
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.
    except Exception as e:
        # print(e)    
        print("Say that again please...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query

def message(name):
    filea=open("contact1.bat","rb")
    r=pickle.load(filea)
    if name in r:
        speak("What's your message sir?")
        m1=takeCommand().lower()
        speak(f"sendind message to {name}")
        kit.sendwhatmsg_instantly(r[name],m1)
        speak("Message sent succesfully ")
    else:
        speak("Unable to send the message")
    filea.close()

def google():
    speak("What should i search on google?")
    c1=takeCommand().lower()
    speak("Searching google")
    webbrowser.open(f"{c1}")

def xxsendemail12():
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.login('veer47003@gmail.com','Veertiarra@2005')
    try:
        speak("Sure sir whom you want to send the email?")
        reciever=takeCommand().lower()
        fileemail=open("email1.bat","rb")
        content=pickle.load(fileemail)
        if reciever in content:
            speak("What is your message sir?")
            msg=takeCommand().lower()
            server.sendmail('veer47003@gmail.com',content[reciever],msg)
            speak(f"Message sent succesfully to {reciever} sir!")
            server.close()
            fileemail.close()
        else:
            speak(f"No reciever found with name {reciever}")
    except Exception as e:
        speak("Error unable to send message")
    
def news():
    main_url='https://newsapi.org//v2//top-headlines?sources-techcrunch&apiKey=73d168358a504b9481554e9958376eaf'
    main_page=requests.get(main_url).json()
    articles=main_page["articles"]
    head=[]
    day=["first","second","third","fourth","fifth","sixth","seventh","eight","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        speak(f"today's {day[i]} news is : {head[i]}")
        
def getloacation():
    try:
        ipad=requests.get('https://api.ipyfy.org').text
        print(ipad)
        url='https://get.geojs.io/v1/ip/geo/'+ipad+'.json'
        geo_requests=requests.get(url)
        geo_data=geo_requests.json()
        #print(geo_data)
        city=geo_data['city']
        country=geo_data['country']
        speak(f"Sir i am not sure but i think we are at {city} city of {country}")
    except Exception as e:
        speak("Sorry sir due to network issues i am unable to find the data")
        pass
        
def instagram():
    speak("Sir please enter the user name ")
    print()
    name=input("Enter username here : ")
    speak("Please wait while i find the profile")
    webbrowser.open(f"www.instagram.com/{name}")
    speak("Sir here is the profile")
    time.sleep(5)
    speak("Sir would you like to download the profile picture?")
    condition=takeCommand().lower()
    if 'yes' in condition:
        mod=instadownloader.instaloader()
        mod.download_profile(name,profile_pic_only=True)
        speak("Picture Downloaded succesfully")
    else:
        pass
    
def screenshot():
    speak("Sure sir, please tell me the name  for this file")
    name=takeCommand().lower()
    speak("Please hold for a second Taking screenshot")
    img=pyautogui.screenshot()
    img.save(f"{name}.png")
    speak("Screenshot saved !!")
    
def pdf_reader():
    speak("Sure sir")
    with open('CCE.pdf', "rb") as book:
        pdfreader = PyPDF2.PdfReader(book)
        pages = len(pdfreader.pages)
        speak(f"The total number of pages in this PDF is {pages}")
        speak("Please enter the page number I have to read")
        print()
        pg = int(input("Enter the page number: "))
        page = pdfreader.pages[pg]
        text = page.extract_text()
        print(text)
        speak(text)






if __name__ == "__main__":
    wishme()
    while True:
    
        query = takeCommand().lower() #Converting user query into lower case

        # Logic for executing tasks based on query
        if 'wikipedia' in query:  #if wikipedia found in the query then this block will be executed
            speak('Sure Sir Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            print(results)
            speak(results)
        
        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            google()
            
        elif 'play music' in query:
            speak("playing music...")
            music_dir='C:\\Users\\Veer Jain\\Desktop\\Personal\\music'
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[0]))

        elif 'the time' in query:
            strTime=datetime.datetime.now().strftime("%H:%m:%S")
            speak(f"Sir the time is {strTime}")
            print(strTime)

        
        elif 'send message' in query:
            speak("Sure sir, whom do you want to send?")
            recipient_name = takeCommand().lower()
            message(recipient_name)

        
        elif 'open camera' in query:
            cap=cv2.VideoCapture(0)
            while True:
                ret,img=cap.read()
                cv2.imshow('Webcam',img)
                k=cv2.waitKey(50)
                if k==27:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        elif 'send email' in query:
            xxsendemail12()
            print()
            
        elif 'tell me a joke' in query:
            speak("Sure sir ")
            jokes=pyjokes.get_joke()
            print(jokes)
            print()
            speak(jokes)

        elif 'switch the window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            pyautogui.keyUp("alt")

        elif 'tell me the news' in query:
            speak('Sure Sir')
            speak('Please wait while i search latest news')
            news()
            
        elif 'where i am' in query or 'where are we' in query:
            speak("Wait sir findind the location")
            getloacation()
            
        elif 'instagram profile' in query or 'profile on instagram' in query:
            instagram()
        
        elif 'take screenshot' in query or 'screenshot' in query:
            screenshot()
            
        elif 'read file' in query:
            pdf_reader()

        elif 'exit' in query:
            speak("exiting system , Goodbye sir")
            exit()
            
        
            




    

 