import uuid
import itertools
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from  flask_weasyprint import render_pdf, HTML
from src.models import Users, Records, Entries, GeneralSummary, db
from src.lib import get_data_structure_from_excel_file
from src.utils import concat_summaries
from src.processing import generate_summary
from werkzeug.security import check_password_hash, generate_password_hash

api = Blueprint("api", __name__, static_folder="./frontend/dist")
api.template_folder = "./static" # only used for summary pdf generation



@api.route("/index")
def index():
    return {"message": "Hello from the API endpoint"}


@api.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = Users.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"user": user.to_dict()}), 200
    else:
        return jsonify({"loggedIn": False}), 401


@api.route("/logout")
def logout():
    logout_user()
    return jsonify({"loggedIn": False}), 200


@api.route("/upload", methods=["POST"])
@login_required
def upload():
    file = request.files.get("file")
    description = request.form.get("description")
    ext: str = file.filename.split(".")[-1]
    accepted_extensions = ["csv", "xlsx", "xls"]
    if ext not in accepted_extensions:
        return (
            jsonify(
                {
                    "message": "Unsupported file type. Only CSV and XLSX files are acceptable."
                }
            ),
            415,
        )

    # get data structure from file
    data_structure = get_data_structure_from_excel_file(file, file_type=ext)

    if data_structure is None:
        return jsonify({"message": "Error processing file"}), 400

    # process data
    # create record
    record_id = str(uuid.uuid4())
    new_record: Records = Records()
    new_record.id = record_id
    new_record.created_by = current_user.id
    new_record.name = file.filename
    new_record.description = description
    db.session.add(new_record)
    db.session.commit()

    # send data for summarization
    summary = generate_summary(record_id=record_id, data=data_structure)

    if summary is None:
        return jsonify({"message": "Error processing file"}), 400

    return jsonify({"message": "File uploaded and summary generated!"}), 200


@api.route("/records", methods=["GET"])
@login_required
def records():
    if current_user is None:
        return jsonify(None), 401
    records = Records.query.filter_by(created_by=current_user.id).all()
    record = list(
        map(
            lambda record: {
                **record.to_dict(),
                "created_by": record.get_user_profile().username,
            },
            records,
        )
    )
    return jsonify(record), 200


@api.route("/get-record/<string:record_id>", methods=["GET"])
@login_required
def get_record(record_id):
    if current_user is None:
        return jsonify(None), 401

    record = Records.query.filter_by(id=record_id, created_by=current_user.id).first()

    if record is None:
        return jsonify(None), 404

    entries = Entries.query.filter_by(record_id=record_id).all()
    if entries == []:
        return jsonify({"record": record.to_dict(), "entries": entries}), 200

    # convert to dict
    entries = [entry.to_dict() for entry in entries]
    # remove unused keys
    entries = list(
        filter(
            lambda entry: (entry.pop("record", None), entry.pop("id", None)), entries
        )
    )
    #  sort items
    entries = sorted(entries, key=lambda entry: entry["title"])
    #  group items
    entries = itertools.groupby(entries, key=lambda entry: entry["title"])
    # make new list with expected entries
    entries = [{"key": key, "value": list(value)} for key, value in entries]
    # merge with generated summaries
    general_summaries = (
        GeneralSummary.query.filter_by(record_id=record_id)
        .with_entities(GeneralSummary.title, GeneralSummary.summary)
        .all()
    )
    general_summaries = [
        {"title": summary.title, "summary": summary.summary}
        for summary in general_summaries
    ]

    # include general summaries in entries
    for entry in entries:
        for summary in general_summaries:
            if entry["key"] == summary["title"]:
                entry["general_summary"] = summary["summary"]

    return jsonify({"record": record.to_dict(), "entries": entries}), 200

@api.route("/generate-summary/<string:record_id>", methods=["GET"])
def generate_summary_as_pdf(record_id):
    if current_user is None:
        return jsonify(None), 401

    record: Records = Records.query.filter_by(id=record_id, created_by=current_user.id).first()
    if record is None:
        return jsonify(None), 404

    download_name = record.name.replace(" ", "_").replace(".", "-").replace(":", "-").replace("/", "-")
    entries = Entries.query.filter_by(record_id=record_id).all()
    if entries == []:
        return jsonify({"record": record.to_dict(), "entries": entries}), 200

    # convert to dict
    entries = [entry.to_dict() for entry in entries]
    # remove unused keys
    entries = list(
        filter(
            lambda entry: (entry.pop("record", None), entry.pop("id", None)), entries
        )
    )
    #  sort items
    entries = sorted(entries, key=lambda entry: entry["title"])
    #  group items
    entries = itertools.groupby(entries, key=lambda entry: entry["title"])
    # make new list with expected entries
    entries = [{"key": key, "value": list(value)} for key, value in entries]
    # merge with generated summaries
    general_summaries = (
        GeneralSummary.query.filter_by(record_id=record_id)
        .with_entities(GeneralSummary.title, GeneralSummary.summary)
        .all()
    )
    general_summaries = [
        {"title": summary.title, "summary": summary.summary}
        for summary in general_summaries
    ]

    # include general summaries in entries
    for entry in entries:
        for summary in general_summaries:
            if entry["key"] == summary["title"]:
                entry["general_summary"] = summary["summary"]
    
    html = render_template("summary.html", context={"entries": entries, "record": record.to_dict(), "pdf_mode": True})

    #! for development
    # pdf = HTML(string=html, base_url=request.url_root, media_type="print").write_pdf()
    # with open("summary-from.pdf", "wb") as file:
    #     file.write(pdf)
    pdf = render_pdf(HTML(string=html), download_filename=download_name+".pdf")
    return pdf

    #! for development
    # return render_template("summary.html", context={"entries": entries, "record": record.to_dict(), "pdf_mode": False})



@api.route("/delete-record/<string:record_id>", methods=["DELETE"])
@login_required
def delete_record(record_id):
    if current_user is None:
        return jsonify(None), 401
    record = Records.query.filter_by(id=record_id, created_by=current_user.id).first()
    if record is None:
        return jsonify(None), 404

    # delete record
    db.session.delete(record)
    db.session.commit()
    return jsonify(None), 200


@api.route("/profile", methods=["GET"])
@login_required
def profile():
    if current_user is None:
        return jsonify(None), 401
    return jsonify(current_user.to_dict()), 200


@api.route("/change-password", methods=["POST"])
@login_required
def change_password():
    if current_user is None:
        return jsonify(None), 401
    current_password = request.form.get("currentPassword")
    new_password = request.form.get("newPassword")
    confirm_password = request.form.get("confirmPassword")
    # length is verified client side 
    
    if not all([current_password, new_password, confirm_password]):
        return jsonify({"message": "All fields are required"}), 400
    
    if not check_password_hash(current_user.password, current_password):
        return jsonify({"message": "Current password is incorrect"}), 400

    if new_password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400
    
    user = Users.query.filter_by(id=current_user.id).first()
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password changed successfully! You will be logged out soon."}), 200