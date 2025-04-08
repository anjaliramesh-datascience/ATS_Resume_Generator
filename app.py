#!/usr/bin/env python3
"""
Web UI for Resume Generator
This Flask application provides a web interface for the ATS-optimized resume generator.
"""

import os
import json
import tempfile
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, Response
from werkzeug.utils import secure_filename
import resume_generator  # Import the resume generator module

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

@app.route('/')
def index():
    """Render the main form page"""
    return render_template('index.html')

def extract_resume_data_from_form(form_data):
    """Extract and format resume data from form submission"""
    data = {
        "name": form_data.get('name'),
        "contact_info": [
            form_data.get('email'),
            form_data.get('phone'),
            form_data.get('linkedin'),
            form_data.get('location')
        ],
        "work_experience": [],
        "technical_skills": {},
        "education": []
    }
    
    # Add professional summary only if it's not empty
    professional_summary = form_data.get('professional_summary', '').strip()
    if professional_summary:
        data["professional_summary"] = professional_summary
    
    # Process work experience
    work_count = int(form_data.get('work_count', 0))
    for i in range(work_count):
        prefix = f'work_{i}_'
        
        # Get responsibilities and achievements as arrays
        responsibilities = []
        achievements = []
        
        resp_count = int(form_data.get(f'{prefix}resp_count', 0))
        for j in range(resp_count):
            resp = form_data.get(f'{prefix}resp_{j}')
            if resp and resp.strip():
                responsibilities.append(resp.strip())
        
        ach_count = int(form_data.get(f'{prefix}ach_count', 0))
        for j in range(ach_count):
            ach = form_data.get(f'{prefix}ach_{j}')
            if ach and ach.strip():
                achievements.append(ach.strip())
        
        experience = {
            "title": form_data.get(f'{prefix}title'),
            "company": form_data.get(f'{prefix}company'),
            "location": form_data.get(f'{prefix}location'),
            "start_date": form_data.get(f'{prefix}start_date'),
            "end_date": form_data.get(f'{prefix}end_date'),
            "responsibilities": responsibilities,
            "achievements": achievements
        }
        
        data["work_experience"].append(experience)
    
    # Process internships (optional)
    intern_count = int(form_data.get('intern_count', 0))
    if intern_count > 0:
        data["internships"] = []
        
        for i in range(intern_count):
            prefix = f'intern_{i}_'
            
            # Get responsibilities and achievements as arrays
            responsibilities = []
            achievements = []
            
            resp_count = int(form_data.get(f'{prefix}resp_count', 0))
            for j in range(resp_count):
                resp = form_data.get(f'{prefix}resp_{j}')
                if resp and resp.strip():
                    responsibilities.append(resp.strip())
            
            ach_count = int(form_data.get(f'{prefix}ach_count', 0))
            for j in range(ach_count):
                ach = form_data.get(f'{prefix}ach_{j}')
                if ach and ach.strip():
                    achievements.append(ach.strip())
            
            internship = {
                "title": form_data.get(f'{prefix}title'),
                "company": form_data.get(f'{prefix}company'),
                "location": form_data.get(f'{prefix}location'),
                "start_date": form_data.get(f'{prefix}start_date'),
                "end_date": form_data.get(f'{prefix}end_date'),
                "responsibilities": responsibilities,
                "achievements": achievements
            }
            
            data["internships"].append(internship)
    
    # Process projects (optional)
    project_count = int(form_data.get('project_count', 0))
    if project_count > 0:
        data["projects"] = []
        
        for i in range(project_count):
            prefix = f'project_{i}_'
            
            # Get technologies as an array
            technologies_text = form_data.get(f'{prefix}technologies', '')
            technologies = [tech.strip() for tech in technologies_text.split(',') if tech.strip()]
            
            project = {
                "name": form_data.get(f'{prefix}name'),
                "description": form_data.get(f'{prefix}description'),
                "technologies": technologies,
                "url": form_data.get(f'{prefix}url') or None,
                "start_date": form_data.get(f'{prefix}start_date') or None,
                "end_date": form_data.get(f'{prefix}end_date') or None
            }
            
            data["projects"].append(project)
    
    # Process technical skills
    skill_categories = form_data.getlist('skill_category[]')
    skill_values = form_data.getlist('skill_values[]')
    
    for i in range(len(skill_categories)):
        if i < len(skill_values):
            category = skill_categories[i].strip()
            if category:
                # Split comma-separated skills into a list
                skills = [skill.strip() for skill in skill_values[i].split(',') if skill.strip()]
                if skills:
                    data["technical_skills"][category] = skills
    
    # Process certifications (optional)
    cert_count = int(form_data.get('cert_count', 0))
    if cert_count > 0:
        data["certifications"] = []
        
        for i in range(cert_count):
            prefix = f'cert_{i}_'
            
            certification = {
                "name": form_data.get(f'{prefix}name'),
                "issuer": form_data.get(f'{prefix}issuer'),
                "date": form_data.get(f'{prefix}date'),
                "expiration_date": form_data.get(f'{prefix}expiration') or None,
                "url": form_data.get(f'{prefix}url') or None
            }
            
            data["certifications"].append(certification)
    
    # Process education
    edu_count = int(form_data.get('edu_count', 0))
    for i in range(edu_count):
        prefix = f'edu_{i}_'
        
        # Get courses as an array
        courses_text = form_data.get(f'{prefix}courses', '')
        courses = [course.strip() for course in courses_text.split(',') if course.strip()]
        
        education = {
            "degree": form_data.get(f'{prefix}degree'),
            "institution": form_data.get(f'{prefix}institution'),
            "location": form_data.get(f'{prefix}location'),
            "graduation_date": form_data.get(f'{prefix}graduation'),
            "gpa": form_data.get(f'{prefix}gpa') or None,
            "relevant_courses": courses if courses else None
        }
        
        data["education"].append(education)
    
    # Set output filename (optional)
    output_filename = form_data.get('output_filename')
    if output_filename:
        if not output_filename.endswith('.docx'):
            output_filename += '.docx'
        data["output_filename"] = output_filename
    
    return data

@app.route('/save_json', methods=['POST'])
def save_json():
    """Save form data as JSON and return as downloadable file"""
    try:
        data = extract_resume_data_from_form(request.form)
        
        # Generate a meaningful filename using the person's name
        clean_name = data["name"].replace(' ', '_')
        json_filename = f"{clean_name}_resume_data.json"
        
        # Create JSON response with appropriate headers for download
        return Response(
            json.dumps(data, indent=2),
            mimetype='application/json',
            headers={
                'Content-Disposition': f'attachment; filename={json_filename}'
            }
        )
    
    except Exception as e:
        flash(f"Error saving JSON data: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate_resume():
    """Process form data and generate resume"""
    try:
        # Extract form data using the shared function
        data = extract_resume_data_from_form(request.form)
        
        # Save JSON to temporary file
        json_file = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_resume_data.json')
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Generate resume
        resume_path = resume_generator.create_resume_from_json(json_file)
        
        # Keep a copy of the JSON for user download
        json_copy = os.path.join(app.config['UPLOAD_FOLDER'], f"{data['name'].replace(' ', '_')}_resume_data.json")
        with open(json_copy, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Clean up temporary JSON file
        os.remove(json_file)
        
        # Return the result with download links for both resume and JSON
        return render_template('success.html', 
                              resume_path=resume_path,
                              json_path=json_copy,
                              user_name=data['name'])
    
    except Exception as e:
        flash(f"Error generating resume: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download a file"""
    directory = os.path.dirname(filename)
    file = os.path.basename(filename)
    return send_file(filename, as_attachment=True, download_name=file)

@app.route('/upload_json', methods=['POST'])
def upload_json():
    """Process uploaded JSON to pre-fill the form"""
    if 'json_file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
        
    file = request.files['json_file']
    
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
        
    if file and file.filename.endswith('.json'):
        try:
            # Save the uploaded file temporarily
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_resume_data.json')
            file.save(temp_path)
            
            # Load the data
            with open(temp_path, 'r') as f:
                data = json.load(f)
                
            # Remove the temporary file
            os.remove(temp_path)
            
            # Pass the data to the template
            return render_template('index.html', prefill_data=data)
            
        except Exception as e:
            flash(f'Error processing JSON file: {str(e)}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload a JSON file.', 'error')
        return redirect(url_for('index'))

@app.route('/template')
def template():
    """Return a blank JSON template"""
    template_data = {
        "name": "",
        "contact_info": ["email", "phone", "linkedin", "location"],
        "professional_summary": "",
        "work_experience": [{
            "title": "",
            "company": "",
            "location": "",
            "start_date": "",
            "end_date": "",
            "responsibilities": [""],
            "achievements": [""]
        }],
        "technical_skills": {
            "Category": ["Skill1", "Skill2"]
        },
        "education": [{
            "degree": "",
            "institution": "",
            "location": "",
            "graduation_date": "",
            "gpa": "",
            "relevant_courses": [""]
        }]
    }
    
    # Optional sections
    template_data["internships"] = [{
        "title": "",
        "company": "",
        "location": "",
        "start_date": "",
        "end_date": "",
        "responsibilities": [""],
        "achievements": [""]
    }]
    
    template_data["projects"] = [{
        "name": "",
        "description": "",
        "technologies": [""],
        "url": "",
        "start_date": "",
        "end_date": ""
    }]
    
    template_data["certifications"] = [{
        "name": "",
        "issuer": "",
        "date": "",
        "expiration_date": "",
        "url": ""
    }]
    
    return jsonify(template_data)

if __name__ == '__main__':
    app.run(debug=True) 