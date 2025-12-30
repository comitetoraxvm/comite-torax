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

def test_multiple_studies_per_group(client, db_session, user, patient, temp_upload_dir):
    # create a consultation with two func studies and two img studies (each with its own file)
    login(client)
    data = {
        'study_groups': ['func','img'],
        'study_type_func': ['Espirometría', 'Espirometría seguimiento'],
        'study_date_func': ['2025-12-01', '2025-12-06'],
        'study_description_func': ['Hallazgos A', 'Hallazgos B'],
        'study_type_img': ['TC Tórax', 'Rx Torax'],
        'study_date_img': ['2025-12-02', '2025-12-03'],
        'study_center_img': ['Hospital Pasteur', 'Clinica San Martin'],
        'study_access_code_img': ['ABC123', 'DEF456'],
        'study_description_img': ['Lesion 1', 'Lesion 2'],
        'control_enabled': 'on',
        'control_date': '2026-01-15',
        'date': '2025-12-30',
    }

    files = [
        ('study_file_func', (io.BytesIO(b"PDFFUNC1"), 'func1.pdf')),
        ('study_file_func', (io.BytesIO(b"PDFFUNC2"), 'func2.pdf')),
        ('study_file_img', (io.BytesIO(b"PDFIMG1"), 'img1.pdf')),
        ('study_file_img', (io.BytesIO(b"PDFIMG2"), 'img2.pdf')),
    ]

    multipart = []
    for k, v in data.items():
        if isinstance(v, list):
            for item in v:
                multipart.append((k, item))
        else:
            multipart.append((k, v))
    multipart.extend(files)

    # use MultiDict so multiple values/files with same field name are preserved
    from werkzeug.datastructures import MultiDict
    multipart_md = MultiDict(multipart)
    resp = client.post(f"/patients/{patient.id}/consultations/new", data=multipart_md, content_type='multipart/form-data', follow_redirects=True)
    assert resp.status_code == 200

    # verify DB entries
    with client.application.app_context():
        studies = list(Study.query.filter_by(patient_id=patient.id).all())
        # expect 4 studies created
        assert len(studies) >= 4
        types = [s.study_type for s in studies]
        assert 'Espirometría' in types
        assert 'Espirometría seguimiento' in types
        assert 'TC Tórax' in types
        assert 'Rx Torax' in types

        # ensure files were saved
        from app import get_upload_dir
        import os
        for s in studies:
            if s.report_file:
                path = os.path.join(get_upload_dir(), s.report_file)
                assert os.path.exists(path)

        # control reminder created
        cr = ControlReminder.query.filter_by(consultation_id=studies[0].consultation_id if studies else None).first()
        assert cr is not None