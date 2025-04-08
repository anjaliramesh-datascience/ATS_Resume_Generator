# ATS-Optimized Resume Generator

A powerful tool to create professionally formatted resumes optimized for Applicant Tracking Systems (ATS) with a user-friendly web interface.

## Overview

This resume generator helps you create professional resumes that are optimized to score 90+ in Applicant Tracking Systems (ATS). The application provides a web-based user interface for easy input, along with flexible configuration options.

Features include:
- Clean, ATS-friendly formatting
- Dynamic content sections (work experience, education, skills, etc.)
- Optional sections for internships, projects, and certifications
- Automatic formatting adjustments based on content volume
- Web UI for easy data entry
- Support for JSON configuration files

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository to your local machine

2. Install required dependencies:
   ```bash
   pip install flask python-docx
   ```

## Usage

### Running the Web UI

1. Navigate to the project directory in your terminal/command prompt
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Open your web browser and go to:
   ```
   http://localhost:5000
   ```
   or
   ```
   http://127.0.0.1:5000
   ```

### Generating a Resume with the Web UI

1. Fill out the form with your information:
   - Personal details (name, contact information)
   - Professional summary
   - Work experience
   - Technical skills
   - Education
   - Optional sections: internships, projects, certifications

2. Click the "Generate Resume" button at the bottom of the form

3. Download your resume from the success page

### Updating an Existing Resume

One of the key features of this tool is the ability to easily update your resume in the future:

1. **Save Your Resume Data**:
   - When you generate a resume, you'll receive both the DOCX file and a JSON file
   - The JSON file contains all your resume information in a structured format
   - Always keep this JSON file for future updates

2. **Import Your Previous Resume**:
   - When you need to update your resume, click "Choose File" in the Import/Export section
   - Select your previously saved JSON file
   - Click "Import JSON" to load all your existing resume data

3. **Make Your Updates**:
   - Add new work experiences, update existing details, or make any other changes
   - For example, add a new certification, update responsibilities, or add new skills
   - All your previous information remains intact

4. **Generate Updated Resume**:
   - Click "Generate Resume" to create a fresh document with your updates
   - Both the updated resume DOCX and a new JSON file (with your changes) will be available

### Saving Resume Data Without Generating a Resume

If you want to save your progress without generating a resume:

1. Fill out the form with your information (partially or completely)
2. Click the "Save Form Data as JSON" button in the Import/Export section
3. This will download a JSON file with all your current data
4. You can later import this file to continue where you left off

### Form Tips

- Required fields are marked with an asterisk (*)
- Use the "Add" buttons to include multiple entries for work experience, education, etc.
- Use the remove buttons (X) to delete entries
- For lists of responsibilities or achievements, click "Add Responsibility" or "Add Achievement" to include multiple items
- Separate multiple skills with commas in the skills section
- Separate multiple courses with commas in the education section

## Alternative Methods

### Using JSON Files Directly

If you prefer to prepare your data in advance or reuse resume configurations, you can use a JSON file:

1. Create a JSON file with your resume data (see `sample_resume.json` for reference)
2. Run the resume generator with the JSON file:
   ```bash
   python resume-generator.py --json your_resume_data.json
   ```

### Using the Command Line Interface

The tool also provides an interactive CLI mode:

```bash
python resume-generator.py --interactive
```

Follow the prompts to enter your resume information.

## Customization

### Output Filename

You can specify a custom output filename in the web UI or in your JSON file. If not specified, the default format is `YourName_Resume.docx`.

### Resume Structure

The resume generator automatically adjusts formatting based on content volume to ensure your resume fits well on one page. Font sizes, spacing, and margins are dynamically calculated.

## Troubleshooting

### Common Issues

1. **Missing dependencies**
   - Ensure you've installed all required Python packages

2. **File permission errors**
   - Check that the application has write permissions to create the output file

3. **Web UI not showing**
   - Verify that the Flask server is running without errors
   - Check that you're using the correct URL (http://localhost:5000)

4. **JSON file errors**
   - Verify your JSON file is formatted correctly
   - Check that all required fields are present

### Getting Help

If you encounter any issues or have questions, please open an issue in the project repository.

## Technical Details

The resume generator uses:
- Python for backend processing
- Flask for the web server
- python-docx for document generation
- Bootstrap for the web UI

## License

This project is released under the MIT License. 