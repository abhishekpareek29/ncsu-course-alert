import http.client
from bs4 import BeautifulSoup
import json
from telegram.ext import Updater, CommandHandler
import telegram


def get_course_statuses():
  conn = http.client.HTTPSConnection("www.acs.ncsu.edu")
  payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"term\"\r\n\r\n2191\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"subject\"\r\n\r\nCSC - Computer Science\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"course-inequality\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"course-number\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"course-career\"\r\n\r\nGRAD\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"session\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"start-time-inequality\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"start-time\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"end-time-inequality\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"end-time\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"instructor-name\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"current_strm\"\r\n\r\n2191\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
  headers = {
      'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
      'cache-control': "no-cache",
      }
  conn.request("POST", "/php/coursecat/search.php", payload, headers)
  res = conn.getresponse()
  data = res.read().decode('utf-8')
  data = json.loads(data)
  html = data['html']
  soup = BeautifulSoup(html, 'html.parser')
  course = {}
  for row in soup.findAll('tr'):
    dep, cno, sec = None, None, None
    depf = row.find('input', {'name': 'department.0'})
    if depf:
      dep = depf.get('value')
    cnof = row.find('input', {'name': 'course.0'})
    if cnof:
      cno = cnof.get('value')
    secf = row.find('input', {'name': 'section.0'})
    if secf:
      sec = secf.get('value')
    cols = row.findAll('td')
    if len(cols) > 4 and dep and cno and sec:
      course[dep+cno+"-"+sec] = cols[3].text
  return course

def check_your_courses(token,chat_id,course,check=[]):
  # token = '564482475:AAG4FHtCv-4KigmkVEmxdBKrKt6qEe1kmM0'
  bot = telegram.Bot(token=token)
  # chat_id = bot.get_updates()[-1].message.chat_id
  # chat_id = -271712683
  for cid in check:
    if 'Open' in course[cid] or 'Waitlist' in course[cid]:
      bot.send_message(chat_id=chat_id, text=cid+" is open/waitlisted, Fuckin register for it now!")

if __name__ == "__main__":
  course = {}
  course = get_course_statuses()
  # check = ['CSC 591-002', 'CSC 722-001']
  check_abhishek = ['CSC 510-001', 'CSC 573-002', 'CSC 591-024']
  #check_parth = ['CSC 591-002']
  #check_pranjal = ['CSC 501-001']
  #check_your_courses('680790205:AAFqRZM-R2PvYKmiW8e7Iv1B-k4HklZnW-Y',-236560483,course,check_pranjal)
  check_your_courses('564482475:AAG4FHtCv-4KigmkVEmxdBKrKt6qEe1kmM0',-271712683,course,check_abhishek)
  #check_your_courses('584419095:AAHCvHtANo0-5EyunUQaC8ZjUJHrWUBBJJk',579286362,course,check_parth)
