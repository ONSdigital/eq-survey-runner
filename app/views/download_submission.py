from flask import Blueprint, Response, make_response

import pdfkit

download_submission_blueprint = Blueprint('download_submission', __name__)

@download_submission_blueprint.route('/download_submission', methods=['GET'])
def download_submission():
    print("works")

    pdf = pdfkit.from_url('http://google.com', False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"

    return response