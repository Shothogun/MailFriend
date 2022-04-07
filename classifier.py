from datetime import datetime, timedelta
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

def classifyTicket(call):
  ticketDate = datetime.strptime(call['Data_do_Registro'], "%d/%m/%Y %H:%M:%S")
  ticketDate = commercialBeginDate(ticketDate)
  # Vencido
  timeDiference = datetime.now() - ticketDate
  call['Tempo_Restante'] = "%d dia(s) e %dh".format(timeDiference.days, secondsToHours(timeDiference.seconds))
  if timeDiference.days > 1:
    return (call, 'V')
  # Contagem de horas de um dia pro outro:
  # horas decorridas menos as horas entre 
  # as 18h e as 8h
  elif timeDiference.days == 1 and \
        (secondsToHours(timeDiference.seconds)-14) > 8:
    return (call, 'V')
  elif timeDiference.days == 1 and \
        2 < (secondsToHours(timeDiference.seconds)-14) <= 8:
    return (call, 'A')
  elif timeDiference.days == 1 and \
        (secondsToHours(timeDiference.seconds)-14) < 2:
    return (call, 'B')
  elif timeDiference.days == 0 and \
        secondsToHours(timeDiference.seconds) > 8:
    return (call, 'V')
  elif 2 < secondsToHours(timeDiference.seconds) <= 8:
    return (call, 'A')
  elif secondsToHours(timeDiference.seconds) < 2:
    return (call, 'B')