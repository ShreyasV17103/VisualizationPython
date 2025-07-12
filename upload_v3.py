import json
from google.cloud import storage
from google.oauth2 import service_account
import os
import re

def upload_file_to_gcs(file_path, bucket_name, destination_blob_name, credentials):
    """
    Uploads a file from the local filesystem to a specified GCS bucket using service account credentials.
    """
    if isinstance(credentials, str):
        credentials = json.loads(credentials)
    creds = service_account.Credentials.from_service_account_info(credentials)
    client = storage.Client(credentials=creds, project=credentials.get("project_id"))
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    try:
        blob.upload_from_filename(file_path)
        print(f"Uploaded: {file_path} -> gs://{bucket_name}/{destination_blob_name}")
    except Exception as e:
        print("Error uploading file:", e)

def upload_directory_to_gcs(local_dir, bucket_name, gcs_dir, credentials):
        """
        Recursively uploads a directory to GCS under the specified gcs_dir.
        Only uploads files with allowed extensions.
        """
        allowed_exts = {'.py', '.html', '.csv', '.png', '.npy'}
        for root, _, files in os.walk(local_dir):
            for file in files:
                if os.path.splitext(file)[1].lower() not in allowed_exts:
                    continue
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, local_dir)
                gcs_path = os.path.join(gcs_dir, rel_path).replace("\\", "/")
                upload_file_to_gcs(local_path, bucket_name, gcs_path, credentials)

if __name__ == "__main__":
    while True:
        print("\n" + "*" * 64 + "\n")
        print("Please use \033[93mhttps://www.uuidtools.com/v4\033[0m to obtain a unique UUID.")
        print("\n" + "*" * 64 + "\n")
        data_row_id = input("Enter a UUID (example: 44106ae2-4b29-4dce-a81d-ba05da4bbfdd): ").strip()
        if re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", data_row_id):
            break
        print("Invalid UUID.")

    print("\nPlease confirm that all files in your 'data', 'outputs', and 'scripts' folders are correct.")
    print("Once uploaded, you will \033[91mNOT\033[0m be able to update or replace them.")
    confirm = input("Type 'yes' to continue with the upload, or anything else to cancel: ").strip().lower()
    if confirm != 'yes':
        print("Upload cancelled.")
        exit(0)
    bucket_name = 'coding_evaluation'
    credentials = {
        "type": "service_account",
        "project_id": "dataoperations-449123",
        "private_key_id": "6b3cac1121f2fa3e3c403e4a47e629f02e5453f9",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCzaave24FtdpzY\nHSd+ugoA2tipixzNsyhJqftynnTdZvEtQlce9JW9wv6qnrOy+7OUMhzD34Kw7vSm\nbU0MhY/yDgc1cBBf+dMBm0aN/IWTGGHVbu+8/VuGKpScviTxzmt4kyuk9ZnVGrhN\nYQeqvyl736jSPYVObtLJBNZExN2+44gJet+f8RtJmeRsB68OnATymbEjx+2Cv4uL\nCG3ravgkfEkhnkztb1zztmuAjd+2NfViUs983Wli9MrIuyd6JXrJPjKmM5wsNYuW\nJ8lsiqyWX6pxfQdRbKDpqQM2N+IjKIOcTIx/wx9PC7voGDqlOOM1DZpJuDCnioC+\nfWStkLX/AgMBAAECggEAMicH9HRH6eGOVptPvw0iXrrOdhZ9JsM+L9lkgNXqtTlh\nkdVJpU2ZzkIEDo3ujcnumS6o+9gvIGar3RoQv79WTcO+ICIDcdDUO068mlRMwqG+\nN3ubaKkqPIcKpAZDLZUWVc5OFP7S0c92VasaCZEGd6o99wdbjGFOawL/IpolooZf\nAmfvq4N0fQdUPywezyQunm5lau2suYWinbP+L3aA4/No9gpjPvAfVMNTLZB7a4Nm\nwAoLG+bFC0A6msYMjECaAuFWKGxWTOSJ1iGphUUvRAuF7UHch0dEKz0dXr02DPtf\nRh+5lOHAcvbVjj9cjSRxMYIV0wwgkeaRIflQT+ndgQKBgQD5K0SymLehXzC8MUN6\nMSCBDFCHan0wznP6K5JF31vqcNnZMTe5Dplhn499jVvHhY6f5LwFZQc9XQYS5iNR\nFwwkR5YJJJOPD6xp+MnFOy/fdjnRWGmEXI3b1Q8uBabmvlb7mNFr92KwT0X5aIgy\nHLcmXkMzzGrP8C+JcyWnupWaiwKBgQC4VNYB1DRVdxn94caxsIA94dsbggY25wPa\nNq1wNyT1oelbA5Tz4T+JO/fd1vkt7u/3UKNgtBfkObrEB0BQp1S5DpPp336ILO3f\nSSPj5nklFmITVHCbpXIsVvyJAbCp3jP1jBpSGnCuNOIJFCzWDYYCShzMmBrMSUD8\n/PGHm6Rk3QKBgA4wXJUfBTX3Sbstwv3uVj+DCALuGXryBsC0QnwgIAfVrVIk71tm\nbW2VvIIVzqgp/tk0GVDlU+g2p+XjnRc9DL/0I6MZph17cwIF3NeSa0N6ZAh71GZp\nLtrZ4ydnwv1Y0XM6XJKdX81SdlWhkj/oSrWwoHsOpPZ6YvqcyAQpJ+PJAoGBAJYj\nY3xx336NV/pWX4RzgsDkqZaqPW2SlKy0RGhWQiBgFLYxIK3UFfAtjCKA6szjBUmn\nwKsPhTY7X0gzr8sBwBxLJ2cixukbz1RDOpxyKNJwfMnJyT69b1V2NJNTcRWrCx9B\nUl71cjoykLlcWXiv4ysSOoraiVlDgU+OpxwRRcFxAoGBAPP/4Elq8HsVHwGyTRjQ\nvHBkXsyKzXPYZ1/a9Y6t8RU2II35yTYhc1D3lBX1t0YS7hhrXicaTkuPBtc/unIm\nMbQ65teQwDfMkQx5hqjtqK9aiYH2X+/TSoPT9ipDM7p7b83VdiUEWMqKQu28B18V\n9c9wLRhlb2cIdYuGgqNkZQAn\n-----END PRIVATE KEY-----\n",
        "client_email": "coding-evaluation@dataoperations-449123.iam.gserviceaccount.com",
        "client_id": "112271742990232659742",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/coding-evaluation%40dataoperations-449123.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }


    base_dir = os.path.dirname(os.path.abspath(__file__))
    folders = {
        "data": os.path.abspath(os.path.join(base_dir, "data")),
        "outputs": os.path.abspath(os.path.join(base_dir, "outputs")),
        "scripts": os.path.abspath(os.path.join(base_dir, "scripts")),
    }

    # Upload each folder
    for key, local_path in folders.items():
        gcs_dir = f"{data_row_id}/{key}/"
        if os.path.exists(local_path):
            upload_directory_to_gcs(local_path, bucket_name, gcs_dir, credentials)
        else:
            print(f"Warning: {local_path} does not exist, skipping.")

    print("\nCopy-paste the following into the Labelbox editor:\n")
    print(f"data_gen.py URI: gs://{bucket_name}/{data_row_id}/scripts/data_gen.py")
    print(f"Generated Data URI: gs://{bucket_name}/{data_row_id}/data/")
    print(f"viz.py URI: gs://{bucket_name}/{data_row_id}/scripts/viz.py")
    print(f"Outputs URI: gs://{bucket_name}/{data_row_id}/outputs/")