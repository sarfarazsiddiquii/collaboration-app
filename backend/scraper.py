from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bs4 import BeautifulSoup
import requests
from models import db, ScrapedContent, Workspace, User

# Create a Blueprint for the scraper routes
scraper_bp = Blueprint('scraper', __name__)

@scraper_bp.route('/workspaces/<int:workspace_id>/scrape', methods=['POST'])
@jwt_required()
def scrape(workspace_id):
    data = request.get_json()
    url = data.get('url')
    user_email = get_jwt_identity()

    user = User.query.filter_by(email=user_email).first()
    workspace = Workspace.query.get(workspace_id)

    if not workspace or user not in workspace.users:
        return jsonify({"message": "Workspace not found or access denied"}), 404

    try:
        # Fetch the content from the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        structured_content = []

        # Extract headings and their corresponding content
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            heading_text = heading.get_text(strip=True)
            content_text = ''
            for sibling in heading.find_next_siblings():
                if sibling.name and sibling.name.startswith('h'):
                    break
                content_text += sibling.get_text(separator=' ', strip=True) + ' '
            structured_content.append(f"{heading_text}\n{content_text.strip()}")

        # Join the structured content into a single string
        structured_content_str = '\n\n'.join(structured_content)

        # Save the structured content to the database
        new_scrape = ScrapedContent(user_email=user_email, url=url, content=structured_content_str)
        db.session.add(new_scrape)
        db.session.commit()

        return jsonify({"message": "Content scraped successfully", "content": structured_content_str[:500]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500