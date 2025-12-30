import io
import pytest
from app import Study, ControlReminder


def login(client, username="testuser", password="secret"):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)


def test_create_consultation_with_multiple_groups(client, db_session, user, patient):
    # login
    rv = login(client)
    assert b"Login" not in rv.data or rv.status_code == 200

    # build multipart data with two files (func + img)
    data = {
        'study_groups': ['func','img'],
        'study_type_func': 'Espirometría',
        'study_date_func': '2025-12-01',
        'study_description_func': 'Hallazgos funcionales',
        'study_type_img': 'TC Tórax',
        'study_date_img': '2025-12-02',
        'study_center_img': 'Hospital Pasteur',
        'study_access_code_img': 'ABC123',
        'study_description_img': 'Lesiones pulmonares',
        'control_enabled': 'on',
        'control_date': '2026-01-15',
        'date': '2025-12-30',
    }

    files = {
        'study_file_func': (io.BytesIO(b"PDFDATAFUNC"), 'func.pdf'),
        'study_file_img': (io.BytesIO(b"PDFDATAIMG"), 'img.pdf'),
    }

    # merge files into data for client.post
    multipart = {}
    for k, v in data.items():
        multipart[k] = v
    multipart.update(files)

    resp = client.post(f"/patients/{patient.id}/consultations/new", data=multipart, content_type='multipart/form-data', follow_redirects=True)
    assert resp.status_code == 200

    # check DB
    with client.application.app_context():
        st_func = Study.query.filter_by(study_type='Espirometría').first()
        st_img = Study.query.filter_by(study_type='TC Tórax').first()
        assert st_func is not None
        assert st_img is not None

        cr = ControlReminder.query.filter_by(consultation_id=st_func.consultation_id if st_func else None).first()
        assert cr is not None
