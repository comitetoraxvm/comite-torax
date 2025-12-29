import datetime
from app import app, Screening, ScreeningFollowup, ControlReminder, send_email


def get_recipients(patient, extra_email=None, created_by=None):
    recipients = []
    if patient and patient.email:
        recipients.append(patient.email)
    if extra_email:
        recipients.append(extra_email)
    if created_by and getattr(created_by, "email", None):
        recipients.append(created_by.email)
    cleaned = []
    for r in recipients:
        if r and r not in cleaned:
            cleaned.append(r)
    return cleaned


def send_reminders_for_date(target_date: str):
    with app.app_context():
        screenings = Screening.query.filter(Screening.next_control_date == target_date).all()
        followups = ScreeningFollowup.query.filter(
            ScreeningFollowup.next_control_date == target_date, ScreeningFollowup.completed == False
        ).all()
        controls = ControlReminder.query.filter(
            ControlReminder.control_date == target_date, ControlReminder.completed == False
        ).all()

        for s in screenings:
            recipients = get_recipients(s.patient, s.extra_email, s.patient.created_by if s.patient else None)
        if not recipients:
            continue
        subject = "CONTROL MEDICO"
        body = (
            f"Recordatorio paciente {s.patient.full_name} (DNI: {s.patient.dni or '-'}).\n"
            f"Control medico con doctor: {s.patient.created_by.full_name if s.patient and s.patient.created_by else '---'}"
        )
        send_email(recipients, subject, body)

    for fu in followups:
        s = fu.screening
        recipients = get_recipients(s.patient, s.extra_email, fu.created_by or (s.patient.created_by if s.patient else None))
        if not recipients:
            continue
        subject = "CONTROL MEDICO"
        body = (
            f"Recordatorio paciente {s.patient.full_name} (DNI: {s.patient.dni or '-'}).\n"
            f"Control medico con doctor: {fu.created_by.full_name if fu.created_by else (s.patient.created_by.full_name if s.patient and s.patient.created_by else '---')}"
        )
        send_email(recipients, subject, body)

    for cr in controls:
        recipients = get_recipients(cr.patient, cr.extra_emails, cr.created_by or (cr.patient.created_by if cr.patient else None))
        if not recipients:
            continue
        subject = "CONTROL MEDICO"
        body = (
            f"Recordatorio paciente {cr.patient.full_name} (DNI: {cr.patient.dni or '-'}).\n"
            f"Control medico con doctor: {cr.created_by.full_name if cr.created_by else (cr.patient.created_by.full_name if cr.patient and cr.patient.created_by else '---')}"
        )
        send_email(recipients, subject, body)


if __name__ == "__main__":
    today = datetime.date.today().isoformat()
    send_reminders_for_date(today)
    print(f"Recordatorios enviados para {today}")
