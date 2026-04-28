import os
from datetime import datetime

def get_next_despatch_id() -> str:
    import src.db
    
    now = datetime.utcnow()
    year = str(now.year)[2:]
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    date_part = f"{year}{month}{day}"
    
    response = src.db.dynamodb_table.update_item(
        Key={"email_address": "SYSTEM", "despatch_id": f"counter_{date_part}"},
        UpdateExpression="SET #count = if_not_exists(#count, :zero) + :one",
        ExpressionAttributeNames={"#count": "count"},
        ExpressionAttributeValues={":zero": 0, ":one": 1},
        ReturnValues="UPDATED_NEW"
    )
    
    count = int(response["Attributes"]["count"])
    return f"DA-{date_part}-{str(count).zfill(5)}"