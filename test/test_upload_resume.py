import sys
import os

# Add the `app/` folder to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

# Now import Flask app from backend_2
from backend_2 import app  # ✅ Now this will work

import io
import unittest

class ResumeUploadTestCase(unittest.TestCase):
    """Unit test for resume upload API."""

    def setUp(self):
        """Set up the test client before each test."""
        self.client = app.test_client()  # Initialize test client
        self.client.testing = True  # Enable testing mode

    def test_upload_resume(self):
        """Test uploading a sample PDF resume."""
        # Create a fake PDF file in memory
        resume_path = os.path.abspath("sample_resumes/Alhaan_resume.pdf")  
        # Check if the file exists before testing
        self.assertTrue(os.path.exists(resume_path), "Test PDF file does not exist!")
        with open(resume_path, "rb") as pdf_file:
            data = {
                "resume": (pdf_file, "Alhaan_resume.pdf"),  # ✅ Correct format
                "job_description": "Looking for a Python Developer"
            }

            # Send POST request
            response = self.client.post(
                "/upload",
                data=data,
                content_type="multipart/form-data",
            )

            # Debugging output
            print("\n🔍 DEBUG: Full API Response:", response.json)

            # Assert response status code
            self.assertEqual(response.status_code, 200)

        # Parse JSON response
        response_data = response.get_json()

        # Validate response keys
        self.assertIn("message", response_data)
        self.assertIn("resume_id", response_data)
        self.assertIn("ats_score", response_data)
        self.assertIn("file_path", response_data)

if __name__ == "__main__":
    unittest.main()
