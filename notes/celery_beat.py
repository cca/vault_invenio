from datetime import datetime

# add from invenio_app_rdm.config import CELERY_BEAT_SCHEDULE; print(CELERY_BEAT_SCHEDULE) to invenio.cfg to see this

# '<crontab...>' strings are the string representation of a crontab
# not the actual crontab object

CELERY_BEAT_SCHEDULE = {
    'indexer': {
        'task': 'invenio_records_resources.tasks.manage_indexer_queues',
        'schedule': datetime.timedelta(seconds=10)
    },
    'accounts_sessions': {
        'task': 'invenio_accounts.tasks.clean_session_table',
        'schedule': datetime.timedelta(seconds=3600)
    },
    'accounts_ips': {
        'task': 'invenio_accounts.tasks.delete_ips',
        'schedule': datetime.timedelta(seconds=21600)
    },
    'draft_resources': {
        'task': 'invenio_drafts_resources.services.records.tasks.cleanup_drafts',
        'schedule': datetime.timedelta(seconds=3600)
    },
    'rdm_records': {
        'task': 'invenio_rdm_records.services.tasks.update_expired_embargos',
        'schedule': '<crontab: 2 0 * * * (m/h/d/dM/MY)>'
    },
    'expire_requests': {
        'task': 'invenio_requests.tasks.check_expired_requests',
    'schedule': '<crontab: 3 0 * * * (m/h/d/dM/MY)>'
    },
    'file-checks': {
        'task': 'invenio_files_rest.tasks.schedule_checksum_verification',
        'schedule': datetime.timedelta(seconds=3600),
        'kwargs': {
            'batch_interval': {
                'hours': 1
            },
            'frequency': {
                'days': 14
            },
            'max_count': 0,
            'files_query': 'invenio_app_rdm.utils.files.checksum_verification_files_query'
        }
    },
    'file-integrity-report': {
        'task': 'invenio_app_rdm.tasks.file_integrity_report',
        'schedule': '<crontab: 0 7 * * * (m/h/d/dM/MY)>'
    }
}
