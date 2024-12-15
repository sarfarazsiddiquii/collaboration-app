from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Workspace

# Create a Blueprint for workspace routes
workspace_bp = Blueprint('workspace', __name__)

# Create a new workspace with a workspace code
@workspace_bp.route('/workspaces', methods=['POST'])
@jwt_required()
def create_workspace():
    data = request.get_json()
    name = data.get('name')
    code = data.get('code')
    email = get_jwt_identity()

    if not name or not code:
        return jsonify({"message": "Name and code are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    new_workspace = Workspace(name=name, owner_id=user.id)
    new_workspace.set_password(code)
    new_workspace.users.append(user)
    db.session.add(new_workspace)
    db.session.commit()

    return jsonify({"message": "Workspace created successfully", "workspace_id": new_workspace.id}), 201

# Join a workspace with a workspace code
@workspace_bp.route('/workspaces/join', methods=['POST'])
@jwt_required()
def join_workspace():
    data = request.get_json()
    workspace_id = data.get('workspace_id')
    code = data.get('code')
    email = get_jwt_identity()

    if not workspace_id or not code:
        return jsonify({"message": "Workspace ID and code are required"}), 400

    workspace = Workspace.query.get(workspace_id)
    if not workspace:
        return jsonify({"message": "Workspace not found"}), 404

    if not workspace.check_password(code):
        return jsonify({"message": "Incorrect code"}), 401

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if user in workspace.users:
        return jsonify({"message": "User already in the workspace"}), 400

    workspace.users.append(user)
    db.session.commit()

    return jsonify({"message": "Successfully joined the workspace", "workspace_id": workspace.id, "name": workspace.name}), 200

# Fetch all workspaces
@workspace_bp.route('/workspaces', methods=['GET'])
@jwt_required()
def get_workspaces():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    workspaces = Workspace.query.filter(Workspace.users.any(id=user.id)).all()
    workspaces_list = [{"id": ws.id, "name": ws.name} for ws in workspaces]

    return jsonify(workspaces_list), 200

# Fetch workspace details
@workspace_bp.route('/workspaces/<int:workspace_id>', methods=['GET'])
@jwt_required()
def get_workspace(workspace_id):
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    workspace = Workspace.query.get(workspace_id)
    if not workspace or user not in workspace.users:
        return jsonify({"message": "Workspace not found or access denied"}), 404

    users = [{"id": u.id, "email": u.email} for u in workspace.users]
    workspace_details = {
        "id": workspace.id,
        "name": workspace.name,
        "code": workspace.plain_code,  # Display the plain text code temporarily
        "users": users
    }
    return jsonify(workspace_details), 200