from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Workspace, Invite

# Create a Blueprint for workspace routes
workspace_bp = Blueprint('workspace', __name__)

# Create a workspace
@workspace_bp.route('/workspaces', methods=['POST'])
@jwt_required()
def create_workspace():
    data = request.get_json()
    name = data.get('name')
    email = get_jwt_identity()

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    workspace = Workspace(name=name, owner_id=user.id)
    workspace.users.append(user)
    db.session.add(workspace)
    db.session.commit()

    return jsonify({"message": "Workspace created successfully", "workspace_id": workspace.id}), 201

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

    workspace_details = {"id": workspace.id, "name": workspace.name}
    return jsonify(workspace_details), 200

# Send an invite to a workspace
@workspace_bp.route('/workspaces/<int:workspace_id>/invite', methods=['POST'])
@jwt_required()
def invite_to_workspace(workspace_id):
    data = request.get_json()
    email = data.get('email')

    invite = Invite(email=email, workspace_id=workspace_id)
    db.session.add(invite)
    db.session.commit()

    return jsonify({"message": "Invite sent successfully"}), 201

# Accept an invite
@workspace_bp.route('/workspaces/<int:workspace_id>/accept', methods=['POST'])
@jwt_required()
def accept_invite(workspace_id):
    email = get_jwt_identity()
    invite = Invite.query.filter_by(email=email, workspace_id=workspace_id).first()

    if not invite:
        return jsonify({"message": "Invite not found"}), 404

    user = User.query.filter_by(email=email).first()
    workspace = Workspace.query.get(workspace_id)
    workspace.users.append(user)

    db.session.delete(invite)
    db.session.commit()

    return jsonify({"message": "Invite accepted"}), 200
