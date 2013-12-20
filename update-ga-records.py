import pymongo
from datetime import timedelta


ga_buckets = [
    "carers_allowance_journey",
    "deposit_foreign_marriage_journey",
    "pay_foreign_marriage_certificates_journey",
    "pay_legalisation_drop_off_journey",
    "pay_legalisation_post_journey",
    "pay_register_birth_abroad_journey",
    "pay_register_death_abroad_journey",
    "lpa_journey",
    "licensing_journey",
]
backdrop = pymongo.Connection()['backdrop']

for bucket_name in ga_buckets:
    bucket = backdrop[bucket_name]

    records = list(bucket.find())
    
    for record in records:
        if record['_timestamp'].hour == 23:
            # WARNING: only fixes the _timestamp not the period start fields
            record['_timestamp'] = record['_timestamp'].replace(tzinfo=None) + timedelta(hours=1)
            bucket.save(record)
            print(record['_timestamp'].isoformat())
