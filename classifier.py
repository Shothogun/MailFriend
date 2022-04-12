from datetime import date, datetime, timedelta
import os

def secondsToHours(seconds: int):
  return seconds//3600

def commercialBeginDate(date: datetime):
  if date.hour < 8:
    return datetime(date.year,date.month, date.day, 8)
  elif date.hour >= 18:
    date = date + timedelta(days=1)
    return datetime(date.year,date.month, date.day, 8)
  else:
    return date

def commercialTimePassed(previousDate: datetime, now: datetime):
  total = 0
  current_date = previousDate
  # TODO raise error with day after today

  # Count previous days hours
  while current_date.day != now.day:
    day_deadline = datetime(current_date.year, current_date.month,
                            current_date.day, 18, 0 ,0)
    total += secondsToHours((day_deadline - current_date).seconds)

    current_date += timedelta(days=1)
    current_date = datetime(current_date.year, current_date.month,
                            current_date.day, 8, 0 ,0)

  total += secondsToHours((now - current_date).seconds)

  return total

def classifyTicket(call):
  ticketDate = datetime.strptime(call['Data_do_Registro'], "%d/%m/%Y %H:%M:%S")
  ticketDate = commercialBeginDate(ticketDate)

  timeLeft = 8 - commercialTimePassed(ticketDate, datetime.now())

  if timeLeft <= 0:
    return (call, 'V')
  elif 0 < timeLeft <= 2:
    return (call, 'B')
  else:
    return (call, 'A')
  

def updateRemainingTime(call_tuple):
  call, callClass = call_tuple

  if callClass == 'V':
    call['Tempo_Restante'] = "Vencido!"
    return (call,callClass)

  ticketDate = datetime.strptime(call['Data_do_Registro'], "%d/%m/%Y %H:%M:%S")
  ticketDate = commercialBeginDate(ticketDate)

  total_hours = 8

  deadline = ticketDate

  while total_hours > 0:
    deadline += timedelta(hours=1)
    if deadline.hour == 18:
      deadline = deadline + timedelta(days=1)
      deadline = datetime(deadline.year, deadline.month,
                          deadline.day, 8, deadline.minute ,deadline.second)
    total_hours -= 1

  timeLeft = commercialTimePassed(datetime.now(), deadline)
  daysLeft = timeLeft//8
  hoursLeft = timeLeft%8

  call['Tempo_Restante'] = "{} dia(s) e {}h".format(daysLeft,hoursLeft)

  return (call,callClass)