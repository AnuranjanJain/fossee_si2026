"""
API Client for Chemical Equipment Visualizer Desktop App.
Uses connection pooling and timeouts for better performance.
"""
import requests
from typing import Optional, Dict, Any, List


# Default timeout for API requests (connect, read)
DEFAULT_TIMEOUT = (3.0, 10.0)


class APIClient:
    """HTTP client for communicating with Django backend."""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.token: Optional[str] = None
        # Use Session for connection pooling (reuses TCP connections)
        self.session = requests.Session()
    
    def _headers(self) -> Dict[str, str]:
        """Get request headers with auth token."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        return headers
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and store token."""
        response = self.session.post(
            f"{self.base_url}/auth/login/",
            json={"username": username, "password": password},
            timeout=DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        self.token = data.get("token")
        return data
    
    def logout(self) -> None:
        """Logout and clear token."""
        try:
            self.session.post(
                f"{self.base_url}/auth/logout/",
                headers=self._headers(),
                timeout=DEFAULT_TIMEOUT
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
            response = self.session.post(
                f"{self.base_url}/upload/",
                files={"file": f},
                headers=headers,
                timeout=(3.0, 30.0)  # Longer timeout for file upload
            )
        response.raise_for_status()
        return response.json()
    
    def get_equipment(self, session_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get equipment list."""
        params = {}
        if session_id:
            params["session_id"] = session_id
        
        response = self.session.get(
            f"{self.base_url}/equipment/",
            headers=self._headers(),
            params=params,
            timeout=DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    
    def get_summary(self, session_id: Optional[int] = None) -> Dict[str, Any]:
        """Get summary statistics."""
        params = {}
        if session_id:
            params["session_id"] = session_id
        
        response = self.session.get(
            f"{self.base_url}/summary/",
            headers=self._headers(),
            params=params,
            timeout=DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get upload history."""
        response = self.session.get(
            f"{self.base_url}/history/",
            headers=self._headers(),
            timeout=DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    
    def download_pdf(self, session_id: Optional[int] = None) -> bytes:
        """Download PDF report."""
        params = {}
        if session_id:
            params["session_id"] = session_id
        
        response = self.session.get(
            f"{self.base_url}/report/pdf/",
            headers=self._headers(),
            params=params,
            timeout=(3.0, 30.0)  # Longer timeout for PDF generation
        )
        response.raise_for_status()
        return response.content
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.token is not None


# Global API client instance
api_client = APIClient()
