from datetime import datetime, timedelta
import os

def callAberto(ticketDate: datetime):
  if ticketDate.day == datetime.now().day:
    # Case: 8h-10h
    if ticketDate.hour < 8:
      timeInterval = datetime.today() - timedelta(hours=8)
      # It lasts more than 2h
      if timeInterval.hour < 6:
        return True
      else:
        return False


    else if 8 <= ticketDate.hour <= 10:
      timeInterval = datetime.today() - timedelta(hours=ticketDate.hour, minutes=ticketDate.minute)
      # It lasts more than 2h
      if timeInterval.hour < 6:
        return True
      else:
        return False
    else:



def callBreve(ticketDate: datetime):
  timeInterval = datetime.today() - timedelta(hours=ticketDate.hour, minutes=ticketDate.minute)
  if timeInterval.hour <= 2:
    return True
  else:
    return False

def callVencido(ticketDate: datetime):
  timeInterval = datetime.today() - timedelta(hours=ticketDate.hour, minutes=ticketDate.minute)
  if ticketDate:
    return True
  else:
    return False