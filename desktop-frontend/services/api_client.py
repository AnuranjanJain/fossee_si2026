"""
API Client for Chemical Equipment Visualizer Desktop App.
"""
import requests
from typing import Optional, Dict, Any, List


class APIClient:
    """HTTP client for communicating with Django backend."""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.token: Optional[str] = None
    
    def _headers(self) -> Dict[str, str]:
        """Get request headers with auth token."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        return headers
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and store token."""
        response = requests.post(
            f"{self.base_url}/auth/login/",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data.get("token")
        return data
    
    def logout(self) -> None:
        """Logout and clear token."""
        try:
            requests.post(
                f"{self.base_url}/auth/logout/",
                headers=self._headers()
            )
        except:
            pass
        self.token = None
    
    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """Upload CSV file to backend."""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{self.base_url}/upload/",
                files={"file": f},
                headers=headers
            )
        response.raise_for_status()
        return response.json()
    
    def get_equipment(self, session_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get equipment list."""
        params = {}
        if session_id:
            params["session_id"] = session_id
        
        response = requests.get(
            f"{self.base_url}/equipment/",
            headers=self._headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def get_summary(self, session_id: Optional[int] = None) -> Dict[str, Any]:
        """Get summary statistics."""
        params = {}
        if session_id:
            params["session_id"] = session_id
        
        response = requests.get(
            f"{self.base_url}/summary/",
            headers=self._headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get upload history."""
        response = requests.get(
            f"{self.base_url}/history/",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def download_pdf(self, session_id: Optional[int] = None) -> bytes:
        """Download PDF report."""
        params = {}
        if session_id:
            params["session_id"] = session_id
        
        response = requests.get(
            f"{self.base_url}/report/pdf/",
            headers=self._headers(),
            params=params
        )
        response.raise_for_status()
        return response.content
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.token is not None


# Global API client instance
api_client = APIClient()
