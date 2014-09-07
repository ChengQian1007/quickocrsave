__author__ = 'chrisshroba'
import sendgrid

sg = sendgrid.SendGridClient("chrisshroba","Illinois!")

def send_email(address, subject, body):
    message = sendgrid.Mail()
    message.add_to(address)
    message.set_subject(subject)
    message.set_html(body)
    message.set_from("The Chancellor <phylliswise@illinois.edu")
    status, msg = sg.send(message)
    print status
    print msg

send_email("bpmoria2@illinois.edu","Expulsion Notice","You are expelled for hacking")