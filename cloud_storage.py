import os
import requests
from typing import Optional

class CloudStorageError(Exception):
    """Base exception for Cloud Storage related errors."""
    pass

class FileNotFoundError(CloudStorageError):
    """Raised when the specified file cannot be found."""
    pass

class UploadFailedError(CloudStorageError):
    """Raised when file upload fails."""
    pass

class NetworkError(CloudStorageError):
    """Raised when there's a network-related issue."""
    pass

class CloudStorage:
    def __init__(self):
        """
        Initialize CloudStorage with optional custom API endpoint.
        
        :param api_endpoint: URL of the cloud storage API
        """
        self.api_endpoint = "https://catbox.moe/user/api.php"

    def __send_request_to_api(self, file_path: str) -> Optional[str]:
        """
        Send file to cloud storage API.
        
        :param file_path: Path to the file to be uploaded
        :return: URL of uploaded file or None if upload fails
        :raises FileNotFoundError: If the specified file does not exist
        :raises NetworkError: If there are network-related issues
        :raises UploadFailedError: If the upload is unsuccessful
        """
        # Validate file existence
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Validate file is not empty
        if os.path.getsize(file_path) == 0:
            raise CloudStorageError(f"File is empty: {file_path}")

        try:
            params = {"reqtype": "fileupload"}
            
            with open(file_path, "rb") as file:
                response = requests.post(
                    self.api_endpoint, 
                    data=params, 
                    files={"fileToUpload": file}
                )
            
            if response.status_code == 200:
                file_url = response.text.strip()
                if not file_url:
                    raise UploadFailedError("Received empty response from server")
                return file_url
            else:
                raise UploadFailedError(
                    f"Upload failed. Status code: {response.status_code}. "
                    f"Response: {response.text}"
                )
        
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error during upload: {e}")
        except IOError as e:
            raise CloudStorageError(f"File reading error: {e}")

    def upload_to_cloud(self, file: str) -> Optional[str]:
        """
        Upload a file to cloud storage.
        
        :param file: Path to the file to be uploaded
        :return: URL of uploaded file or None if upload fails
        """
        try:
            return self.__send_request_to_api(file)
        except CloudStorageError as err:
            print(f"[!] Cloud Storage Error: {err}")
            return None
        except Exception as err:
            print(f"[!] Unexpected error during cloud upload: {err}")
            return None

def main():
    """Example usage of CloudStorage class."""
    try:
        cld = CloudStorage()
        upload_result = cld.upload_to_cloud('README.md')
        
        if upload_result:
            print(f"File uploaded successfully. URL: {upload_result}")
        else:
            print("File upload failed.")
    
    except Exception as e:
        print(f"An error occurred in the main execution: {e}")

if __name__ == '__main__':
    main()